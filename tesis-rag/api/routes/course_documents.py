"""
Gestión de documentos de conocimiento (RAG) por el profesor, scoped por curso.

Flujo: el profe sube un documento declarando capa (doc_layer) y atribución.
El sistema aplica la POLÍTICA DE COPYRIGHT (la misma de ingest.py: patrones y
marcadores prohibidos, paquetes_limpios, etc.) y, si pasa, lo indexa en el RAG
y lo registra en `local_tesisai_documents`. Si no pasa, se rechaza con motivos.

Todo gated por `require_teacher` (rol docente real en Moodle).
La política de indexado/copyright permanece en código (admin); el profe NUNCA la salta.
"""

import json
import os
import re
import time
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

import ingest
from api.dependencies import require_teacher, require_course_admin, TeacherContext
from services import db_service

router = APIRouter(prefix="/authoring/documents", tags=["authoring-documents"])

ALLOWED_EXT = (".md", ".pdf", ".json", ".txt") + ingest.IMAGE_EXTENSIONS
# El profe puede subir contenido propio (canónico) o derivados; los paquetes
# limpios (material atribuible/forense) son competencia del admin, no se suben aquí.
ALLOWED_LAYERS = {"canonico", "derivado"}


def _slug(text: str) -> str:
    s = re.sub(r"[^0-9A-Za-z]+", "_", (text or "").strip().lower()).strip("_")
    return s or f"doc_{int(time.time())}"


def _strip_leading_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return text


def _write_with_metadata(filepath: str, raw: bytes, meta: dict) -> None:
    """Escribe el archivo con la metadata que necesita la política (status/source_origin/etc.)."""
    lower = filepath.lower()
    if lower.endswith(".md"):
        body = _strip_leading_frontmatter(raw.decode("utf-8", errors="ignore"))
        fm = "---\n" + "\n".join(f"{k}: {v}" for k, v in meta.items()) + "\n---\n\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fm + body)
    elif lower.endswith(".json"):
        try:
            data = json.loads(raw.decode("utf-8", errors="ignore"))
        except Exception:
            raise HTTPException(status_code=400, detail="El archivo .json no es JSON válido.")
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="El .json debe ser un objeto (dict) con texto.")
        data.update(meta)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        # pdf / txt / imágenes: se guarda el binario o texto crudo + un sidecar
        # .json con la metadata (la política y _metadata_base lo leen). Para
        # imágenes, el sidecar lleva la DESCRIPCIÓN que es lo que se indexa.
        with open(filepath, "wb") as f:
            f.write(raw)
        base, _ = os.path.splitext(filepath)
        with open(f"{base}.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)


def _doc_to_public(d: dict) -> dict:
    meta = d.get("metadata") or {}
    return {
        "doc_id": d.get("doc_id"),
        "title": d.get("title"),
        "course_id": d.get("course_id"),
        "axis_id": d.get("axis_id"),
        "moodle_section_id": d.get("moodle_section_id"),
        "lesson_id": d.get("lesson_id"),
        "doc_layer": d.get("doc_layer"),
        "doc_type": d.get("doc_type"),
        "filename": d.get("filename"),
        "status": d.get("status"),
        "attribution_required": d.get("attribution_required"),
        "ownership": d.get("ownership"),
        "uploaded_by": d.get("uploaded_by"),
        "scope": d.get("scope"),
        "is_global": bool(d.get("is_global")),
        "resource_type": d.get("resource_type"),
        "allowed_for_indexing": bool(d.get("allowed_for_indexing")),
        "visible_to_student": bool(d.get("visible_to_student")),
        "index_status": d.get("index_status") or "pending",
        "index_error": meta.get("index_error") or "",
        "chunk_count": d.get("chunk_count"),
        "chunks": meta.get("chunks"),
        "media_type": d.get("media_type") or meta.get("media_type") or "document",
        "description": meta.get("description") or d.get("notes") or "",
        "relpath": d.get("relpath"),
        "updated_at": d.get("timemodified"),
    }


@router.get("")
def list_course_documents(scope: str = "", ctx: TeacherContext = Depends(require_teacher)):
    # scope="global" => base universal (filtra por scope='global', no por course_id="").
    if scope == "global":
        docs = db_service.list_documents(scope="global")
        return {"course_id": "", "scope": "global", "documents": [_doc_to_public(d) for d in docs]}
    docs = db_service.list_documents(course_id=ctx.course_id)
    return {"course_id": ctx.course_id, "scope": scope or "course", "documents": [_doc_to_public(d) for d in docs]}


@router.get("/structured")
def structured_course_documents(ctx: TeacherContext = Depends(require_teacher)):
    """Documentos del curso agrupados por scope para la UI de Conocimiento.

    Devuelve la jerarquía REAL (autoritativa desde la BD, no desde Chroma):
      - course: recursos scope='course' (todo el curso, sin eje).
      - sections[moodle_section_id]: { section_resources: scope='section', lessons: { lesson_id: [scope='lesson'] } }.
      - global_docs: scope='global' (compartidos por todos los cursos).
    Un recurso de lección NUNCA aparece en section_resources; se agrupa bajo lessons.
    """
    docs = db_service.list_documents(course_id=ctx.course_id)
    course_docs, sections = [], {}
    for d in docs:
        pub = _doc_to_public(d)
        sc = pub.get("scope") or "course"
        if sc == "course":
            course_docs.append(pub)
        elif sc in {"section", "axis"}:
            section_id = pub.get("moodle_section_id") or pub.get("axis_id") or "(sin seccion)"
            sx = sections.setdefault(section_id, {"section_resources": [], "lessons": {}})
            sx["section_resources"].append(pub)
        elif sc == "lesson":
            section_id = pub.get("moodle_section_id") or pub.get("axis_id") or "(sin seccion)"
            ax = sections.setdefault(section_id, {"section_resources": [], "lessons": {}})
            ax["lessons"].setdefault(pub.get("lesson_id") or "(sin lección)", []).append(pub)
        # global no entra aquí (es cross-curso); se pide aparte con scope='global'.
    global_docs = [_doc_to_public(d) for d in db_service.list_documents(scope="global")]
    return {"course_id": ctx.course_id, "course": course_docs, "sections": sections, "global_docs": global_docs}


def _classify_source(src: str, meta: dict):
    """Devuelve (kind, label, doc_id|None) a partir del source del chunk."""
    s = (src or "").replace("\\", "/")
    if s.startswith("transcription:"):
        return "transcripcion", (s.split(":", 1)[1] or "transcripción"), None
    if s.startswith("resource:"):
        doc_id = s.split(":", 1)[1]
        kind = "imagen" if (meta or {}).get("media_type") == "image" else "doc"
        return kind, ((meta or {}).get("title") or doc_id), doc_id
    base = s.rstrip("/").split("/")[-1]
    if "/cursos/" in s or "/oficial/global/" in s:
        doc_id = os.path.splitext(base)[0]
        kind = "imagen" if (meta or {}).get("media_type") == "image" else "doc"
        return kind, (meta.get("title") or base), doc_id
    return "teoria", base, None


def _view_type(media_type: str, ext: str, source: str) -> str:
    """Cómo renderizar el contenido en el visor del gestor: pdf/image/audio/text/file."""
    if source.startswith("transcription:"):
        return "text"
    e = (ext or "").lower()
    if media_type == "image" or e in ingest.IMAGE_EXTENSIONS:
        return "image"
    if e == ".pdf":
        return "pdf"
    if media_type == "audio" or e in ingest.AUDIO_EXTENSIONS:
        return "audio"
    if e in (".md", ".txt"):
        return "text"
    if media_type == "template" or e in ingest.TEMPLATE_EXTENSIONS:
        return "file"
    return "text"


def _resolver_archivo_source(source: str, course: str):
    """Ruta absoluta del archivo de un source (resource:<doc_id> o ruta del corpus). None si no hay."""
    s = (source or "").replace("\\", "/")
    if s.startswith("transcription:"):
        return None
    if s.startswith("resource:"):
        doc = db_service.get_document(s.split(":", 1)[1], course)
        if doc and doc.get("relpath"):
            return os.path.normpath(os.path.join(ingest.BASE_DIR, doc["relpath"]))
        return None
    path = source if os.path.isabs(source) else os.path.join(ingest.BASE_DIR, source)
    return os.path.normpath(path)


@router.get("/knowledge/summary")
def knowledge_summary(ctx: TeacherContext = Depends(require_teacher)):
    """Resumen de lo INDEXADO (Chroma) del curso: por seccion, con la LISTA de fuentes
    (teoría base, transcripciones, docs subidos) y conteos. Más el bloque global."""
    course = str(ctx.course_id or "")
    out = {
        "course_id": course,
        "total": 0,
        "global": {"teoria": 0, "transcripcion": 0, "docs": 0, "total": 0},
        "by_section": {},
    }
    # agrupador: by_section[section]["_sources"][source] = {kind,label,doc_id,chunks}
    try:
        col = ingest.get_vector_store()._collection
        got = col.get(include=["metadatas"])
        for m in (got.get("metadatas") or []):
            m = m or {}
            cid = str(m.get("course_id", "") or "")
            src = str(m.get("source", "") or "")
            kind, label, doc_id = _classify_source(src, m)
            bucket = "transcripcion" if kind == "transcripcion" else ("docs" if kind in ("doc", "imagen") else "teoria")
            if cid == "":
                g = out["global"]
                g[bucket] += 1
                g["total"] += 1
            elif cid == course:
                section = str(m.get("moodle_section_id") or m.get("axis_id") or m.get("axis") or "(sin seccion)")
                a = out["by_section"].setdefault(section, {"teoria": 0, "transcripcion": 0, "docs": 0, "total": 0, "_sources": {}})
                a[bucket] += 1
                a["total"] += 1
                out["total"] += 1
                key = src or label
                srow = a["_sources"].setdefault(key, {"kind": kind, "label": label, "doc_id": doc_id, "source": src, "chunks": 0})
                srow["chunks"] += 1
        # aplanar _sources -> items[]
        for section, a in out["by_section"].items():
            items = sorted(a.pop("_sources", {}).values(), key=lambda r: (r["kind"], -r["chunks"]))
            a["items"] = items
    except Exception as exc:  # pragma: no cover
        out["error"] = str(exc)
    return out


def _chunks_por_source(source: str, course: str):
    """Devuelve [(texto, meta)] de los chunks indexados con ese source, scopeados al curso."""
    col = ingest.get_vector_store()._collection
    got = col.get(where={"source": source}, include=["documents", "metadatas"])
    docs = got.get("documents") or []
    metas = got.get("metadatas") or []
    pares = []
    for d, m in zip(docs, metas):
        if str((m or {}).get("course_id", "") or "") == course:
            pares.append((d, m or {}))
    return pares


@router.get("/knowledge/item")
def knowledge_item(source: str, scope: str = "", ctx: TeacherContext = Depends(require_teacher)):
    """Detalle de lo indexado para un source: nombre, descripción, tipo (para elegir visor)
    y el texto indexado. El archivo en sí se sirve aparte en /knowledge/file."""
    course = "" if scope == "global" else str(ctx.course_id or "")
    pares = _chunks_por_source(source, course)
    if not pares:
        raise HTTPException(status_code=404, detail="No hay contenido indexado para esta fuente.")
    pares.sort(key=lambda p: p[1].get("chunk_index", 0) if isinstance(p[1].get("chunk_index"), int) else 0)
    texto = "\n\n———\n\n".join((d or "").strip() for d, _ in pares)

    m0 = pares[0][1] or {}
    s = source.replace("\\", "/")
    media_type = m0.get("media_type") or ""
    description = ""
    title = m0.get("title") or os.path.basename(s.rstrip("/"))
    doc_id = None
    if s.startswith("resource:"):
        doc_id = s.split(":", 1)[1]
    elif not s.startswith("transcription:"):
        doc_id = os.path.splitext(os.path.basename(s))[0]
    if doc_id:
        doc = db_service.get_document(doc_id, course)
        if doc:
            meta = doc.get("metadata") or {}
            description = meta.get("description") or doc.get("notes") or ""
            media_type = media_type or meta.get("media_type") or ""
            title = doc.get("title") or title

    path = _resolver_archivo_source(source, course)
    ext = os.path.splitext(path or s)[1]
    has_file = bool(path) and os.path.exists(path)
    return {
        "source": source,
        "chunks": len(pares),
        "label": title,
        "description": description,
        "media_type": media_type,
        "view_type": _view_type(media_type, ext, s),
        "has_file": has_file,
        "text": texto[:25000],
    }


@router.get("/knowledge/file")
def knowledge_file(source: str, scope: str = "", ctx: TeacherContext = Depends(require_teacher)):
    """Sirve el archivo real de un source (pdf/audio/imagen) para el visor del gestor."""
    course = "" if scope == "global" else str(ctx.course_id or "")
    path = _resolver_archivo_source(source, course)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="No hay archivo para esta fuente.")

    def _dentro(target, base):
        try:
            return os.path.commonpath([target, os.path.normpath(base)]) == os.path.normpath(base)
        except ValueError:
            return False

    if not any(_dentro(path, d) for d in ingest.ALLOWED_PUBLIC_DIRS):
        raise HTTPException(status_code=403, detail="Ruta no permitida.")
    from fastapi.responses import FileResponse
    return FileResponse(path)


@router.delete("/knowledge/item")
def delete_knowledge_item(source: str, scope: str = "", ctx: TeacherContext = Depends(require_teacher)):
    """Borra del índice TODO lo de un source (teoría base, transcripción o doc). Para que el
    borrado sea durable, si el source es un archivo del corpus se mueve a `no_indexar/`
    (así un Reindexar no lo vuelve a traer). Transcripciones/recursos solo se desindexan."""
    course = "" if scope == "global" else str(ctx.course_id or "")
    col = ingest.get_vector_store()._collection
    try:
        col.delete(where={"$and": [{"source": source}, {"course_id": course}]})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo desindexar: {exc}")

    file_moved = False
    es_archivo = not source.startswith("transcription:") and not source.startswith("resource:")
    if es_archivo:
        path = source if os.path.isabs(source) else os.path.join(ingest.BASE_DIR, source)
        path = os.path.normpath(path)
        if os.path.exists(path):
            try:
                dest_dir = os.path.join(ingest.NO_INDEX_DIR, "desde_gestor")
                os.makedirs(dest_dir, exist_ok=True)
                import shutil
                shutil.move(path, os.path.join(dest_dir, os.path.basename(path)))
                sidecar = os.path.splitext(path)[0] + ".json"
                if os.path.exists(sidecar):
                    shutil.move(sidecar, os.path.join(dest_dir, os.path.basename(sidecar)))
                file_moved = True
            except Exception as exc:  # pragma: no cover
                print(f"[knowledge delete] no se pudo mover {path}: {exc}")

    # Si además había un registro en documents (doc/imagen subido), límpialo.
    doc_id = os.path.splitext(os.path.basename(source.replace("\\", "/")))[0] if es_archivo else ""
    if doc_id:
        try:
            if db_service.get_document(doc_id, course):
                db_service.delete_document(doc_id, course)
        except Exception:
            pass

    return {"deleted": True, "source": source, "file_moved": file_moved}


@router.post("")
async def upload_course_document(
    file: UploadFile = File(...),
    title: str = Form(""),
    axis_id: str = Form(""),
    moodle_section_id: str = Form(""),
    doc_layer: str = Form("canonico"),
    attribution_required: bool = Form(False),
    ownership: str = Form("kenth_academy"),
    notes: str = Form(""),
    scope: str = Form(""),  # "global" => base universal (course_id="" => lo ven todos los cursos)
    description: str = Form(""),  # contexto/descripción (OBLIGATORIA para imágenes)
    concepts: str = Form(""),     # conceptos/tags separados por coma
    resource_type: str = Form(""),  # uso pedagogico (theory/pdf_reading/...); vacio => default por media_type
    ctx: TeacherContext = Depends(require_teacher),
):
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa PDF, TXT, MD o imagen (png/jpg/webp).")
    is_image = ext in ingest.IMAGE_EXTENSIONS
    if is_image and not description.strip():
        raise HTTPException(status_code=400, detail="Una imagen necesita una descripción de qué muestra para que el tutor la entienda.")
    if doc_layer not in ALLOWED_LAYERS:
        raise HTTPException(
            status_code=400,
            detail="doc_layer inválido. El profesor solo puede subir 'canonico' o 'derivado'. "
                   "Los paquetes limpios son material del administrador.",
        )

    is_global = scope == "global"
    effective_course = "" if is_global else ctx.course_id
    canonical_axis = ""
    effective_section = "" if is_global else str(moodle_section_id or "")
    doc_title = (title or os.path.splitext(filename)[0]).strip()
    doc_id = _slug(doc_title)[:80]

    # Scope explicito y coherente: 'global' exige is_global=1; documento de curso
    # con eje => 'axis'; sin eje => 'course'. Rechaza combinaciones invalidas.
    requested_scope = "global" if is_global else ("section" if effective_section else "course")
    try:
        doc_scope, is_global = db_service.validate_scope(
            scope=requested_scope, course_id=effective_course,
            axis_id=canonical_axis,
            moodle_section_id=effective_section,
            lesson_id="",
            is_global=is_global,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if is_global:
        os.makedirs(ingest.GLOBAL_DIR, exist_ok=True)
        target_dir = ingest.GLOBAL_DIR
    else:
        target_dir = ingest.course_upload_dir(ctx.course_id)
    dest = os.path.join(target_dir, f"{doc_id}{ext}")

    concepts_list = [c.strip() for c in (concepts or "").split(",") if c.strip()]
    media_type_str = "image" if is_image else "document"
    eff_resource_type = (resource_type or "").strip().lower() or db_service.default_resource_type(media_type_str, ext.lstrip("."))
    if eff_resource_type not in db_service.RESOURCE_TYPES:
        eff_resource_type = db_service.default_resource_type(media_type_str, ext.lstrip("."))
    meta = {
        "status": "ready_for_indexing",
        "source_origin": "course",
        "allowed_for_indexing": True,
        # Conocimiento del curso: el tutor lo usa/cita; no es un asset descargable
        # por el alumno salvo que sea imagen exhibible. Imagen => visible.
        "visible_to_student": bool(is_image),
        "doc_layer": doc_layer,
        "axis": canonical_axis,
        "axis_id": canonical_axis,
        "moodle_section_id": effective_section,
        "course_id": effective_course,
        "scope": doc_scope,
        "is_global": bool(is_global),
        "ownership": ownership,
        "attribution_required": bool(attribution_required),
        "title": doc_title,
        "description": description,
        "concepts": concepts_list,
        "media_type": media_type_str,
        "resource_type": eff_resource_type,
    }

    raw = await file.read()
    _write_with_metadata(dest, raw, meta)

    # Aplica la política de copyright e indexa de forma incremental.
    result = ingest.add_single_document(dest)
    if not result.get("success"):
        # Rechazado por política → limpiar archivos y devolver motivos.
        for p in (dest, os.path.splitext(dest)[0] + ".json"):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Documento rechazado por la política de contenido (copyright).",
                "reasons": result.get("reasons", [result.get("message", "no aprobado")]),
            },
        )

    relpath = os.path.relpath(dest, ingest.BASE_DIR).replace("\\", "/")
    chunks = result.get("chunks", 0)
    db_service.upsert_document(
        doc_id=doc_id,
        course_id=effective_course,
        axis_id=canonical_axis,
        moodle_section_id=effective_section,
        title=doc_title,
        doc_layer=doc_layer,
        doc_type=ext.lstrip("."),
        filename=f"{doc_id}{ext}",
        relpath=relpath,
        attribution_required=bool(attribution_required),
        allowed_for_indexing=True,
        visible_to_student=bool(is_image),
        media_type=media_type_str,
        resource_type=eff_resource_type,
        scope=doc_scope,
        is_global=bool(is_global),
        index_status="indexed" if chunks > 0 else "failed",
        chunk_count=chunks,
        ownership=ownership,
        status="active",
        uploaded_by=ctx.user_id,
        notes=notes,
        metadata={"chunks": chunks, "media_type": "image" if is_image else "document"},
    )
    doc = db_service.get_document(doc_id, effective_course)
    return {"success": True, "chunks": result.get("chunks", 0), "document": _doc_to_public(doc or {})}


@router.post("/caption")
async def suggest_image_caption(file: UploadFile = File(...), ctx: TeacherContext = Depends(require_teacher)):
    """Borrador de descripción de una imagen con el modelo de visión (botón 'sugerir con IA')."""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ingest.IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Solo imágenes (png/jpg/webp).")
    raw = await file.read()
    import base64
    from services.agent import vision
    b64 = base64.b64encode(raw).decode("ascii")
    text = vision.describir_imagen_para_conocimiento(b64)
    if not text:
        raise HTTPException(status_code=502, detail="El modelo de visión no devolvió descripción. Escríbela a mano.")
    return {"description": text}


@router.get("/media/{doc_id}")
def get_media(doc_id: str, scope: str = "", token: str = "", ctx: TeacherContext = Depends(require_teacher)):
    """Sirve el archivo (imagen/pdf) de un documento, para preview en el hub / chat."""
    from fastapi.responses import FileResponse
    course = "" if scope == "global" else ctx.course_id
    doc = db_service.get_document(doc_id, course)
    if not doc or not doc.get("relpath"):
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    path = os.path.join(ingest.BASE_DIR, doc["relpath"])
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado en disco.")
    return FileResponse(path)


@router.post("/reindex")
def reindex_course_documents(ctx: TeacherContext = Depends(require_course_admin)):
    # Reindex de Chroma por curso: acción destructiva/costosa reservada al gestor
    # del curso (moodle/course:update) o superior. El profesor editor NO reindexa.
    result = ingest.reindex_course_documents(ctx.course_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "No se pudo reindexar el curso."))

    docs = db_service.list_documents(course_id=ctx.course_id)
    return {
        **result,
        "documents": [_doc_to_public(d) for d in docs],
    }


@router.delete("/{doc_id}")
def delete_course_document(doc_id: str, scope: str = "", ctx: TeacherContext = Depends(require_teacher)):
    course = "" if scope == "global" else ctx.course_id
    doc = db_service.get_document(doc_id, course)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")

    relpath = doc.get("relpath", "")
    if relpath:
        filepath = os.path.join(ingest.BASE_DIR, relpath)
        ingest.remove_single_document(filepath)  # quita los chunks del RAG
        for p in (filepath, os.path.splitext(filepath)[0] + ".json"):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass

    db_service.delete_document(doc_id, course)
    return {"deleted": True, "doc_id": doc_id}
