from pydantic import BaseModel
from typing import TypedDict

# ==========================================
# EL ESTADO DEL GRAFO (La memoria compartida)
# ==========================================
class EstadoAgente(TypedDict):
    pregunta: str
    imagen: str
    ruta: str # Aquí el supervisor guardará su decisión
    historial: list # Almacena mensajes previos
    respuesta_final: str

# ==========================================
# ESQUEMAS DE LA API
# ==========================================
class Consulta(BaseModel):
    pregunta: str
    contexto_leccion: str = ""
    imagen: str = ""
    usar_internet: bool = False # <--- AQUI ESTA TU NUEVO BOTÓN
    session_id: str = ""
