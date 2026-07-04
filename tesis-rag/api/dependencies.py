from fastapi import Header, HTTPException, Depends, Query
from typing import Optional
from services.db_service import (
    get_user_id_from_token,
    using_moodle_db,
    is_course_teacher,
    is_course_admin,
    is_course_reviewer,
    is_course_enrolled_or_visible,
    is_site_admin,
    resolve_course_numeric,
)
from services.moodle_permissions import resolve_course_permissions

SITE_COURSE_ID = "1"  # SITEID de Moodle (contexto de sitio para capabilities globales)


def get_current_user_id(
    authorization: Optional[str] = Header(None),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> str:
    """Extrae y valida la identidad del usuario.

    En producción (Moodle DB activa):
    - Requiere cabecera 'Authorization: Bearer <token>'.
    - Valida el token directamente en la BD de Moodle (mdl_external_tokens).

    En desarrollo local (SQLite fallback):
    - Permite usar X-User-Id directamente si no hay token Moodle disponible.
    """
    # 1. Intentar validar token real de Moodle (producción y desarrollo integrado)
    if authorization and authorization.startswith("Bearer "):
        token = authorization[len("Bearer "):].strip()
        user_id = get_user_id_from_token(token)
        if user_id:
            return user_id

    # 2. Si Moodle está activo, NO se permite fallback. El token es obligatorio.
    if using_moodle_db():
        raise HTTPException(
            status_code=401,
            detail="Autenticación fallida o token inválido. Se requiere Bearer token de Moodle en producción."
        )

    # 3. Solo si NO usamos Moodle (desarrollo local aislado), aceptamos X-User-Id
    dev_uid = (x_dev_user_id or "").strip()
    if dev_uid:
        return dev_uid

    # 4. Sin token ni X-User-Id en dev -> Error
    raise HTTPException(
        status_code=401,
        detail="Usuario no autenticado. Se requiere cabecera Authorization."
    )


class TeacherContext:
    """Identidad + curso validados para acciones de autoría del profesor."""
    def __init__(self, user_id: str, course_id: str, course_raw: str):
        self.user_id = user_id
        self.course_id = course_id      # id canónico (numérico Moodle) para scoping de escritura
        self.course_raw = course_raw    # lo que envió el cliente (puede venir firmado)


def _capability(user_id: str, course_raw: str, flag: str, fallback) -> bool:
    """Resuelve una capability por la WS (fuente de verdad) con fallback por rol.

    La WS `local_tesisai_get_permissions` (has_capability) es la autoridad; si no
    está disponible (dev/offline o no registrada) se cae al fallback por nombre de
    rol de db_service. Sólo se aplica cuando Moodle está activo; en SQLite (dev)
    los guards no bloquean.
    """
    perms = resolve_course_permissions(user_id, course_raw)
    if perms is not None:
        return bool(perms.get(flag))
    return fallback(user_id, course_raw)


def require_course_view(
    authorization: Optional[str] = Header(None),
    x_course_id: Optional[str] = Header(None, alias="X-Course-Id"),
    course_id: Optional[str] = Query(default=None),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> TeacherContext:
    """Exige token válido + poder VER el curso (matrícula / course:view).

    Para lecturas de estructura y recursos del alumno: cierra el acceso anónimo
    sin frenar a estudiantes matriculados. En dev sin Moodle no bloquea.

    El curso se toma de la cabecera `X-Course-Id` (preferente) o, como tolerancia
    de integración, del parámetro de consulta `course_id`. La capability
    `puede_ver_curso` se valida SIEMPRE sobre el curso resuelto: aceptar el query
    NO debilita la autorización (un curso sin acceso sigue devolviendo 403).
    """
    user_id = get_current_user_id(authorization, x_dev_user_id)
    course_raw = (x_course_id or course_id or "").strip()
    if not course_raw:
        raise HTTPException(
            status_code=400,
            detail="Falta el identificador del curso: envía la cabecera 'X-Course-Id' o el parámetro de consulta 'course_id'.",
        )

    if using_moodle_db() and not _capability(user_id, course_raw, "puede_ver_curso", is_course_enrolled_or_visible):
        raise HTTPException(status_code=403, detail="No tienes acceso a este curso.")

    numeric = resolve_course_numeric(course_raw) or course_raw
    return TeacherContext(user_id=user_id, course_id=numeric, course_raw=course_raw)


def require_teacher(
    authorization: Optional[str] = Header(None),
    x_course_id: Optional[str] = Header(None, alias="X-Course-Id"),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> TeacherContext:
    """Exige poder editar PEDAGOGÍA del curso (moodle/course:manageactivities).

    Fuente de verdad: capability `es_profesor` (WS); fallback por rol. El profesor
    SIN edición (non-editing teacher) NO pasa: revisa pero no edita. En desarrollo
    local sin Moodle (SQLite) no bloquea.
    """
    user_id = get_current_user_id(authorization, x_dev_user_id)
    course_raw = (x_course_id or "").strip()
    if not course_raw:
        raise HTTPException(status_code=400, detail="Falta la cabecera X-Course-Id.")

    if using_moodle_db() and not _capability(user_id, course_raw, "es_profesor", is_course_teacher):
        raise HTTPException(
            status_code=403,
            detail="Acción reservada al profesor editor: requiere gestionar el contenido del curso.",
        )

    numeric = resolve_course_numeric(course_raw) or course_raw
    return TeacherContext(user_id=user_id, course_id=numeric, course_raw=course_raw)


def require_course_reviewer(
    authorization: Optional[str] = Header(None),
    x_course_id: Optional[str] = Header(None, alias="X-Course-Id"),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> TeacherContext:
    """Exige poder REVISAR/CALIFICAR la clase (moodle/grade:viewall).

    Incluye al profesor SIN edición (analítica, progreso, probar tutor) además del
    profesor editor / gestor. NO habilita edición. En dev sin Moodle no bloquea.
    """
    user_id = get_current_user_id(authorization, x_dev_user_id)
    course_raw = (x_course_id or "").strip()
    if not course_raw:
        raise HTTPException(status_code=400, detail="Falta la cabecera X-Course-Id.")

    if using_moodle_db() and not _capability(user_id, course_raw, "puede_revisar", is_course_reviewer):
        raise HTTPException(
            status_code=403,
            detail="Acción reservada a docentes: requiere revisar/calificar en este curso.",
        )

    numeric = resolve_course_numeric(course_raw) or course_raw
    return TeacherContext(user_id=user_id, course_id=numeric, course_raw=course_raw)


def require_course_admin(
    authorization: Optional[str] = Header(None),
    x_course_id: Optional[str] = Header(None, alias="X-Course-Id"),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> TeacherContext:
    """Exige rol de ADMIN DEL CURSO (estructura técnica), no solo pedagogía.

    Fuente de verdad: capability `puede_administrar_curso` (moodle/course:update,
    WS); fallback por rol (manager/coursecreator/siteadmin). Gatea el editor
    avanzado: timestamps de bloque, alta/baja/reorden, reindex por curso. Un
    editingteacher "profesor" NO pasa (edita momentos vía el endpoint pedagógico).
    En dev sin Moodle (SQLite) no bloquea.
    """
    user_id = get_current_user_id(authorization, x_dev_user_id)
    course_raw = (x_course_id or "").strip()
    if not course_raw:
        raise HTTPException(status_code=400, detail="Falta la cabecera X-Course-Id.")

    if using_moodle_db() and not _capability(user_id, course_raw, "puede_administrar_curso", is_course_admin):
        raise HTTPException(
            status_code=403,
            detail="Acción reservada al administrador del curso: requiere gestionar la estructura del curso.",
        )

    numeric = resolve_course_numeric(course_raw) or course_raw
    return TeacherContext(user_id=user_id, course_id=numeric, course_raw=course_raw)


def require_rag_admin(
    authorization: Optional[str] = Header(None),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> str:
    """Exige rol de TÉCNICO IA/RAG (site admin) para acciones destructivas o de
    diagnóstico del índice (reindex global de Chroma, validación, trazas técnicas).

    No requiere X-Course-Id: estas acciones son globales del índice. Fuente de
    verdad: capability `es_tecnico_rag` (is_siteadmin) resuelta en el contexto de
    sitio; fallback is_site_admin. En dev sin Moodle (SQLite) no bloquea.
    """
    user_id = get_current_user_id(authorization, x_dev_user_id)
    if using_moodle_db():
        perms = resolve_course_permissions(user_id, SITE_COURSE_ID)
        allowed = perms.get("es_tecnico_rag") if perms is not None else is_site_admin(user_id)
        if not allowed:
            raise HTTPException(
                status_code=403,
                detail="Acción reservada al técnico IA/RAG (site admin).",
            )
    return user_id
