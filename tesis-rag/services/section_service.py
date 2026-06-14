"""Servicios de secciones Moodle como fuente de verdad del Tutor IA.

Las secciones provienen de `core_course_get_contents`. La base local solo guarda
asociaciones operativas (lecciones, links, documentos) usando `moodle_section_id`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from services import db_service
from services.lesson_service import load_lesson as _legacy_load_lesson
from services.lesson_service import resolve_lesson_block
from services.moodle_ws_client import MoodleWSClient, get_moodle_ws_client
from services.moodle_ws_client import MoodleWSError


def _normalize_section(raw: Dict[str, Any], order: int) -> Dict[str, Any]:
    section_id = str(raw.get("id") or raw.get("sectionid") or raw.get("section") or "")
    section_number = raw.get("section")
    return {
        "moodle_section_id": section_id,
        "section_id": section_id,
        "section_number": section_number if section_number is not None else order,
        "section_order": order,
        "current_section_order": order,
        "section_name": raw.get("name") or raw.get("title") or f"Tema {order}",
        "current_section_name": raw.get("name") or raw.get("title") or f"Tema {order}",
        "summary": raw.get("summary") or "",
        "visible": raw.get("visible", 1),
        "modules": raw.get("modules") or [],
        "raw": raw,
    }


def resolve_course_id(course_id: str) -> str:
    """Normaliza el course_id que llega desde React.

    El frontend puede enviar el id Moodle real o el id firmado de la capa PHP.
    Para Moodle WS y para leer tablas core necesitamos el id numerico.
    """
    value = str(course_id or "").strip()
    return db_service.resolve_course_numeric(value) or value


def _list_sections_from_db(course_id: str) -> List[Dict[str, Any]]:
    """Fallback local: lee las secciones desde la BD core de Moodle.

    Esto permite que `/sections/*` funcione en desarrollo aunque Moodle Web
    Services no este configurado, siempre que el backend tenga acceso a la BD.
    """
    numeric_course_id = resolve_course_id(course_id)
    if not numeric_course_id or not numeric_course_id.isdigit() or not db_service.using_moodle_db():
        return []
    table = db_service._moodle_table("course_sections")
    q = db_service._q()
    with db_service.get_connection() as conn:
        rows = db_service._fetchall(
            conn,
            f"""
            SELECT id, course, section, name, summary, visible
            FROM {table}
            WHERE course = {q}
            ORDER BY section ASC
            """,
            (numeric_course_id,),
        )
    return [_normalize_section({**row, "modules": []}, idx + 1) for idx, row in enumerate(rows)]


async def list_moodle_sections(
    course_id: str,
    client: Optional[MoodleWSClient] = None,
) -> List[Dict[str, Any]]:
    ws = client or get_moodle_ws_client()
    numeric_course_id = resolve_course_id(course_id)
    if getattr(ws, "configured", False):
        try:
            contents = await ws.get_course_contents(int(numeric_course_id))
            return [_normalize_section(section, idx + 1) for idx, section in enumerate(contents or [])]
        except (MoodleWSError, ValueError):
            fallback = _list_sections_from_db(numeric_course_id)
            if fallback:
                return fallback
            raise
    return _list_sections_from_db(numeric_course_id)


async def get_moodle_section(
    course_id: str,
    moodle_section_id: str,
    client: Optional[MoodleWSClient] = None,
) -> Optional[Dict[str, Any]]:
    target = str(moodle_section_id or "")
    for section in await list_moodle_sections(course_id, client):
        if str(section.get("moodle_section_id") or "") == target:
            return section
    return None


def _with_section_fields(
    item: Dict[str, Any],
    section: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    out = dict(item or {})
    if section:
        out["moodle_section_id"] = str(section.get("moodle_section_id") or out.get("moodle_section_id") or "")
        out["current_section_name"] = section.get("current_section_name") or section.get("section_name") or ""
        out["current_section_order"] = section.get("current_section_order") or section.get("section_order")
    else:
        out.setdefault("current_section_name", "")
        out.setdefault("current_section_order", None)
    return out


async def list_lessons_of_section(
    course_id: str,
    moodle_section_id: str,
    client: Optional[MoodleWSClient] = None,
) -> List[Dict[str, Any]]:
    numeric_course_id = resolve_course_id(course_id)
    section = await get_moodle_section(numeric_course_id, moodle_section_id, client)
    rows = db_service.list_lessons(course_id=numeric_course_id, moodle_section_id=str(moodle_section_id))
    return [_with_section_fields(row, section) for row in rows]


async def list_all_lessons(
    course_id: str,
    client: Optional[MoodleWSClient] = None,
) -> List[Dict[str, Any]]:
    numeric_course_id = resolve_course_id(course_id)
    sections = await list_moodle_sections(numeric_course_id, client)
    by_id = {str(s.get("moodle_section_id") or ""): s for s in sections}
    rows = db_service.list_lessons(course_id=numeric_course_id)
    rows.sort(key=lambda row: (
        by_id.get(str(row.get("moodle_section_id") or ""), {}).get("section_order", 9999),
        int(row.get("order") or 0),
        row.get("lesson_id") or "",
    ))
    return [_with_section_fields(row, by_id.get(str(row.get("moodle_section_id") or ""))) for row in rows]


def load_lesson(lesson_id: str, course_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    return _legacy_load_lesson(lesson_id, course_id)


async def resolve_section_for_lesson(
    course_id: str,
    lesson_id: str,
    client: Optional[MoodleWSClient] = None,
) -> Optional[Dict[str, Any]]:
    numeric_course_id = resolve_course_id(course_id)
    lesson = load_lesson(lesson_id, numeric_course_id)
    section_id = str((lesson or {}).get("moodle_section_id") or "")
    if not section_id:
        return None
    return await get_moodle_section(numeric_course_id, section_id, client)


async def resolve_section_for_resource(
    course_id: str,
    resource_id: str,
    client: Optional[MoodleWSClient] = None,
) -> Optional[Dict[str, Any]]:
    numeric_course_id = resolve_course_id(course_id)
    link = db_service.get_resource_link(resource_id) or {}
    section_id = str(link.get("moodle_section_id") or "")
    if not section_id and link.get("lesson_id"):
        lesson = load_lesson(str(link.get("lesson_id")), numeric_course_id)
        section_id = str((lesson or {}).get("moodle_section_id") or "")
    if not section_id:
        return None
    return await get_moodle_section(numeric_course_id, section_id, client)


async def enrich_link_with_section(
    link: Dict[str, Any],
    client: Optional[MoodleWSClient] = None,
) -> Dict[str, Any]:
    course_id = str((link or {}).get("course_id") or "")
    section_id = str((link or {}).get("moodle_section_id") or "")
    section = None
    if course_id and section_id:
        section = await get_moodle_section(course_id, section_id, client)
    return _with_section_fields(link, section)
