"""Endpoints de Moodle Sections para el Tutor IA.

Este router es la fuente nueva de estructura del curso. `/axes/*` queda como
alias legacy y no debe usarse para crear estructura pedagógica nueva.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from api.dependencies import require_course_view, require_teacher, TeacherContext
from services import db_service, section_service
from services.moodle_ws_client import MoodleWSClient, MoodleWSError, get_moodle_ws_client


router = APIRouter(prefix="/sections", tags=["sections"])


class ResourceLinkPayload(BaseModel):
    lesson_id: str
    course_id: str = ""
    moodle_section_id: Optional[str] = None
    resource_type: str = ""
    resource_subtype: str = ""


def _course(course_id: Optional[str]) -> str:
    value = str(course_id or "").strip()
    if not value:
        raise HTTPException(status_code=400, detail="course_id es requerido para secciones Moodle")
    return db_service.resolve_course_numeric(value) or value


async def _sections_or_error(course_id: str, client: MoodleWSClient):
    try:
        sections = await section_service.list_moodle_sections(course_id, client)
    except MoodleWSError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError:
        raise HTTPException(status_code=400, detail="course_id debe ser numérico Moodle")

    if not sections and not getattr(client, "configured", False) and not db_service.using_moodle_db():
        raise HTTPException(
            status_code=503,
            detail="No hay Moodle Web Services ni conexion a la BD Moodle para leer secciones",
        )
    return sections


@router.get("/list")
async def list_sections(
    _view: TeacherContext = Depends(require_course_view),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    # El curso proviene del contexto validado (`require_course_view` acepta la
    # cabecera X-Course-Id o el query course_id y ya validó `puede_ver_curso`).
    return {"sections": await _sections_or_error(_view.course_id, client)}


@router.get("/lessons/all")
async def list_all_lessons(
    _view: TeacherContext = Depends(require_course_view),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    course = _view.course_id
    await _sections_or_error(course, client)
    return {"lessons": await section_service.list_all_lessons(course, client)}


@router.get("/lessons/{lesson_id}")
def get_lesson(
    lesson_id: str,
    course_id: Optional[str] = Query(default=None),
    _view: TeacherContext = Depends(require_course_view),
):
    """Manifest plano completo de una lección."""
    lesson = section_service.load_lesson(lesson_id, course_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/lessons/{lesson_id}/block")
def get_lesson_block(
    lesson_id: str,
    t: Optional[float] = Query(default=None),
    course_id: Optional[str] = Query(default=None),
    _view: TeacherContext = Depends(require_course_view),
):
    """Bloque del video activo para un timestamp dado (debug / slider de tiempo)."""
    lesson = section_service.load_lesson(lesson_id, course_id)
    resolved = section_service.resolve_lesson_block(lesson_id, t) if lesson else {"lesson": None, "block": None}
    if not resolved.get("lesson"):
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"lesson_id": lesson_id, "timestamp": t, "block": resolved.get("block")}


@router.get("/links")
async def list_links(
    _view: TeacherContext = Depends(require_course_view),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    course = _view.course_id
    await _sections_or_error(course, client)
    links = []
    for link in db_service.list_resource_links(course):
        links.append(await section_service.enrich_link_with_section(link, client))
    return {"links": links}


@router.get("/links/{resource_id}")
async def get_link(
    resource_id: str,
    course_id: Optional[str] = Query(default=None),
    _view: TeacherContext = Depends(require_course_view),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    link = db_service.get_resource_link(resource_id)
    if not link:
        raise HTTPException(status_code=404, detail="Resource not linked")
    course = _course(course_id) if course_id else None
    if course and str(link.get("course_id") or "") not in db_service._course_id_variants(course):
        raise HTTPException(status_code=404, detail="Resource not linked in this course")
    return await section_service.enrich_link_with_section(link, client)


@router.put("/links/{resource_id}")
async def put_link(
    resource_id: str,
    payload: ResourceLinkPayload,
    _ctx: TeacherContext = Depends(require_teacher),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    course = _course(payload.course_id)
    lesson = section_service.load_lesson(payload.lesson_id, course)
    if not lesson:
        raise HTTPException(status_code=400, detail=f"lesson_id '{payload.lesson_id}' no existe en el curso.")

    section_id = str(payload.moodle_section_id or lesson.get("moodle_section_id") or "").strip()
    if not section_id:
        raise HTTPException(status_code=400, detail="moodle_section_id es requerido para nuevos vínculos.")
    section = await section_service.get_moodle_section(course, section_id, client)
    if not section:
        raise HTTPException(status_code=400, detail="La sección Moodle indicada no existe en el curso.")

    link = db_service.upsert_resource_link(
        resource_id=resource_id,
        lesson_id=payload.lesson_id,
        course_id=course,
        axis_id="",
        moodle_section_id=section_id,
        resource_type=payload.resource_type,
        resource_subtype=payload.resource_subtype,
    )
    return await section_service.enrich_link_with_section(link, client)


@router.delete("/links/{resource_id}")
def remove_link(resource_id: str, _ctx: TeacherContext = Depends(require_teacher)):
    deleted = db_service.delete_resource_link(resource_id)
    return {"deleted": deleted, "resource_id": resource_id}


@router.get("/{section_id}/lessons")
async def get_section_lessons(
    section_id: str,
    _view: TeacherContext = Depends(require_course_view),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    course = _view.course_id
    section = await section_service.get_moodle_section(course, section_id, client)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return {
        "moodle_section_id": section_id,
        "current_section_name": section.get("current_section_name", ""),
        "current_section_order": section.get("current_section_order"),
        "lessons": await section_service.list_lessons_of_section(course, section_id, client),
    }
