from fastapi import APIRouter, Header, Depends
from typing import Optional
from api.dependencies import get_current_user_id
from models.schemas import Consulta
from services.agent_service import super_agente
from services.context_service import build_envelope, render_context_block
from services.db_service import (
    get_chat_messages,
    add_message,
    save_trace,
    save_interaction_trace,
    ensure_chat_exists,
    resolve_course_numeric,
)
import json
import time
import uuid
from datetime import datetime

router = APIRouter()


def _normalizar_historial(raw_historial, max_messages: int = 10):
    if not isinstance(raw_historial, list):
        return []

    normalizado = []
    anterior = None
    for msg in raw_historial:
        if not isinstance(msg, dict):
            continue
        role = msg.get("role")
        content = msg.get("content")
        if role not in ("user", "assistant"):
            continue
        if not isinstance(content, str):
            continue
        content = content.strip()
        if not content:
            continue

        item = {"role": role, "content": content}
        if item == anterior:
            continue
        normalizado.append(item)
        anterior = item

    return normalizado[-max_messages:]


@router.post("/chat")
def chat_endpoint(
    consulta: Consulta,
    user_id: str = Depends(get_current_user_id),
):
    trace_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    started = time.perf_counter()

    # Si el boton de React esta encendido, forzamos la ruta de internet.
    ruta_forzada = "internet" if consulta.usar_internet else ""
    print(
        "[CHAT DEBUG] request",
        {
            "has_image": bool(consulta.imagen),
            "image_len": len(consulta.imagen or ""),
            "has_session": bool(consulta.session_id),
            "question_len": len(consulta.pregunta or "")
        }
    )

    # Extraer historial por prioridad: DB de sesion, payload directo, o contexto legacy.
    historial = _normalizar_historial(consulta.historial)
    contexto = consulta.contexto_leccion

    if consulta.session_id:
        db_messages = get_chat_messages(consulta.session_id)
        historial_db = _normalizar_historial([
            {"role": msg["role"], "content": msg["content"]}
            for msg in db_messages
        ])
        if historial_db:
            historial = historial_db

    if not historial:
        try:
            data_json = json.loads(consulta.contexto_leccion)
            if isinstance(data_json, dict):
                historial = _normalizar_historial(data_json.get("historial", []))
                contexto = data_json.get("context", "")
        except Exception:
            pass

    # Si hay session_id, aseguramos que la sesion exista antes de guardar mensajes.
    # El user_id REAL viene del token Moodle validado (o fallback dev).
    # El payload user_id se ignora totalmente por seguridad.
    authenticated_user_id = user_id.strip()
    if consulta.session_id:
        source_client = (consulta.source_client or "").strip().lower()
        user_for_session = authenticated_user_id or (f"{source_client}_user" if source_client else "system")
        title_hint = "Chat Moodle" if source_client == "moodle" else "Chat auto-creado"

        ensure_chat_exists(
            chat_id=consulta.session_id,
            user_id=user_for_session,
            title=title_hint
        )
        add_message(consulta.session_id, "user", consulta.pregunta, consulta.imagen, user_id=user_for_session)

    # Capa 2/3: hidrata contexto de actividad y estado de sesion sin
    # contaminar la query vectorial. El bloque renderizado se inyecta
    # al prompt como CONTEXTO ACTIVO; el envelope completo viaja en el
    # estado por si nodos posteriores lo necesitan (recuperacion contextual).
    envelope = build_envelope(
        question=consulta.pregunta,
        raw_activity_context=consulta.activity_context,
        session_id=consulta.session_id,
        has_image=bool(consulta.imagen),
    )
    activity_context_block = render_context_block(envelope)
    runtime_context_trace = {
        "has_activity_context": not envelope.activity_context.is_empty(),
        "current_axis": envelope.activity_context.current_axis,
        "current_lesson_id": envelope.activity_context.current_lesson_id,
        "current_resource_id": envelope.activity_context.current_resource_id,
        "current_timestamp": envelope.activity_context.current_timestamp,
        "current_page": envelope.activity_context.current_page,
        "active_lesson_id": (envelope.active_lesson or {}).get("lesson_id", ""),
        "active_block_id": (envelope.active_block or {}).get("block_id", ""),
        "runtime_source_category": "B_RUNTIME_CONTEXT" if activity_context_block else "",
    }

    # Fase 1: la pregunta queda limpia para retrieval.
    # El contexto de leccion viaja separado para que el agente lo use como pista,
    # pero no contamine la query vectorial.
    scoped_course_id = resolve_course_numeric(consulta.course_id) or consulta.course_id
    estado_inicial = {
        "pregunta": consulta.pregunta,
        "course_id": scoped_course_id,
        "contexto_leccion": contexto,
        "imagen": consulta.imagen,
        "ruta": ruta_forzada,
        "historial": historial,
        "respuesta_final": "",
        "evidencias": [],
        "evidence_level": "",
        "intent": "",
        "answer_type": "",
        "course_module": "",
        "evaluation_category": "",
        "requires_course_evidence": True,
        "warnings": [],
        "retrieved_chunks": [],
        "trace_id": trace_id,
        "model_used": "",
        "prompt_id": "",
        "activity_context_block": activity_context_block,
        "tutor_envelope": envelope,
    }

    resultado = super_agente.invoke(estado_inicial)

    respuesta = resultado["respuesta_final"]

    fuentes = resultado.get("evidencias", [])
    evidence_level = resultado.get("evidence_level", "")
    ruta = resultado.get("ruta", "")
    intent = resultado.get("intent", "")
    answer_type = resultado.get("answer_type", "")
    course_module = resultado.get("course_module", "")
    evaluation_category = resultado.get("evaluation_category", "")
    requires_course_evidence = resultado.get("requires_course_evidence", True)
    warnings = resultado.get("warnings", [])
    retrieved_chunks = resultado.get("retrieved_chunks", [])
    model_used = resultado.get("model_used", "")
    prompt_id = resultado.get("prompt_id", "")
    latency_ms_total = int((time.perf_counter() - started) * 1000)

    trace_data = {
        "trace_id": trace_id,
        "timestamp": timestamp,
        "session_id": consulta.session_id,
        "source_client": consulta.source_client,
        "user_id": authenticated_user_id,
        "course_id": consulta.course_id,
        "lesson_id": consulta.lesson_id,
        "pregunta": consulta.pregunta,
        "has_image": bool(consulta.imagen),
        "usar_internet": consulta.usar_internet,
        "intent": intent,
        "answer_type": answer_type,
        "course_module": course_module,
        "evaluation_category": evaluation_category,
        "requires_course_evidence": requires_course_evidence,
        "evidence_level": evidence_level,
        "retrieved_chunks": retrieved_chunks,
        "scores": [chunk.get("score") for chunk in retrieved_chunks if isinstance(chunk, dict)],
        "fuentes_finales": fuentes,
        "ruta": ruta,
        "modelo_usado": model_used,
        "prompt_id": prompt_id,
        "latencia_total_ms": latency_ms_total,
        "warnings": warnings,
        "runtime_context": runtime_context_trace,
        "source_policy": {
            "A_INDEXED_RAG": bool(retrieved_chunks),
            "B_RUNTIME_CONTEXT": bool(activity_context_block),
            "C_SYSTEM_RULES": True,
        }
    }

    save_interaction_trace(trace_id=trace_id, session_id=consulta.session_id, trace_data=trace_data)

    # Si hay session_id, guardamos el mensaje del asistente y su traza.
    if consulta.session_id:
        msg = add_message(consulta.session_id, "assistant", respuesta, user_id=authenticated_user_id)
        save_trace(
            message_id=msg["id"],
            ruta=ruta,
            evidence_level=evidence_level,
            fuentes=fuentes,
            trace_data=trace_data,
            trace_id=trace_id
        )

    return {
        "respuesta": respuesta,
        "answer_type": answer_type,
        "intent": intent,
        "course_module": course_module,
        "evaluation_category": evaluation_category,
        "fuentes": fuentes,
        "evidence_level": evidence_level,
        "ruta": ruta,
        "warnings": warnings,
        "runtime_context": runtime_context_trace,
        "source_policy": trace_data["source_policy"],
        "trace_id": trace_id,
        "prompt_id": prompt_id
    }
