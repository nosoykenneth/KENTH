"""
Endpoints REST de la estructura formal del curso por ejes.

Reemplaza al antiguo router `/pilot`. La capa operativa ahora es
`course_runtime/axes/eje_N/` y se expone bajo el prefijo `/axes`.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from services.axis_service import (
    is_known_lesson,
    list_axes,
    list_all_lessons,
    list_lessons_of_axis,
    list_resources_of_axis,
    load_axis_manifest,
    load_course_manifest,
    load_lesson,
    load_resource,
    resolve_lesson_block,
)
from services.db_service import (
    delete_resource_link,
    get_resource_link,
    list_resource_links,
    upsert_resource_link,
)


router = APIRouter(prefix="/axes", tags=["axes"])


class ResourceLinkPayload(BaseModel):
    lesson_id: str
    course_id: str = ""
    resource_type: str = ""
    resource_subtype: str = ""


# ==========================================
# MANIFEST GLOBAL Y POR EJE
# ==========================================

@router.get("")
def get_course_manifest():
    """Manifest global del curso con la lista de los 8 ejes."""
    return load_course_manifest()


@router.get("/list")
def get_axes_list(course_id: Optional[str] = Query(default=None)):
    """Lista detallada de los ejes con su manifest."""
    return {"axes": list_axes(course_id)}


# IMPORTANTE: /links debe declararse ANTES de /{axis_id}; si no, FastAPI hace
# match de "links" como un axis_id y responde 404 "Axis not found".
@router.get("/links")
def list_links(course_id: Optional[str] = Query(default=None)):
    """Lista vínculos. Si course_id viene, filtra por curso."""
    return {"links": list_resource_links(course_id)}


@router.get("/{axis_id}")
def get_axis(axis_id: str, course_id: Optional[str] = Query(default=None)):
    """Manifest individual de un eje (axis_id puede ser 'Eje 0', 'eje_0', '0')."""
    manifest = load_axis_manifest(axis_id, course_id)
    if not manifest:
        raise HTTPException(status_code=404, detail="Axis not found")
    return manifest


@router.get("/{axis_id}/lessons")
def get_axis_lessons(axis_id: str, course_id: Optional[str] = Query(default=None)):
    """Lecciones de un eje en formato resumido."""
    if not load_axis_manifest(axis_id, course_id):
        raise HTTPException(status_code=404, detail="Axis not found")
    return {"axis_id": axis_id, "lessons": list_lessons_of_axis(axis_id, course_id)}


@router.get("/{axis_id}/resources")
def get_axis_resources(axis_id: str, course_id: Optional[str] = Query(default=None)):
    """Recursos declarados por el eje (canónico, paquete limpio, derivados)."""
    if not load_axis_manifest(axis_id, course_id):
        raise HTTPException(status_code=404, detail="Axis not found")
    return {"axis_id": axis_id, "resources": list_resources_of_axis(axis_id, course_id)}


# ==========================================
# LECCIONES (acceso plano por lesson_id)
# ==========================================

@router.get("/lessons/all")
def get_all_lessons(course_id: Optional[str] = Query(default=None)):
    """Lista resumida de todas las lecciones del curso (todos los ejes)."""
    return {"lessons": list_all_lessons(course_id)}


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str, course_id: Optional[str] = Query(default=None)):
    """Manifest plano completo de una lección."""
    lesson = load_lesson(lesson_id, course_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/lessons/{lesson_id}/block")
def get_lesson_block(
    lesson_id: str,
    t: Optional[float] = Query(default=None),
    course_id: Optional[str] = Query(default=None),
):
    """Devuelve el bloque del video activo para un timestamp dado.

    Útil para debug y para que el frontend pinte qué bloque corresponde
    a un slider de tiempo sin clonar la lógica del backend.
    """
    lesson = load_lesson(lesson_id, course_id)
    resolved = resolve_lesson_block(lesson_id, t) if lesson else {"lesson": None, "block": None}
    if not resolved.get("lesson"):
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {
        "lesson_id": lesson_id,
        "timestamp": t,
        "block": resolved.get("block"),
    }


# ==========================================
# RECURSOS (acceso plano por resource_id)
# ==========================================

@router.get("/resources/{resource_id}")
def get_resource(resource_id: str):
    """Manifest plano de un recurso."""
    data = load_resource(resource_id)
    if not data:
        raise HTTPException(status_code=404, detail="Resource not found")
    return data


# ==========================================
# VINCULOS RECURSO MOODLE <-> LECCION
# ==========================================
# Misma semántica que tenía /pilot/links: permiten que un módulo de
# Moodle (video, PDF, H5P) quede vinculado a una lección formal del
# course_runtime para que el tutor sepa qué contexto inyectar.
# (GET /links se declara arriba, antes de /{axis_id}, para no ser eclipsado.)

@router.get("/links/{resource_id}")
def get_link(resource_id: str):
    """Devuelve el vínculo del recurso o 404 si no está enlazado."""
    link = get_resource_link(resource_id)
    if not link:
        raise HTTPException(status_code=404, detail="Resource not linked")
    return link


@router.put("/links/{resource_id}")
def put_link(resource_id: str, payload: ResourceLinkPayload):
    """Crea o actualiza el vínculo recurso Moodle -> lección formal."""
    if not is_known_lesson(payload.lesson_id, payload.course_id or None):
        raise HTTPException(
            status_code=400,
            detail=f"lesson_id '{payload.lesson_id}' no es una lección registrada en el course_runtime.",
        )
    lesson = load_lesson(payload.lesson_id, payload.course_id or None) or {}
    link = upsert_resource_link(
        resource_id=resource_id,
        lesson_id=payload.lesson_id,
        course_id=payload.course_id,
        axis_id=lesson.get("axis_id", ""),
        resource_type=payload.resource_type,
        resource_subtype=payload.resource_subtype,
    )
    return link


@router.delete("/links/{resource_id}")
def remove_link(resource_id: str):
    """Quita el vínculo. Idempotente."""
    deleted = delete_resource_link(resource_id)
    return {"deleted": deleted, "resource_id": resource_id}
