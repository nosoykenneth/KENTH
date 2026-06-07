"""
Servicio de contexto del tutor (Capas 2 y 3).

Responsabilidades:
- Cargar lecciones/recursos desde la persistencia operativa Moodle-first.
- Validar e hidratar ActivityContext (Capa 2).
- Mantener StudentSessionState por session_id con persistencia operativa.
- Exponer contratos para recuperar referencias a chunks del recurso
  activo (Capa 2). La materializacion fina queda como TODO; el
  contrato ya es estable.
- Renderizar el contexto activo como bloque de texto que el agente
  inyecta en el prompt SIN contaminar la query de retrieval.

NO toca el RAG documental por ejes (Capa 1).
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from models.context import (
    ActivityContext,
    BehavioralSignals,
    InteractionMode,
    Lesson,
    Resource,
    ResourceChunkReference,
    ResourceType,
    StudentSessionState,
    TutorContextEnvelope,
)
from services import db_service
from services.axis_service import (
    is_known_lesson,
    load_lesson as load_axis_lesson,
    load_resource as load_axis_resource,
    resolve_lesson_block,
)


logger = logging.getLogger(__name__)


# ==========================================
# RUTAS
# ==========================================

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RUNTIME_DIR = os.path.join(_BASE_DIR, "course_runtime")
_RESOURCES_DIR = os.path.join(_RUNTIME_DIR, "resources")
_MANIFEST_FILE = os.path.join(_RUNTIME_DIR, "manifest.json")


# ==========================================
# CARGADORES (Capa 2)
# ==========================================

def load_lesson(lesson_id: str) -> Optional[Lesson]:
    """Devuelve la lección tipada como Pydantic Lesson.

    Resolución: DB → JSON en axes/eje_N/lessons (vía axis_service).
    """
    if not lesson_id:
        return None
    row = db_service.get_lesson(lesson_id)
    if row:
        return Lesson(
            lesson_id=row["lesson_id"],
            axis_id=row.get("axis_id", ""),
            title=row.get("title", ""),
            order=row.get("order", 0),
            learning_goals=row.get("learning_goals", []),
            expected_actions=row.get("expected_actions", []),
            resources=row.get("resources", []),
            prerequisites=row.get("prerequisites", []),
            notes=row.get("notes", ""),
        )
    data = load_axis_lesson(lesson_id)
    if not data:
        return None
    return Lesson(
        lesson_id=data.get("lesson_id", ""),
        axis_id=data.get("axis_id", ""),
        title=data.get("lesson_title") or data.get("title", ""),
        order=data.get("order", 0),
        learning_goals=data.get("learning_goals", []),
        expected_actions=data.get("expected_actions", []),
        resources=data.get("resources", []),
        prerequisites=data.get("prerequisites", []),
        notes=data.get("notes", ""),
    )


def load_resource(resource_id: str) -> Optional[Resource]:
    """Devuelve el recurso tipado como Pydantic Resource."""
    if not resource_id:
        return None
    row = db_service.get_resource(resource_id)
    if row:
        return row
    data = load_axis_resource(resource_id)
    if not data:
        return None
    return Resource(**data)


def load_runtime_manifest() -> dict:
    """Manifest global del curso (DB → JSON)."""
    lessons = db_service.list_lessons()
    if lessons:
        axes: Dict[str, List[str]] = {}
        for lesson in lessons:
            axes.setdefault(lesson.get("axis_id", ""), []).append(lesson.get("lesson_id", ""))
        return {
            "course_id": "curso_mezcla_masterizacion",
            "source": "moodle_db" if db_service.using_moodle_db() else "sqlite_fallback",
            "axes": [
                {"axis_id": axis_id, "lessons": lesson_ids}
                for axis_id, lesson_ids in sorted(axes.items())
                if axis_id
            ],
        }
    if not os.path.exists(_MANIFEST_FILE):
        return {}
    with open(_MANIFEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================
# HIDRATADO DE ActivityContext
# ==========================================

def hydrate_activity_context(raw: Optional[dict]) -> ActivityContext:
    """Convierte payload crudo (frontend/Moodle) en ActivityContext validado.

    Si el frontend manda lesson_id pero no axis_id, se completa desde el
    manifiesto de leccion. Si manda resource_id pero no resource_type,
    se completa desde el manifiesto del recurso.

    Si la lección tiene bloques de video y llega timestamp, hidratamos
    los campos pedagógicos del bloque activo (learning_goal,
    expected_action, interaction_mode, current_section) cuando no
    vengan ya seteados desde el cliente.
    """
    if not raw:
        return ActivityContext()

    ctx = ActivityContext(**raw)

    if ctx.current_lesson_id and not ctx.current_axis:
        lesson = load_lesson(ctx.current_lesson_id)
        if lesson:
            ctx.current_axis = lesson.axis_id

    if ctx.current_resource_id and ctx.current_resource_type is None:
        resource = load_resource(ctx.current_resource_id)
        if resource:
            ctx.current_resource_type = resource.type
            if not ctx.current_axis:
                ctx.current_axis = resource.axis_id

    # Si la lección tiene bloques de video, enriquecemos el ctx
    # desde el bloque activo según el timestamp.
    if is_known_lesson(ctx.current_lesson_id):
        resolved = resolve_lesson_block(ctx.current_lesson_id, ctx.current_timestamp)
        lesson_data = resolved.get("lesson")
        block_data = resolved.get("block")
        if lesson_data:
            if not ctx.current_axis:
                ctx.current_axis = lesson_data.get("axis_id", "")
            if not ctx.current_resource_id:
                ctx.current_resource_id = lesson_data.get("resource_id", "")
            if ctx.current_resource_type is None and lesson_data.get("resource_type"):
                try:
                    ctx.current_resource_type = ResourceType(lesson_data["resource_type"])
                except ValueError:
                    pass
            if not ctx.learning_goal:
                ctx.learning_goal = lesson_data.get("learning_goal", "")
            if not ctx.expected_action:
                ctx.expected_action = lesson_data.get("expected_action", "")
        if block_data:
            if not ctx.current_section:
                ctx.current_section = block_data.get("block_title", "")
            mode_raw = block_data.get("interaction_mode", "")
            try:
                ctx.interaction_mode = InteractionMode(mode_raw)
            except ValueError:
                # interaction_mode del bloque puede ser un valor pedagogico
                # ad-hoc (ej. "criterio_operativo", "corregir_criterio")
                # que no esta en el enum. En ese caso conservamos el modo
                # previo y dejamos el detalle textual en current_section
                # via render_context_block (campo tutor_focus).
                pass

    return ctx


# ==========================================
# ESTADO DE SESION (Capa 3) - en memoria
# ==========================================

_SESSION_STATES: Dict[str, StudentSessionState] = {}


def get_session_state(session_id: str) -> StudentSessionState:
    if not session_id:
        return StudentSessionState(session_id="")
    state = _SESSION_STATES.get(session_id)
    if state is None:
        state = StudentSessionState(session_id=session_id)
        _SESSION_STATES[session_id] = state
    return state


def update_session_state(
    session_id: str,
    *,
    activity_context: Optional[ActivityContext] = None,
    last_concept: Optional[str] = None,
    last_difficulty: Optional[str] = None,
    has_image: Optional[bool] = None,
    short_history: Optional[List[Dict[str, str]]] = None,
    signals: Optional[BehavioralSignals] = None,
) -> StudentSessionState:
    state = get_session_state(session_id)
    if activity_context is not None:
        state.active_context = activity_context
        if activity_context.current_resource_id:
            state.last_resource_id = activity_context.current_resource_id
    if last_concept is not None:
        state.last_concept = last_concept
        if last_concept and last_concept not in state.recent_concepts:
            state.recent_concepts = (state.recent_concepts + [last_concept])[-10:]
    if last_difficulty is not None:
        state.last_difficulty = last_difficulty
    if has_image is not None:
        state.has_image = has_image
        state.signals.has_visual_evidence = has_image
    if short_history is not None:
        state.short_history = short_history[-10:]
    if signals is not None:
        state.signals = signals
    state.updated_at = datetime.utcnow().isoformat()
    if session_id:
        active_context_payload = (
            activity_context.model_dump(mode="json")
            if activity_context is not None
            else (state.active_context.model_dump(mode="json") if state.active_context else {})
        )
        db_service.upsert_session_context(
            session_id,
            student_id=state.student_id,
            active_context=active_context_payload,
            last_resource_id=state.last_resource_id,
            last_concept=state.last_concept,
            last_difficulty=state.last_difficulty,
            recent_concepts=state.recent_concepts,
            signals=state.signals.model_dump(mode="json"),
            has_image=state.has_image,
        )
    return state


# ==========================================
# CHUNKS DEL RECURSO ACTIVO (Capa 2)
# ==========================================

def get_active_chunk_references(
    activity_context: ActivityContext,
    *,
    include_neighbors: bool = True,
    max_neighbors: int = 2,
) -> List[ResourceChunkReference]:
    """Devuelve el chunk actual del recurso activo y, opcionalmente,
    chunks vecinos para anclar al tutor en lo que el alumno esta viendo.

    Por ahora devuelve referencias vacias pero bien formadas: el contrato
    ya viaja por el flujo del agente y solo falta llenar el cuerpo.
    """
    if not activity_context.current_resource_id:
        return []

    locator: Dict[str, object] = {}
    if activity_context.current_timestamp is not None:
        locator["timestamp"] = activity_context.current_timestamp
    if activity_context.current_page is not None:
        locator["page"] = activity_context.current_page
    if activity_context.current_section:
        locator["section"] = activity_context.current_section

    refs: List[ResourceChunkReference] = [
        ResourceChunkReference(
            resource_id=activity_context.current_resource_id,
            chunk_id="",
            locator=locator,
            text_excerpt="",
            is_neighbor=False,
        )
    ]

    if include_neighbors and max_neighbors > 0:
        pass  # Placeholder: chunker fino no implementado todavía.

    return refs


# ==========================================
# RENDER DEL CONTEXTO PARA EL PROMPT
# ==========================================

def render_context_block(envelope: TutorContextEnvelope) -> str:
    """Bloque de texto plano que el agente inyecta como CONTEXTO ACTIVO.

    No es evidencia RAG. No contamina la query vectorial. Solo orienta
    al tutor sobre donde esta parado el alumno y como debe comportarse.

    Para lecciones con bloques de video activos: se inyecta primero un
    bloque "BLOQUE ACTIVO DEL VIDEO" como punto de partida, luego la
    metadata de la leccion, y solo despues el RAG general del eje
    (que sigue llegando como evidencia RAG aparte).
    """
    ctx = envelope.activity_context
    if ctx.is_empty() and not envelope.session_state and not envelope.active_block:
        return ""

    lineas: List[str] = []

    block = envelope.active_block
    lesson_data = envelope.active_lesson
    if block:
        lineas.append("--- BLOQUE ACTIVO DEL VIDEO (PUNTO DE PARTIDA) ---")
        if lesson_data:
            lineas.append(f"Lección: {lesson_data.get('lesson_id', '')} - {lesson_data.get('lesson_title', '')}")
            if lesson_data.get("axis_id"):
                lineas.append(f"Eje de la leccion: {lesson_data.get('axis_id', '')}")
        lineas.append(f"Bloque: {block.get('block_id', '')} - {block.get('block_title', '')}")
        lineas.append(f"Rango: {block.get('start_time', 0)}s - {block.get('end_time', 0)}s")
        if ctx.current_timestamp is not None:
            lineas.append(f"Timestamp del alumno: {ctx.current_timestamp:.1f}s")
        if block.get("summary"):
            lineas.append(f"Que esta pasando en pantalla: {block['summary']}")
        if block.get("interaction_mode"):
            lineas.append(f"Modo pedagogico del bloque: {block['interaction_mode']}")
        if block.get("tutor_focus"):
            lineas.append(f"Foco del tutor en este bloque: {block['tutor_focus']}")
        if block.get("concepts"):
            lineas.append("Conceptos del bloque: " + ", ".join(block["concepts"]))
        if block.get("preguntas_probables"):
            lineas.append("Preguntas probables del alumno aqui:")
            for q in block["preguntas_probables"]:
                lineas.append(f"  - {q}")
        lineas.append(
            "USO DEL BLOQUE: responde primero anclado a este bloque. "
            "La evidencia RAG del eje sirve para fundamentar o ampliar, no para borrar el punto actual. "
            "Las preguntas probables son pistas runtime, no evidencia documental. "
            "Si el alumno pregunta algo mas amplio, puedes conectar con la leccion, el eje actual o ejes previos."
        )
        lineas.append("------------------------")

    lineas.append("--- CONTEXTO ACTIVO DEL ALUMNO (NO ES EVIDENCIA RAG) ---")
    if lesson_data:
        if lesson_data.get("lesson_id") or lesson_data.get("lesson_title"):
            lineas.append(
                f"Leccion activa: {lesson_data.get('lesson_id', '')} - {lesson_data.get('lesson_title', '')}"
            )
        if lesson_data.get("axis_id"):
            lineas.append(f"Axis_id de la leccion activa: {lesson_data.get('axis_id', '')}")
        if lesson_data.get("learning_goal"):
            lineas.append(f"Objetivo de la leccion: {lesson_data.get('learning_goal', '')}")
        if lesson_data.get("expected_action"):
            lineas.append(f"Accion esperada de la leccion: {lesson_data.get('expected_action', '')}")
        if lesson_data.get("proactive_message"):
            lineas.append(f"Mensaje proactivo de la leccion: {lesson_data.get('proactive_message', '')}")
        suggested = lesson_data.get("suggested_prompts") or []
        if suggested:
            lineas.append("Prompts sugeridos de la leccion:")
            for prompt in suggested[:5]:
                lineas.append(f"  - {prompt}")
        metadata = lesson_data.get("metadata") or {}
        constraints = metadata.get("tutor_constraints") or metadata.get("constraints") or metadata.get("restricciones_tutor")
        if constraints:
            lineas.append(f"Restricciones del tutor para esta leccion: {constraints}")
    if ctx.current_axis:
        lineas.append(f"Eje actual: {ctx.current_axis}")
    if ctx.current_lesson_id:
        lineas.append(f"Leccion: {ctx.current_lesson_id}")
    if ctx.current_resource_id:
        rtype = ctx.current_resource_type.value if ctx.current_resource_type else "desconocido"
        if ctx.resource_subtype:
            lineas.append(
                f"Recurso abierto: {ctx.current_resource_id} ({rtype} / {ctx.resource_subtype})"
            )
        else:
            lineas.append(f"Recurso abierto: {ctx.current_resource_id} ({rtype})")
    if ctx.current_timestamp is not None:
        lineas.append(f"Timestamp video: {ctx.current_timestamp:.1f}s")
    if ctx.current_page is not None:
        lineas.append(f"Pagina PDF: {ctx.current_page}")
    if ctx.current_section:
        lineas.append(f"Seccion: {ctx.current_section}")
    if ctx.learning_goal:
        lineas.append(f"Objetivo de aprendizaje: {ctx.learning_goal}")
    if ctx.expected_action:
        lineas.append(f"Accion esperada: {ctx.expected_action}")
    lineas.append(f"Modo de interaccion: {envelope.interaction_mode.value}")

    state = envelope.session_state
    if state:
        if state.last_concept:
            lineas.append(f"Ultimo concepto consultado: {state.last_concept}")
        if state.last_difficulty:
            lineas.append(f"Ultima dificultad detectada: {state.last_difficulty}")
        if state.signals.student_seems_lost:
            lineas.append("Senal: el alumno parece perdido.")
        if state.signals.student_seems_frustrated:
            lineas.append("Senal: el alumno parece frustrado.")

    if envelope.chunk_references:
        lineas.append("Referencias al recurso activo:")
        for ref in envelope.chunk_references:
            loc = ", ".join(f"{k}={v}" for k, v in ref.locator.items()) or "sin locator"
            lineas.append(f"  - {ref.resource_id} [{loc}]")

    lineas.append("Usa este contexto para orientar tu respuesta. Para afirmaciones tecnicas del curso, "
                  "apoyate en EVIDENCIA RAG o en datos runtime explicitamente visibles en este bloque.")
    lineas.append("------------------------")
    return "\n".join(lineas)


# ==========================================
# CONSTRUCTOR DEL ENVELOPE
# ==========================================

def build_envelope(
    *,
    question: str,
    raw_activity_context: Optional[dict],
    session_id: str,
    has_image: bool,
) -> TutorContextEnvelope:
    """Punto unico de entrada: convierte payload crudo en envelope listo
    para el agente, actualiza estado de sesion y arma chunk references.
    """
    ctx = hydrate_activity_context(raw_activity_context)

    state = update_session_state(
        session_id=session_id,
        activity_context=ctx if not ctx.is_empty() else None,
        has_image=has_image,
    )

    chunk_refs = get_active_chunk_references(ctx) if not ctx.is_empty() else []

    # Si la lección tiene bloques de video y hay timestamp, adjuntamos
    # el bloque activo al envelope para que el render lo priorice.
    active_lesson_data = None
    active_block_data = None
    if is_known_lesson(ctx.current_lesson_id):
        resolved = resolve_lesson_block(ctx.current_lesson_id, ctx.current_timestamp)
        active_lesson_data = resolved.get("lesson")
        active_block_data = resolved.get("block")

    return TutorContextEnvelope(
        question=question,
        activity_context=ctx,
        session_state=state if session_id else None,
        chunk_references=chunk_refs,
        interaction_mode=ctx.interaction_mode,
        active_lesson=active_lesson_data,
        active_block=active_block_data,
    )
