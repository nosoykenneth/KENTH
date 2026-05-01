from fastapi import APIRouter
from models.schemas import Consulta
from services.agent_service import super_agente
from services.db_service import get_chat_messages, add_message
import json

router = APIRouter()

@router.post("/chat")
def chat_endpoint(consulta: Consulta):
    
    # Si el botón de React está encendido, bypasseamos al supervisor y forzamos la ruta
    ruta_forzada = "internet" if consulta.usar_internet else ""

    # Extraer historial si viene empaquetado en el contexto o si hay session_id
    historial = []
    contexto = consulta.contexto_leccion
    
    if consulta.session_id:
        db_messages = get_chat_messages(consulta.session_id)
        for msg in db_messages:
            historial.append({"role": msg["role"], "content": msg["content"]})
    else:
        try:
            data_json = json.loads(consulta.contexto_leccion)
            if isinstance(data_json, dict):
                historial = data_json.get("historial", [])
                contexto = data_json.get("context", "")
        except Exception:
            pass

    # Si hay session_id, guardamos el mensaje del usuario
    if consulta.session_id:
        add_message(consulta.session_id, "user", consulta.pregunta, consulta.imagen)

    estado_inicial = {
        "pregunta": f"Contexto actual: {contexto}\n\nPregunta: {consulta.pregunta}",
        "imagen": consulta.imagen,
        "ruta": ruta_forzada, 
        "historial": historial,
        "respuesta_final": ""
    }
    
    # Para no romper el nodo que solo lee "pregunta", inyectamos el contexto aquí
    estado_inicial["pregunta"] = f"[CONTEXTO DEL ALUMNO: {contexto}]\n\n{consulta.pregunta}"
    
    # Si forzamos la ruta, el LangGraph saltará directo a donde le dijimos
    resultado = super_agente.invoke(estado_inicial)
    
    respuesta = resultado["respuesta_final"]

    # Si hay session_id, guardamos el mensaje del asistente
    if consulta.session_id:
        add_message(consulta.session_id, "assistant", respuesta)

    return {"respuesta": respuesta}
