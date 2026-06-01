from fastapi import Header, HTTPException, Depends
from typing import Optional
from services.db_service import (
    get_user_id_from_token,
    using_moodle_db,
    is_course_teacher,
    resolve_course_numeric,
)

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


def require_teacher(
    authorization: Optional[str] = Header(None),
    x_course_id: Optional[str] = Header(None, alias="X-Course-Id"),
    x_dev_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> TeacherContext:
    """Exige que el usuario sea docente/gestor del curso indicado en X-Course-Id.

    Reusa la verdad de Moodle (roles en el contexto del curso). En desarrollo
    local sin Moodle (SQLite) no bloquea, para no frenar el desarrollo.
    """
    user_id = get_current_user_id(authorization, x_dev_user_id)
    course_raw = (x_course_id or "").strip()
    if not course_raw:
        raise HTTPException(status_code=400, detail="Falta la cabecera X-Course-Id.")

    if using_moodle_db() and not is_course_teacher(user_id, course_raw):
        raise HTTPException(
            status_code=403,
            detail="Acción reservada al profesor: requiere rol docente/gestor en este curso.",
        )

    numeric = resolve_course_numeric(course_raw) or course_raw
    return TeacherContext(user_id=user_id, course_id=numeric, course_raw=course_raw)
