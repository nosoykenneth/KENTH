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
from services.lesson_service import (
    is_known_lesson,
    load_lesson as load_axis_lesson,
    load_resource as load_axis_resource,
    resolve_lesson_block,
)


logger = logging.getLogger(__name__)


def _fmt_mmss(seconds) -> str:
    """Segundos -> 'm:ss' humano. Devuelve '' si no es numérico.

    Se usa para que el CONTEXTO inyectado no exponga tiempos crudos (start_time=0)
    ni invite al tutor a hablar en segundos; el alumno piensa en minutos del video.
    """
    try:
        total = int(float(seconds))
    except (TypeError, ValueError):
        return ""
    if total < 0:
        total = 0
    return f"{total // 60}:{total % 60:02d}"


def _fmt_rango(start, end) -> str:
    """Rango 'm:ss–m:ss' humano para ubicar el momento en el video."""
    ini = _fmt_mmss(start)
    fin = _fmt_mmss(end)
    if not ini and not fin:
        return ""
    return f"{ini}–{fin}"


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

    Resolución: DB → JSON en axes/eje_N/lessons (vía lesson_service).
    """
    if not lesson_id:
        return None
    row = db_service.get_lesson(lesson_id)
    if row:
        return Lesson(
            lesson_id=row["lesson_id"],
            axis_id=row.get("axis_id", ""),
            moodle_section_id=row.get("moodle_section_id", ""),
            title=row.get("title", ""),
            order=row.get("order", 0),
            learning_goals=row.get("learning_goals", []),
            resources=row.get("resources", []),
            prerequisites=row.get("prerequisites", []),
            delegated_to_tutor=row.get("delegated_to_tutor", []),
            attribution_constraints=row.get("attribution_constraints", []),
            notes=row.get("notes", ""),
        )
    data = load_axis_lesson(lesson_id)
    if not data:
        return None
    return Lesson(
        lesson_id=data.get("lesson_id", ""),
        axis_id=data.get("axis_id", ""),
        moodle_section_id=data.get("moodle_section_id", ""),
        title=data.get("lesson_title") or data.get("title", ""),
        order=data.get("order", 0),
        learning_goals=data.get("learning_goals", []),
        resources=data.get("resources", []),
        prerequisites=data.get("prerequisites", []),
        delegated_to_tutor=data.get("delegated_to_tutor", []),
        attribution_constraints=data.get("attribution_constraints", []),
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

    if ctx.current_lesson_id and not ctx.moodle_section_id:
        lesson = load_lesson(ctx.current_lesson_id)
        if lesson:
            if not ctx.moodle_section_id:
                ctx.moodle_section_id = lesson.moodle_section_id

    if ctx.current_resource_id and ctx.current_resource_type is None:
        resource = load_resource(ctx.current_resource_id)
        if resource:
            ctx.current_resource_type = resource.type
            if not ctx.moodle_section_id:
                ctx.moodle_section_id = resource.moodle_section_id

    # Si la lección tiene bloques de video, enriquecemos el ctx
    # desde el bloque activo según el timestamp.
    if is_known_lesson(ctx.current_lesson_id):
        resolved = resolve_lesson_block(ctx.current_lesson_id, ctx.current_timestamp)
        lesson_data = resolved.get("lesson")
        block_data = resolved.get("block")
        if lesson_data:
            if not ctx.moodle_section_id:
                ctx.moodle_section_id = lesson_data.get("moodle_section_id", "")
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
            if mode_raw:
                try:
                    ctx.interaction_mode = InteractionMode(mode_raw)
                except ValueError:
                    # Vocabulario roto: el bloque trae un modo que no existe en
                    # InteractionMode. Es un error de datos (el editor y el enum
                    # deben compartir vocabulario) y se reporta fuerte, nunca se
                    # conserva el modo previo en silencio.
                    logger.error(
                        "interaction_mode desconocido '%s' en bloque %s de la leccion %s; "
                        "valores validos: %s",
                        mode_raw,
                        block_data.get("block_id", ""),
                        ctx.current_lesson_id,
                        [m.value for m in InteractionMode],
                    )

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

    # Para de-duplicar objetivo/accion: el mismo dato viaja en lesson_data y se
    # hidrata tambien en ctx (hydrate_activity_context). Registramos lo que ya se
    # inyecto desde la leccion para no repetirlo con otra etiqueta (regla 12).
    objetivo_leccion_inyectado = ""
    accion_leccion_inyectada = ""

    block = envelope.active_block
    lesson_data = envelope.active_lesson
    if block:
        # Encabezado técnico (interno): NO exponemos block_id/lesson_id/section_id como
        # texto; el tutor podría repetirlos. Usamos títulos y tiempos humanizados.
        lineas.append("--- BLOQUE ACTIVO DEL VIDEO (PUNTO DE PARTIDA) ---")
        if lesson_data:
            if lesson_data.get("lesson_title"):
                lineas.append(f"Lección: {lesson_data.get('lesson_title', '')}")
            # La sección SÍ se mantiene como dato de grounding (contrato de retrieval);
            # lo que se quita es el block_id/lesson_id que el tutor podría verbalizar.
            if lesson_data.get("section_name") or lesson_data.get("moodle_section_id"):
                lineas.append(
                    f"Sección del curso: {lesson_data.get('section_name', '')} "
                    f"(moodle_section_id={lesson_data.get('moodle_section_id', '')})"
                )
        if block.get("block_title"):
            lineas.append(f"Parte actual de la lección: {block.get('block_title', '')}")
        rango = _fmt_rango(block.get("start_time"), block.get("end_time"))
        if rango:
            lineas.append(f"Ubicación en el video: {rango}")
        if ctx.current_timestamp is not None:
            lineas.append(f"Momento del alumno en el video: {_fmt_mmss(ctx.current_timestamp)}")
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
            "La evidencia RAG de la seccion sirve para fundamentar o ampliar, no para borrar el punto actual. "
            "Las preguntas probables son pistas runtime, no evidencia documental. "
            "Si el alumno pregunta algo mas amplio, puedes conectar con la leccion, la seccion actual o secciones previas."
        )
        lineas.append("------------------------")

    lineas.append("--- CONTEXTO ACTIVO DEL ALUMNO (NO ES EVIDENCIA RAG) ---")
    if lesson_data:
        if lesson_data.get("lesson_title"):
            lineas.append(f"Leccion activa: {lesson_data.get('lesson_title', '')}")
        if lesson_data.get("section_name") or lesson_data.get("moodle_section_id"):
            lineas.append(
                f"Seccion activa: {lesson_data.get('section_name', '')} "
                f"(moodle_section_id={lesson_data.get('moodle_section_id', '')})"
            )
        if lesson_data.get("learning_goal"):
            objetivo_leccion_inyectado = lesson_data.get("learning_goal", "")
            lineas.append(f"Objetivo de la leccion: {objetivo_leccion_inyectado}")
        criterios = lesson_data.get("learning_goals") or []
        if criterios:
            lineas.append("Criterios de logro de la leccion:")
            for criterio in criterios:
                lineas.append(f"  - {criterio}")
        prerequisitos = lesson_data.get("prerequisites") or []
        if prerequisitos:
            lineas.append(
                "Prerrequisitos de la leccion (si el alumno muestra lagunas, "
                "puedes remitirlo a estas lecciones previas): " + ", ".join(prerequisitos)
            )
        if lesson_data.get("expected_action"):
            accion_leccion_inyectada = lesson_data.get("expected_action", "")
            lineas.append(f"Accion esperada de la leccion: {accion_leccion_inyectada}")
        delegado = lesson_data.get("delegated_to_tutor") or []
        if delegado:
            lineas.append("Delegado al tutor en esta leccion (el profesor te encarga cubrir esto):")
            for item in delegado:
                lineas.append(f"  - {item}")
        if lesson_data.get("proactive_message"):
            lineas.append(f"Mensaje proactivo de la leccion: {lesson_data.get('proactive_message', '')}")
        suggested = lesson_data.get("suggested_prompts") or []
        if suggested:
            lineas.append("Prompts sugeridos de la leccion:")
            for prompt in suggested[:5]:
                lineas.append(f"  - {prompt}")
        atribuciones = lesson_data.get("attribution_constraints") or []
        if atribuciones:
            lineas.append(
                "RESTRICCIONES Y ATRIBUCIONES (OBLIGATORIAS): cumple estas reglas "
                "en TODAS tus respuestas de esta leccion. No son contexto informativo, "
                "son normas de comportamiento:"
            )
            for regla in atribuciones:
                lineas.append(f"  - {regla}")
        # Personalizacion pedagogica que el profesor definio para esta leccion
        # (metadata.pedagogy). Inyeccion ADITIVA y condicional: si el campo no
        # existe, no se emite nada (no rompe el gate de dominio ni contamina la
        # query vectorial; solo orienta el comportamiento del tutor).
        pedagogia = (lesson_data.get("metadata") or {}).get("pedagogy") or {}
        if pedagogia.get("lesson_summary"):
            lineas.append(f"Resumen de la leccion (para orientar, no es evidencia): {pedagogia['lesson_summary']}")
        if pedagogia.get("tutor_tone"):
            lineas.append(f"Tono del tutor solicitado por el profesor: {pedagogia['tutor_tone']}")
        if pedagogia.get("help_level"):
            lineas.append(
                f"Nivel de ayuda esperado en esta leccion: {pedagogia['help_level']} "
                "(ajusta cuanto guias vs cuanto resuelves)."
            )
        if pedagogia.get("lesson_rules"):
            lineas.append(f"Reglas de la leccion (definidas por el profesor): {pedagogia['lesson_rules']}")
        errores = pedagogia.get("common_mistakes") or []
        if errores:
            lineas.append("Errores comunes a vigilar y prevenir en esta leccion:")
            for err in errores:
                lineas.append(f"  - {err}")
    if ctx.current_section_name:
        lineas.append(f"Seccion actual: {ctx.current_section_name}")
    if ctx.current_section_order is not None:
        if ctx.current_section_order >= 2:
            lineas.append(f"Numero de seccion (por orden, base 0): {ctx.current_section_order - 2}")
        elif ctx.current_section_order == 1:
            lineas.append("Es la seccion de bienvenida (no cuenta como seccion pedagogica).")
    if ctx.current_resource_id:
        # No emitimos el id del recurso (cmid): solo su tipo, en lenguaje humano.
        rtype = ctx.current_resource_type.value if ctx.current_resource_type else "desconocido"
        if ctx.resource_subtype:
            lineas.append(f"Recurso abierto: {rtype} / {ctx.resource_subtype}")
        else:
            lineas.append(f"Recurso abierto: {rtype}")
    if ctx.current_timestamp is not None:
        lineas.append(f"Momento del video: {_fmt_mmss(ctx.current_timestamp)}")
    if ctx.current_page is not None:
        lineas.append(f"Pagina PDF: {ctx.current_page}")
    if ctx.current_section:
        lineas.append(f"Seccion: {ctx.current_section}")
    # Solo inyectamos el objetivo/accion de ctx si AÑADEN algo distinto a lo ya
    # inyectado desde la leccion (evita la doble inyeccion del mismo dato).
    if ctx.learning_goal and ctx.learning_goal.strip().casefold() != objetivo_leccion_inyectado.strip().casefold():
        lineas.append(f"Objetivo de aprendizaje: {ctx.learning_goal}")
    if ctx.expected_action and ctx.expected_action.strip().casefold() != accion_leccion_inyectada.strip().casefold():
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
    lineas.append("No menciones identificadores internos (codigos de bloque, de leccion o de seccion) en tu "
                  "respuesta; refierete a 'esta parte de la leccion', 'este momento del video' o al titulo del momento.")
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
