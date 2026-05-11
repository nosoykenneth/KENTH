"""
Endpoints minimos de la vertical slice piloto.

Sirven para que el frontend liste las lecciones piloto y, opcionalmente,
inspeccione el bloque resuelto a un timestamp dado (debug).
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from services.pilot_service import (
    list_pilot_lessons,
    load_pilot_lesson,
    is_pilot_lesson,
    resolve_pilot_block,
)
from services.db_service import (
    get_resource_link,
    list_resource_links,
    upsert_resource_link,
    delete_resource_link,
)

router = APIRouter(prefix="/pilot", tags=["pilot"])


class ResourceLinkPayload(BaseModel):
    lesson_id: str
    course_id: str = ""
    resource_type: str = ""
    resource_subtype: str = ""


@router.get("/lessons")
def get_pilot_lessons():
    """Lista resumida de lecciones piloto."""
    return {"lessons": list_pilot_lessons()}


@router.get("/lessons/{lesson_id}")
def get_pilot_lesson(lesson_id: str):
    """Manifiesto plano completo de una leccion piloto."""
    lesson = load_pilot_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Pilot lesson not found")
    return lesson


@router.get("/lessons/{lesson_id}/block")
def get_pilot_block(lesson_id: str, t: Optional[float] = Query(default=None)):
    """Devuelve el bloque resuelto para un timestamp dado.

    Util para debug: el frontend puede pintar que bloque corresponde a
    un slider de tiempo sin tener que clonar la logica del backend.
    """
    resolved = resolve_pilot_block(lesson_id, t)
    if not resolved.get("lesson"):
        raise HTTPException(status_code=404, detail="Pilot lesson not found")
    return {
        "lesson_id": lesson_id,
        "timestamp": t,
        "block": resolved.get("block"),
    }


# ==========================================
# VINCULOS RECURSO <-> LECCION
# ==========================================

@router.get("/links")
def list_links(course_id: Optional[str] = Query(default=None)):
    """Lista vinculos. Si course_id viene, filtra por curso.

    El frontend lo usa para hidratar de un solo golpe los badges de
    "leccion enlazada" en la vista de contenido del curso.
    """
    return {"links": list_resource_links(course_id)}


@router.get("/links/{resource_id}")
def get_link(resource_id: str):
    """Devuelve el vinculo del recurso o 404 si no esta enlazado."""
    link = get_resource_link(resource_id)
    if not link:
        raise HTTPException(status_code=404, detail="Resource not linked")
    return link


@router.put("/links/{resource_id}")
def put_link(resource_id: str, payload: ResourceLinkPayload):
    """Crea o actualiza el vinculo recurso -> leccion piloto."""
    if not is_pilot_lesson(payload.lesson_id):
        raise HTTPException(
            status_code=400,
            detail=f"lesson_id '{payload.lesson_id}' no es una leccion piloto registrada.",
        )
    lesson = load_pilot_lesson(payload.lesson_id) or {}
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
    """Quita el vinculo. Idempotente."""
    deleted = delete_resource_link(resource_id)
    return {"deleted": deleted, "resource_id": resource_id}
