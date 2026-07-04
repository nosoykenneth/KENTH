"""Endpoints que consumen Moodle via Web Services REST.

La idea es que FastAPI lea informacion de Moodle "core" (usuarios, contenidos del
curso, calificaciones) por contrato REST, no consultando tablas mdl_* directamente.

Estos endpoints son utiles para el tutor contextual (saber en que leccion esta el
estudiante segun Moodle) y como evidencia auditable en el capitulo IV de la tesis.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from api.dependencies import SITE_COURSE_ID, get_current_user_id
from services.moodle_permissions import resolve_course_permissions
from services.moodle_ws_client import MoodleWSClient, MoodleWSError, get_moodle_ws_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/moodle", tags=["moodle"])

# Campos del perfil Moodle que se exponen al propio usuario. Lista blanca: evita
# filtrar campos internos/sensibles que devuelva el WS (preferencias, custom
# fields, etc.). Es el perfil del propio solicitante (/me), no de terceros.
_PROFILE_PUBLIC_FIELDS = (
    "id", "username", "firstname", "lastname", "fullname",
    "email", "department", "institution", "city", "country",
    "profileimageurl", "profileimageurlsmall", "lang",
)


def _pick_profile_fields(profile: dict) -> dict:
    picked = {k: profile.get(k) for k in _PROFILE_PUBLIC_FIELDS if k in profile}
    # Rol efectivo declarado por Moodle (si viene en roles[]) — util para la UI.
    roles = profile.get("roles")
    if isinstance(roles, list) and roles:
        picked["roles"] = [
            {"shortname": r.get("shortname"), "name": r.get("name")}
            for r in roles
            if isinstance(r, dict)
        ]
    return picked


@router.get("/me")
async def get_my_profile(
    user_id: str = Depends(get_current_user_id),
    course_id: Optional[str] = Query(default=None),
    x_course_id: Optional[str] = Header(default=None, alias="X-Course-Id"),
    client: MoodleWSClient = Depends(get_moodle_ws_client),
):
    """Identidad, perfil y capabilities del usuario autenticado.

    Contrato:
    - Token invalido -> 401 (via dependencia).
    - Token valido -> 200 SIEMPRE, con `user_id`, `profile` y `capabilities`.
    - Si el Moodle WS de perfil falla, se degrada de forma controlada
      (`profile: null`, `moodle_ws: "error"`) SIN convertirlo en 500/502: la
      identidad ya esta validada por el token y las capabilities pueden resolverse
      por una WS distinta (server-to-server). Nunca se exponen secretos.

    Las capabilities se resuelven en el contexto del curso indicado (query
    `course_id` o cabecera `X-Course-Id`); si no se indica, se usa el contexto de
    sitio (SITEID) — util para descubrir el rol tecnico/RAG global.
    """
    result: dict = {
        "user_id": user_id,
        "profile": None,
        "capabilities": None,
        "moodle_ws": "unavailable",
    }

    # 1) Perfil via Moodle core WS (best-effort, no debe tumbar el endpoint).
    if client.configured:
        try:
            profile = await client.get_user_by_id(int(user_id))
            if profile:
                result["profile"] = _pick_profile_fields(profile)
                result["moodle_ws"] = "ok"
            else:
                result["moodle_ws"] = "not_found"
        except (ValueError, MoodleWSError) as exc:
            # Error controlado: se registra pero se responde 200 degradado.
            logger.warning(
                "moodle_me_profile_failed",
                extra={"ws_function": "core_user_get_users_by_field", "error": str(exc)},
            )
            result["moodle_ws"] = "error"

    # 2) Capabilities via la WS de permisos (fuente de verdad de autorizacion).
    ctx_course = (course_id or x_course_id or SITE_COURSE_ID or "").strip()
    perms = resolve_course_permissions(user_id, ctx_course)
    if perms is not None:
        result["capabilities"] = perms
        result["capabilities_context"] = ctx_course

    return result


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
