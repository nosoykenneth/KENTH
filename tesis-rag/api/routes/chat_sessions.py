"""
Endpoints de sesiones de chat con control de acceso por usuario.

REGLA DE PRIVACIDAD: ningún endpoint devuelve datos sin verificar
que el usuario autenticado es dueño de la sesión/mensajes solicitados.
El user_id se extrae de la cabecera X-User-Id que inyecta la capa de
autenticación (Moodle web service token → plugin PHP → proxy).
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional
from api.dependencies import get_current_user_id
from services.db_service import (
    create_chat,
    get_user_chats,
    delete_chat,
    get_chat_messages,
    verify_session_ownership,
)

router = APIRouter(prefix="/chat-sessions", tags=["Chat Sessions"])


# ==========================================
# HELPERS DE AUTENTICACIÓN
# ==========================================

# _require_user_id fue reemplazado por api.dependencies.get_current_user_id
# para validación segura de tokens contra Moodle DB en producción.


def _require_ownership(session_id: str, user_id: str) -> None:
    """Verifica que session_id pertenece a user_id. 403 si no."""
    if not verify_session_ownership(session_id, user_id):
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a esta sesión.",
        )


# ==========================================
# SCHEMAS
# ==========================================

class CreateChatRequest(BaseModel):
    title: str = "Nuevo Chat"


# ==========================================
# ENDPOINTS
# ==========================================

@router.post("/")
def api_create_chat(
    request: CreateChatRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Crea una sesión nueva propiedad del usuario autenticado."""
    try:
        chat = create_chat(user_id, request.title)
        return {"success": True, "chat": chat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def api_get_my_chats(
    user_id: str = Depends(get_current_user_id),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Lista SOLO las sesiones del usuario autenticado, con paginación."""
    try:
        chats = get_user_chats(user_id, limit=limit, offset=offset)
        return {"success": True, "chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id_param}")
def api_get_user_chats_legacy(
    user_id_param: str,
    user_id: str = Depends(get_current_user_id),
):
    """LEGACY — redirige a la lista filtrada del usuario autenticado.

    El user_id del path se ignora; solo se usa el validado
    para evitar que un atacante enumere sesiones de otros usuarios.
    """
    try:
        chats = get_user_chats(user_id)
        return {"success": True, "chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chat_id}/messages")
def api_get_chat_messages(
    chat_id: str,
    user_id: str = Depends(get_current_user_id),
    limit: int = Query(default=50, ge=1, le=500),
):
    """Devuelve mensajes SOLO si el usuario autenticado es dueño de la sesión."""
    _require_ownership(chat_id, user_id)
    try:
        messages = get_chat_messages(chat_id, limit=limit)
        return {"success": True, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{chat_id}")
def api_delete_chat(
    chat_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Elimina una sesión SOLO si el usuario autenticado es dueño."""
    _require_ownership(chat_id, user_id)
    try:
        success = delete_chat(chat_id)
        if success:
            return {"success": True, "message": "Chat eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Chat no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
