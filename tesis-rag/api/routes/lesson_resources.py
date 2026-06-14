"""
Recursos por lección: el profe sube N recursos (imagen, plantilla .flp/.als, audio
.wav/.mp3, pdf/txt) ligados a una lección. Cada recurso declara dos flags:
  - Indexar al tutor (allowed_for_indexing): su descripción/contenido entra al RAG.
  - Visible al alumno (visible_to_student): aparece en el panel de la lección y el
    tutor lo puede mostrar/enlazar.

Reusa la tabla `local_tesisai_documents` (extendida con lesson_id + visible_to_student),
el storage propio (course_upload_dir) y el índice Chroma. Endpoints docentes gated por
require_teacher; el listado/descarga del alumno valida visible_to_student.
"""

import os
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

import ingest
from api.dependencies import require_teacher, TeacherContext
from services import db_service
from api.routes.course_documents import _slug, _write_with_metadata

router = APIRouter(tags=["lesson-resources"])


def _resource_to_public(d: dict) -> dict:
    meta = d.get("metadata") or {}
    media_type = d.get("media_type") or meta.get("media_type") or ingest.resource_media_type(d.get("doc_type", ""))
    doc_id = d.get("doc_id")
    return {
        "doc_id": doc_id,
        "title": d.get("title"),
        "course_id": d.get("course_id"),
        "lesson_id": d.get("lesson_id"),
        "axis_id": d.get("axis_id"),
        "moodle_section_id": d.get("moodle_section_id"),
        "doc_type": d.get("doc_type"),
        "media_type": media_type,
        "resource_type": d.get("resource_type"),
        "description": meta.get("description") or d.get("notes") or "",
        "concepts": meta.get("concepts") or [],
        "indexed": bool(d.get("allowed_for_indexing")),
        "allowed_for_indexing": bool(d.get("allowed_for_indexing")),
        "visible_to_student": bool(d.get("visible_to_student")),
        "scope": d.get("scope") or "lesson",
        "is_global": bool(d.get("is_global")),
        "index_status": d.get("index_status") or "pending",
        "index_error": meta.get("index_error") or "",
        "chunk_count": d.get("chunk_count"),
        "chunks": meta.get("chunks"),
        "filename": d.get("filename"),
        "download_url": f"/api/ai/lessons/resources/{doc_id}/file?course_id={d.get('course_id','')}",
        "updated_at": d.get("timemodified"),
    }


# ============================================================
# DOCENTE (gated) — helper compartido lección/eje
# ============================================================

async def _store_resource(
    *,
    scope: str,
    course_id: str,
    axis_id: str,
    lesson_id: str,
    moodle_section_id: str = "",
    file: UploadFile,
    title: str,
    description: str,
    concepts: str,
    index_to_tutor: bool,
    visible_to_student: Optional[bool],
    resource_type: str,
    uploaded_by: str,
) -> dict:
    """Sube + (opcional) indexa + registra un recurso en un scope dado.

    Reutilizado por recursos de LECCIÓN (scope='lesson') y de EJE (scope='axis').
    Un recurso de eje NO lleva lesson_id; uno de lección sí. El scope/coordenadas
    se validan antes de tocar disco para no dejar archivos huérfanos.
    """
    # Validación de coherencia scope<->coordenadas (lanza ValueError->400).
    try:
        scope, is_global = db_service.validate_scope(
            scope=scope, course_id=course_id, axis_id=axis_id,
            moodle_section_id=moodle_section_id, lesson_id=lesson_id, is_global=False,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ingest.RESOURCE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Formato no permitido. Imágenes, audio (wav/mp3), plantillas (flp/als…), pdf/txt/md.",
        )
    media_type = ingest.resource_media_type(ext)
    eff_resource_type = (resource_type or "").strip().lower() or db_service.default_resource_type(media_type, ext.lstrip("."))
    if eff_resource_type not in db_service.RESOURCE_TYPES:
        eff_resource_type = db_service.default_resource_type(media_type, ext.lstrip("."))

    # Visibilidad: si el docente no la fija explícitamente, solution/rubric son
    # material del profe (default oculto); el resto, visible por defecto.
    if visible_to_student is None:
        visible = eff_resource_type not in db_service.TEACHER_ONLY_RESOURCE_TYPES
    else:
        visible = bool(visible_to_student)

    if index_to_tutor and media_type != "document" and not description.strip():
        raise HTTPException(
            status_code=400,
            detail="Para que el tutor lo entienda, este recurso necesita una descripción de qué es y para qué sirve.",
        )

    doc_title = (title or os.path.splitext(filename)[0]).strip()
    seed = f"{lesson_id}_{doc_title}" if scope == "lesson" else f"{moodle_section_id}_{doc_title}"
    doc_id = _slug(seed)[:80]
    concepts_list = [c.strip() for c in (concepts or "").split(",") if c.strip()]

    target_dir = ingest.course_upload_dir(course_id)
    os.makedirs(target_dir, exist_ok=True)
    dest = os.path.join(target_dir, f"{doc_id}{ext}")

    meta = {
        "status": "ready_for_indexing",
        "source_origin": "course",
        "allowed_for_indexing": bool(index_to_tutor),
        "visible_to_student": bool(visible),
        "doc_layer": "canonico",
        "axis": "",
        "axis_id": "",
        "moodle_section_id": moodle_section_id,
        "course_id": course_id,
        "lesson_id": lesson_id,
        "scope": scope,
        "is_global": False,
        "title": doc_title,
        "description": description,
        "concepts": concepts_list,
        "media_type": media_type,
        "resource_type": eff_resource_type,
    }

    raw = await file.read()
    _write_with_metadata(dest, raw, meta)
    relpath = os.path.relpath(dest, ingest.BASE_DIR).replace("\\", "/")

    chunks = 0
    index_error = ""
    if index_to_tutor:
        if media_type in ("document", "image"):
            result = ingest.add_single_document(dest)
            if not result.get("success"):
                for p in (dest, os.path.splitext(dest)[0] + ".json"):
                    try:
                        if os.path.exists(p):
                            os.remove(p)
                    except OSError:
                        pass
                raise HTTPException(
                    status_code=422,
                    detail={
                        "message": "Recurso rechazado por la política de contenido (copyright).",
                        "reasons": result.get("reasons", [result.get("message", "no aprobado")]),
                    },
                )
            chunks = result.get("chunks", 0)
        else:
            r = ingest.index_resource_description(
                course_id=course_id, lesson_id=lesson_id, doc_id=doc_id,
                title=doc_title, description=description, concepts=concepts_list,
                axis_id="", moodle_section_id=moodle_section_id,
                media_type=media_type, media_path=relpath, doc_type=ext.lstrip("."),
                visible_to_student=bool(visible), allowed_for_indexing=True,
                scope=scope, is_global=False, resource_type=eff_resource_type,
            )
            chunks = r.get("chunks", 0)
            if not r.get("success"):
                index_error = r.get("message", "no se pudo indexar la descripción del recurso")

    if not index_to_tutor:
        index_status = "pending"
    elif chunks > 0:
        index_status = "indexed"
    else:
        index_status = "failed"
        if not index_error:
            index_error = "indexación solicitada pero no se generaron chunks"

    metadata_payload = {
        "chunks": chunks,
        "media_type": media_type,
        "description": description,
        "concepts": concepts_list,
    }
    if index_status == "failed" and index_error:
        metadata_payload["index_error"] = index_error

    db_service.upsert_document(
        doc_id=doc_id,
        course_id=course_id,
        axis_id="",
        moodle_section_id=moodle_section_id,
        lesson_id=lesson_id,
        title=doc_title,
        doc_layer="canonico",
        doc_type=ext.lstrip("."),
        filename=f"{doc_id}{ext}",
        relpath=relpath,
        allowed_for_indexing=bool(index_to_tutor),
        visible_to_student=bool(visible),
        media_type=media_type,
        resource_type=eff_resource_type,
        scope=scope,
        is_global=False,
        index_status=index_status,
        chunk_count=chunks,
        ownership="kenth_academy",
        status="active",
        uploaded_by=uploaded_by,
        notes=description,
        metadata=metadata_payload,
    )
    doc = db_service.get_document(doc_id, course_id)
    return {"success": True, "chunks": chunks, "resource": _resource_to_public(doc or {})}


@router.post("/authoring/lessons/{lesson_id}/resources")
async def upload_lesson_resource(
    lesson_id: str,
    file: UploadFile = File(...),
    title: str = Form(""),
    description: str = Form(""),
    concepts: str = Form(""),
    index_to_tutor: bool = Form(True),
    visible_to_student: Optional[bool] = Form(None),
    resource_type: str = Form(""),
    ctx: TeacherContext = Depends(require_teacher),
):
    lesson = db_service.get_lesson(lesson_id, ctx.course_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="La lección no existe en este curso.")
    return await _store_resource(
        scope="lesson", course_id=ctx.course_id, axis_id="",
        moodle_section_id=lesson.get("moodle_section_id", ""), lesson_id=lesson_id,
        file=file, title=title, description=description, concepts=concepts,
        index_to_tutor=index_to_tutor, visible_to_student=visible_to_student,
        resource_type=resource_type, uploaded_by=ctx.user_id,
    )


@router.get("/authoring/lessons/{lesson_id}/resources")
def list_lesson_resources(
    lesson_id: str,
    include_section: bool = False,
    ctx: TeacherContext = Depends(require_teacher),
):
    """Recursos de la lección. Con include_section=true, añade los recursos HEREDADOS
    de la sección (scope='section') como lista separada y de SOLO LECTURA (no son de la lección)."""
    docs = db_service.list_documents(course_id=ctx.course_id, lesson_id=lesson_id)
    out = {"resources": [_resource_to_public(d) for d in docs]}
    if include_section:
        lesson = db_service.get_lesson(lesson_id, ctx.course_id)
        section_id = (lesson or {}).get("moodle_section_id") or ""
        inherited = []
        if section_id:
            for d in db_service.list_documents(course_id=ctx.course_id):
                if d.get("scope") in {"section", "axis"} and (d.get("moodle_section_id") or d.get("axis_id")) == section_id:
                    inherited.append(_resource_to_public(d))
        out["inherited_section_resources"] = inherited
        out["moodle_section_id"] = section_id
    return out


# ============================================================
# DOCENTE - RECURSOS DE SECCION (scope='section', sin lesson_id)
# ============================================================

@router.post("/authoring/sections/{section_id}/resources")
async def upload_section_resource(
    section_id: str,
    file: UploadFile = File(...),
    title: str = Form(""),
    description: str = Form(""),
    concepts: str = Form(""),
    index_to_tutor: bool = Form(True),
    visible_to_student: Optional[bool] = Form(None),
    resource_type: str = Form(""),
    ctx: TeacherContext = Depends(require_teacher),
):
    return await _store_resource(
        scope="section", course_id=ctx.course_id, axis_id="",
        moodle_section_id=section_id, lesson_id="",
        file=file, title=title, description=description, concepts=concepts,
        index_to_tutor=index_to_tutor, visible_to_student=visible_to_student,
        resource_type=resource_type, uploaded_by=ctx.user_id,
    )


@router.get("/authoring/sections/{section_id}/resources")
def list_section_resources(section_id: str, ctx: TeacherContext = Depends(require_teacher)):
    docs = [
        d for d in db_service.list_documents(course_id=ctx.course_id)
        if d.get("scope") == "section" and d.get("moodle_section_id") == section_id
    ]
    return {"moodle_section_id": section_id, "resources": [_resource_to_public(d) for d in docs]}


@router.delete("/authoring/sections/{section_id}/resources/{doc_id}")
def delete_section_resource(section_id: str, doc_id: str, ctx: TeacherContext = Depends(require_teacher)):
    doc = db_service.get_document(doc_id, ctx.course_id)
    if not doc or doc.get("scope") != "section" or doc.get("moodle_section_id") != section_id:
        raise HTTPException(status_code=404, detail="Recurso de seccion no encontrado.")
    relpath = doc.get("relpath", "")
    if relpath:
        filepath = os.path.join(ingest.BASE_DIR, relpath)
        ingest.remove_single_document(filepath)
        for p in (filepath, os.path.splitext(filepath)[0] + ".json"):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass
    ingest.delete_resource_index(doc_id)
    db_service.delete_document(doc_id, ctx.course_id)
    return {"deleted": True, "doc_id": doc_id}


@router.delete("/authoring/lessons/{lesson_id}/resources/{doc_id}")
def delete_lesson_resource(lesson_id: str, doc_id: str, ctx: TeacherContext = Depends(require_teacher)):
    doc = db_service.get_document(doc_id, ctx.course_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Recurso no encontrado.")

    relpath = doc.get("relpath", "")
    if relpath:
        filepath = os.path.join(ingest.BASE_DIR, relpath)
        ingest.remove_single_document(filepath)  # chunks de contenido (doc/imagen)
        for p in (filepath, os.path.splitext(filepath)[0] + ".json"):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass
    ingest.delete_resource_index(doc_id)  # chunks de descripción (audio/plantilla)
    db_service.delete_document(doc_id, ctx.course_id)
    return {"deleted": True, "doc_id": doc_id}


# ============================================================
# ALUMNO (sin gate docente; valida visible_to_student)
# ============================================================

@router.get("/lessons/{lesson_id}/resources")
def student_lesson_resources(lesson_id: str, course_id: str = ""):
    """Recursos VISIBLES de la lección, para el panel del alumno."""
    docs = db_service.list_documents(course_id=course_id or None, lesson_id=lesson_id, visible_only=True)
    return {"resources": [_resource_to_public(d) for d in docs]}


@router.get("/lessons/resources/{doc_id}/file")
def download_resource_file(doc_id: str, course_id: str = ""):
    """Sirve/descarga el archivo de un recurso VISIBLE (imagen inline, resto attachment)."""
    doc = db_service.get_document(doc_id, course_id or None)
    if not doc:
        raise HTTPException(status_code=404, detail="Recurso no encontrado.")
    if not doc.get("visible_to_student"):
        raise HTTPException(status_code=403, detail="Este recurso no está disponible para estudiantes.")
    relpath = doc.get("relpath", "")
    if not relpath:
        raise HTTPException(status_code=404, detail="El recurso no tiene archivo asociado.")
    path = os.path.join(ingest.BASE_DIR, relpath)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado en disco.")

    media_type = (doc.get("metadata") or {}).get("media_type") or ingest.resource_media_type(doc.get("doc_type", ""))
    if media_type == "image":
        return FileResponse(path)
    return FileResponse(path, filename=doc.get("filename") or os.path.basename(path),
                        media_type="application/octet-stream")
