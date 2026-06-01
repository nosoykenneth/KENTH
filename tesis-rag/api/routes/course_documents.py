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
from api.dependencies import require_teacher, TeacherContext
from services import db_service
from services.axis_service import _canonical_axis_id

router = APIRouter(prefix="/authoring/documents", tags=["authoring-documents"])

ALLOWED_EXT = (".md", ".pdf", ".json")
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
    elif lower.endswith(".pdf"):
        with open(filepath, "wb") as f:
            f.write(raw)
        # sidecar JSON con la metadata para la política
        base, _ = os.path.splitext(filepath)
        with open(f"{base}.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)


def _doc_to_public(d: dict) -> dict:
    return {
        "doc_id": d.get("doc_id"),
        "title": d.get("title"),
        "axis_id": d.get("axis_id"),
        "doc_layer": d.get("doc_layer"),
        "doc_type": d.get("doc_type"),
        "filename": d.get("filename"),
        "status": d.get("status"),
        "attribution_required": d.get("attribution_required"),
        "ownership": d.get("ownership"),
        "uploaded_by": d.get("uploaded_by"),
        "chunks": (d.get("metadata") or {}).get("chunks"),
        "updated_at": d.get("timemodified"),
    }


@router.get("")
def list_course_documents(ctx: TeacherContext = Depends(require_teacher)):
    docs = db_service.list_documents(course_id=ctx.course_id)
    return {"course_id": ctx.course_id, "documents": [_doc_to_public(d) for d in docs]}


@router.post("")
async def upload_course_document(
    file: UploadFile = File(...),
    title: str = Form(""),
    axis_id: str = Form(""),
    doc_layer: str = Form("canonico"),
    attribution_required: bool = Form(False),
    ownership: str = Form("kenth_academy"),
    notes: str = Form(""),
    ctx: TeacherContext = Depends(require_teacher),
):
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Solo se permiten .md, .pdf o .json.")
    if doc_layer not in ALLOWED_LAYERS:
        raise HTTPException(
            status_code=400,
            detail="doc_layer inválido. El profesor solo puede subir 'canonico' o 'derivado'. "
                   "Los paquetes limpios son material del administrador.",
        )

    canonical_axis = _canonical_axis_id(axis_id) if axis_id else ""
    doc_title = (title or os.path.splitext(filename)[0]).strip()
    doc_id = _slug(doc_title)[:80]

    target_dir = ingest.course_upload_dir(ctx.course_id)
    dest = os.path.join(target_dir, f"{doc_id}{ext}")

    meta = {
        "status": "ready_for_indexing",
        "source_origin": "course",
        "allowed_for_indexing": True,
        "doc_layer": doc_layer,
        "axis": canonical_axis,
        "course_id": ctx.course_id,
        "ownership": ownership,
        "attribution_required": bool(attribution_required),
        "title": doc_title,
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
    db_service.upsert_document(
        doc_id=doc_id,
        course_id=ctx.course_id,
        axis_id=canonical_axis,
        title=doc_title,
        doc_layer=doc_layer,
        doc_type=ext.lstrip("."),
        filename=f"{doc_id}{ext}",
        relpath=relpath,
        attribution_required=bool(attribution_required),
        allowed_for_indexing=True,
        ownership=ownership,
        status="active",
        uploaded_by=ctx.user_id,
        notes=notes,
        metadata={"chunks": result.get("chunks", 0)},
    )
    doc = db_service.get_document(doc_id, ctx.course_id)
    return {"success": True, "chunks": result.get("chunks", 0), "document": _doc_to_public(doc or {})}


@router.post("/reindex")
def reindex_course_documents(ctx: TeacherContext = Depends(require_teacher)):
    result = ingest.reindex_course_documents(ctx.course_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "No se pudo reindexar el curso."))

    docs = db_service.list_documents(course_id=ctx.course_id)
    return {
        **result,
        "documents": [_doc_to_public(d) for d in docs],
    }


@router.delete("/{doc_id}")
def delete_course_document(doc_id: str, ctx: TeacherContext = Depends(require_teacher)):
    doc = db_service.get_document(doc_id, ctx.course_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado en este curso.")

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

    db_service.delete_document(doc_id, ctx.course_id)
    return {"deleted": True, "doc_id": doc_id}
