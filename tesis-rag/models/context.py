"""
Capa 2 y Capa 3 del tutor contextual.

Capa 1 (conocimiento estable - Ejes 0-7) NO se toca aqui.
Esta capa modela:
    - Capa 2: contexto de la actividad actual (que esta viendo o haciendo el alumno).
    - Capa 3: estado runtime de la sesion del estudiante.

Contratos minimos viables. El backend ya puede aceptarlos, validarlos
y transportarlos al agente. La recuperacion contextual fina por chunks
del recurso quedara cableada en una fase posterior.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ==========================================
# ENUMS
# ==========================================

class ResourceType(str, Enum):
    VIDEO = "video"
    PDF = "pdf"
    WEB_PAGE = "web_page"
    DOWNLOADABLE_FILE = "downloadable_file"
    IMAGE_REFERENCE = "image_reference"
    LESSON_NOTE = "lesson_note"


class InteractionMode(str, Enum):
    """Modo del tutor segun lo que el alumno esta haciendo.

    Vocabulario unico compartido con el editor de leccion
    (INTERACTION_MODES en LessonVideoEditor.jsx): ambos listados
    deben ser identicos.
    """
    TEORIA = "teoria"
    PRACTICA = "practica"
    TROUBLESHOOTING = "troubleshooting"
    REVISION = "revision"
    NAVEGACION_DE_RECURSO = "navegacion_de_recurso"
    CRITERIO_OPERATIVO = "criterio_operativo"


# Alias semantico: el tutor opera en uno de estos modos.
TutorMode = InteractionMode


# ==========================================
# CAPA 2: CONTENIDO ESTRUCTURAL DEL CURSO
# (lecciones y recursos)
# ==========================================

class Resource(BaseModel):
    """Recurso pedagogico individual: video, PDF, pagina web, archivo, etc."""
    resource_id: str
    type: ResourceType
    title: str = ""
    axis_id: str = ""
    moodle_section_id: str = ""
    lesson_id: str = ""
    source_uri: str = ""           # ruta local, URL externa, o id Moodle
    duration_seconds: Optional[int] = None   # solo videos
    page_count: Optional[int] = None         # solo PDFs
    language: str = "es"
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Lesson(BaseModel):
    """Leccion: agrupa recursos bajo una sección Moodle y un objetivo pedagogico."""
    lesson_id: str
    axis_id: str = ""
    moodle_section_id: str = ""
    title: str = ""
    order: int = 0
    learning_goals: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)   # resource_ids
    prerequisites: List[str] = Field(default_factory=list)
    delegated_to_tutor: List[str] = Field(default_factory=list)
    attribution_constraints: List[str] = Field(default_factory=list)
    notes: str = ""   # interno del profesor: nunca se inyecta al tutor


# ==========================================
# CAPA 2: CONTEXTO DE ACTIVIDAD ACTUAL
# (que esta viendo el alumno AHORA)
# ==========================================

class ActivityContext(BaseModel):
    """Snapshot de lo que el alumno esta viendo/haciendo en este momento.

    Este objeto viaja desde el frontend (o Moodle) al backend en cada turno.
    No contiene contenido pesado: solo coordenadas para que el tutor
    pueda decidir como responder y, despues, recuperar el chunk pertinente.
    """
    moodle_section_id: str = ""
    current_lesson_id: str = ""
    current_resource_id: str = ""
    current_resource_type: Optional[ResourceType] = None
    # Subtipo libre para refinar `current_resource_type` sin tocar el enum.
    # Caso de uso principal: H5P se modela como web_page + subtype=h5p_*
    # (h5p_activity, h5p_video, h5p_interactive). Tambien soporta
    # extensiones futuras sin romper compatibilidad.
    resource_subtype: str = ""
    current_timestamp: Optional[float] = None    # segundos, si es video
    current_page: Optional[int] = None           # pagina, si es PDF
    current_section: str = ""                    # encabezado o seccion
    current_section_name: str = ""
    current_section_order: Optional[int] = None
    learning_goal: str = ""
    expected_action: str = ""
    interaction_mode: InteractionMode = InteractionMode.TEORIA

    def is_empty(self) -> bool:
        return not any([
            self.current_lesson_id,
            self.current_resource_id, self.current_section,
            self.moodle_section_id, self.current_section_name,
            self.current_section_order is not None, self.learning_goal
        ])


# ==========================================
# CAPA 2: REFERENCIA A CHUNK DEL RECURSO
# (no se manda el recurso entero al LLM)
# ==========================================

class ResourceChunkReference(BaseModel):
    """Apunta a un fragmento concreto de un recurso (sin embeberlo entero).

    El servicio que materialice este contrato decidira si es:
        - rango de timestamps de un video
        - pagina + offset de un PDF
        - id de chunk en la BD vectorial
    """
    resource_id: str
    chunk_id: str = ""
    locator: Dict[str, Any] = Field(default_factory=dict)   # ej. {"start": 12.0, "end": 47.0}
    text_excerpt: str = ""
    is_neighbor: bool = False
    score: Optional[float] = None


# ==========================================
# CAPA 3: ESTADO RUNTIME DE LA SESION
# ==========================================

class BehavioralSignals(BaseModel):
    """Senales blandas que afectan el comportamiento del tutor."""
    student_seems_lost: bool = False
    student_seems_frustrated: bool = False
    repeated_question: bool = False
    asked_for_simpler_explanation: bool = False
    has_visual_evidence: bool = False


class StudentSessionState(BaseModel):
    """Estado runtime de una sesion del estudiante.

    Persistido en sesion (memoria/DB) por session_id. El backend lo
    actualiza turno a turno. El agente lo recibe como contexto blando.
    """
    session_id: str
    student_id: str = ""
    active_context: Optional[ActivityContext] = None
    last_resource_id: str = ""
    last_concept: str = ""
    last_difficulty: str = ""
    short_history: List[Dict[str, str]] = Field(default_factory=list)   # turnos recientes
    recent_concepts: List[str] = Field(default_factory=list)
    signals: BehavioralSignals = Field(default_factory=BehavioralSignals)
    has_image: bool = False
    updated_at: Optional[str] = None


# ==========================================
# SOBRE EL CONTRATO HACIA EL AGENTE
# ==========================================

class TutorContextEnvelope(BaseModel):
    """Sobre que se entrega al agente junto con la pregunta.

    Es la union limpia de capas 2 y 3. La capa 1 (RAG documental por ejes)
    sigue siendo recuperada por el flujo existente y NO se duplica aqui.
    """
    question: str
    activity_context: ActivityContext = Field(default_factory=ActivityContext)
    session_state: Optional[StudentSessionState] = None
    chunk_references: List[ResourceChunkReference] = Field(default_factory=list)
    interaction_mode: InteractionMode = InteractionMode.TEORIA
    # Lección activa y bloque de video resuelto por timestamp. Cuando
    # están presentes, el agente debe priorizarlos por encima del RAG
    # general del eje. None cuando no hay timestamp o la lección no tiene
    # bloques de video segmentados.
    active_lesson: Optional[Dict[str, Any]] = None
    active_block: Optional[Dict[str, Any]] = None
