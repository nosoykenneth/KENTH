from fastapi import Header, HTTPException, Depends
from typing import Optional
from services.db_service import get_user_id_from_token, using_moodle_db

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
