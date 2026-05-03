from pydantic import BaseModel
from typing import TypedDict

# ==========================================
# ESTADO DEL GRAFO
# ==========================================
class EstadoAgente(TypedDict, total=False):
    pregunta: str
    contexto_leccion: str
    imagen: str
    ruta: str
    historial: list
    evidencias: list
    evidence_level: str
    respuesta_final: str
    intent: str
    answer_type: str
    course_module: str
    evaluation_category: str
    requires_course_evidence: bool
    warnings: list
    retrieved_chunks: list
    trace_id: str
    model_used: str
    prompt_id: str


# ==========================================
# ESQUEMAS DE LA API
# ==========================================
class Consulta(BaseModel):
    pregunta: str
    contexto_leccion: str = ""
    imagen: str = ""
    usar_internet: bool = False
    session_id: str = ""
    source_client: str = ""
    course_id: str = ""
    lesson_id: str = ""
