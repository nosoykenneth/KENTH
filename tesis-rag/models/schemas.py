from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, TypedDict

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
    course_id: str
    current_lesson_id: str
    current_axis_id: str
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
    # Capa 2/3 del tutor contextual: viaja como bloque ya renderizado
    # mas el envelope estructurado por si nodos posteriores lo necesitan.
    activity_context_block: str
    tutor_envelope: Any


# ==========================================
# ESQUEMAS DE LA API
# ==========================================
class Consulta(BaseModel):
    pregunta: str
    contexto_leccion: str = ""
    imagen: str = ""
    usar_internet: bool = False
    session_id: str = ""
    historial: list = Field(default_factory=list)
    source_client: str = ""
    user_id: str = ""
    course_id: str = ""
    lesson_id: str = ""
    # Capa 2: contexto de actividad actual del alumno.
    # Se acepta como dict crudo y se hidrata en el backend via context_service.
    activity_context: Optional[Dict[str, Any]] = None
