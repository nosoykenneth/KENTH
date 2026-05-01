from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.db_service import create_chat, get_user_chats, delete_chat, get_chat_messages

router = APIRouter(prefix="/chat-sessions", tags=["Chat Sessions"])

class CreateChatRequest(BaseModel):
    user_id: str
    title: str = "Nuevo Chat"

@router.post("/")
def api_create_chat(request: CreateChatRequest):
    try:
        chat = create_chat(request.user_id, request.title)
        return {"success": True, "chat": chat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
def api_get_user_chats(user_id: str):
    try:
        chats = get_user_chats(user_id)
        return {"success": True, "chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chat_id}/messages")
def api_get_chat_messages(chat_id: str):
    try:
        messages = get_chat_messages(chat_id)
        return {"success": True, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{chat_id}")
def api_delete_chat(chat_id: str):
    try:
        success = delete_chat(chat_id)
        if success:
            return {"success": True, "message": "Chat eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Chat no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
