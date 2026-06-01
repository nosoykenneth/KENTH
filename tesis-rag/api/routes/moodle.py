"""Endpoints que consumen Moodle via Web Services REST.

La idea es que FastAPI lea informacion de Moodle "core" (usuarios, contenidos del
curso, calificaciones) por contrato REST, no consultando tablas mdl_* directamente.

Estos endpoints son utiles para el tutor contextual (saber en que leccion esta el
estudiante segun Moodle) y como evidencia auditable en el capitulo IV de la tesis.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_current_user_id
from services.moodle_ws_client import MoodleWSClient, MoodleWSError, get_moodle_ws_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/moodle", tags=["moodle"])


@router.get("/me")
async def get_my_profile(
    user_id: str = Depends(get_current_user_id),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    """Perfil del usuario autenticado, obtenido via Moodle WS."""
    if not client.configured:
        raise HTTPException(status_code=503, detail="Moodle Web Services no configurado")
    try:
        profile = await client.get_user_by_id(int(user_id))
    except (ValueError, MoodleWSError) as exc:
        logger.warning("moodle_ws_failed", extra={"function": "core_user_get_users_by_field", "error": str(exc)})
        raise HTTPException(status_code=502, detail=str(exc))
    if not profile:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en Moodle")
    return profile


@router.get("/courses/{course_id}/contents")
async def get_course_contents(
    course_id: int,
    _user_id: str = Depends(get_current_user_id),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    """Contenido del curso (secciones + modulos) tal como Moodle lo entrega."""
    if not client.configured:
        raise HTTPException(status_code=503, detail="Moodle Web Services no configurado")
    try:
        return await client.get_course_contents(course_id)
    except MoodleWSError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/courses/{course_id}/grades")
async def get_my_grades(
    course_id: int,
    user_id: str = Depends(get_current_user_id),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    """Calificaciones del usuario autenticado en el curso."""
    if not client.configured:
        raise HTTPException(status_code=503, detail="Moodle Web Services no configurado")
    try:
        return await client.get_user_grades(int(user_id), course_id)
    except (ValueError, MoodleWSError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/courses/{course_id}/completion")
async def get_my_completion(
    course_id: int,
    user_id: str = Depends(get_current_user_id),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    """Progreso de actividades completadas por el usuario en el curso."""
    if not client.configured:
        raise HTTPException(status_code=503, detail="Moodle Web Services no configurado")
    try:
        return await client.get_activity_completion(int(user_id), course_id)
    except (ValueError, MoodleWSError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))
