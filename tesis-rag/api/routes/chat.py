from fastapi import APIRouter
from models.schemas import Consulta
from services.agent_service import super_agente

router = APIRouter()

@router.post("/chat")
def chat_endpoint(consulta: Consulta):
    
    # Si el botón de React está encendido, bypasseamos al supervisor y forzamos la ruta
    ruta_forzada = "internet" if consulta.usar_internet else ""

    estado_inicial = {
        "pregunta": consulta.pregunta,
        "imagen": consulta.imagen,
        "ruta": ruta_forzada, 
        "respuesta_final": ""
    }
    
    # Si forzamos la ruta, el LangGraph saltará directo a donde le dijimos
    resultado = super_agente.invoke(estado_inicial)
    
    return {"respuesta": resultado["respuesta_final"]}
