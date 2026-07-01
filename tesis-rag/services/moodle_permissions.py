"""Resolución de permisos por CAPABILITIES reales de Moodle (fuente de verdad).

Consulta la Web Service `local_tesisai_get_permissions` (definida en el plugin
`local_tesisai`), que devuelve flags derivados de `has_capability` en el contexto
del curso. Es la ÚNICA fuente de verdad de autorización; los guards de FastAPI la
usan y sólo caen al fallback por nombre de rol de `db_service` si la WS no está
disponible (dev/offline o función no registrada aún).

Contrato de flags (igual en la WS y en tesis_role.php):
    puede_ver_curso         moodle/course:view  OR  is_enrolled
    es_profesor             moodle/course:manageactivities   (editing teacher)
    puede_administrar_curso ROL manager/coursecreator        (gestor) — NO course:update,
                            porque el editingteacher tiene course:update por defecto
    puede_revisar           moodle/grade:viewall             (non-editing teacher)
    es_tecnico_rag          is_siteadmin
    es_invitado             acceso guest / sin matrícula
    rol_efectivo            etiqueta derivada (solo UI)

Llamada server-to-server: se usa MOODLE_WS_TOKEN (cuenta de servicio) + `userid`
explícito; la WS exige que el caller sea de confianza para honrar `userid`.
El resultado se cachea con TTL por (userid, course_numeric).
"""

from __future__ import annotations

import threading
import time
from typing import Any, Dict, Optional

import httpx

from config import MOODLE_WS_BASE, MOODLE_WS_TOKEN
from services.db_service import resolve_course_numeric

WS_FUNCTION = "local_tesisai_get_permissions"
_TTL_SECONDS = 60.0
_TIMEOUT = 8.0

_FLAG_KEYS = (
    "puede_ver_curso",
    "es_profesor",
    "puede_administrar_curso",
    "puede_revisar",
    "es_tecnico_rag",
    "es_invitado",
)

_cache: Dict[str, "tuple[float, Dict[str, Any]]"] = {}
_lock = threading.Lock()


def _normalize(payload: Dict[str, Any]) -> Dict[str, Any]:
    perms = {k: bool(payload.get(k)) for k in _FLAG_KEYS}
    perms["rol_efectivo"] = str(payload.get("rol_efectivo", "") or "")
    return perms


def resolve_course_permissions(user_id: str, course_id: str) -> Optional[Dict[str, Any]]:
    """Devuelve los flags de capabilities para (usuario, curso) vía la WS.

    Devuelve None si la WS no está configurada, no responde o lanza excepción;
    en ese caso el guard debe caer al fallback por nombre de rol.
    """
    if not MOODLE_WS_BASE or not MOODLE_WS_TOKEN:
        return None
    if not user_id or not course_id:
        return None
    numeric = resolve_course_numeric(course_id) or str(course_id)
    key = f"{user_id}::{numeric}"

    now = time.monotonic()
    with _lock:
        hit = _cache.get(key)
        if hit and hit[0] > now:
            return hit[1]

    try:
        resp = httpx.post(
            MOODLE_WS_BASE,
            data={
                "wstoken": MOODLE_WS_TOKEN,
                "wsfunction": WS_FUNCTION,
                "moodlewsrestformat": "json",
                "courseid": numeric,
                "userid": user_id,
            },
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception:
        return None

    if not isinstance(payload, dict) or payload.get("exception"):
        return None

    perms = _normalize(payload)
    with _lock:
        _cache[key] = (now + _TTL_SECONDS, perms)
    return perms


def clear_cache() -> None:
    with _lock:
        _cache.clear()


# --- Accesores (nombres alineados con permissions.js del frontend) ---
def can_view_course(perms: Optional[Dict[str, Any]]) -> bool:
    return bool(perms and perms.get("puede_ver_curso"))


def can_edit_pedagogy(perms: Optional[Dict[str, Any]]) -> bool:
    return bool(perms and perms.get("es_profesor"))


def can_admin_course(perms: Optional[Dict[str, Any]]) -> bool:
    return bool(perms and perms.get("puede_administrar_curso"))


def can_review(perms: Optional[Dict[str, Any]]) -> bool:
    return bool(perms and perms.get("puede_revisar"))


def is_rag_admin(perms: Optional[Dict[str, Any]]) -> bool:
    return bool(perms and perms.get("es_tecnico_rag"))
