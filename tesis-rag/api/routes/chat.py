from fastapi import APIRouter
from models.schemas import Consulta
from services.agent_service import super_agente
from services.db_service import get_chat_messages, add_message, save_trace, save_interaction_trace
import json
import time
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/chat")
def chat_endpoint(consulta: Consulta):
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

    # Extraer historial si viene empaquetado en el contexto o si hay session_id.
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

    # Si hay session_id, guardamos el mensaje del usuario.
    if consulta.session_id:
        add_message(consulta.session_id, "user", consulta.pregunta, consulta.imagen)

    # Fase 1: la pregunta queda limpia para retrieval.
    # El contexto de leccion viaja separado para que el agente lo use como pista,
    # pero no contamine la query vectorial.
    estado_inicial = {
        "pregunta": consulta.pregunta,
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
        "prompt_id": ""
    }

    resultado = super_agente.invoke(estado_inicial)

    respuesta = resultado["respuesta_final"]

    # AUDIT FIX #1: Extraer trazas del resultado del grafo.
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
        "warnings": warnings
    }

    save_interaction_trace(trace_id=trace_id, session_id=consulta.session_id, trace_data=trace_data)

    # Si hay session_id, guardamos el mensaje del asistente y su traza.
    if consulta.session_id:
        msg = add_message(consulta.session_id, "assistant", respuesta)
        # AUDIT FIX #5: Persistir traza RAG asociada al mensaje.
        save_trace(
            message_id=msg["id"],
            ruta=ruta,
            evidence_level=evidence_level,
            fuentes=fuentes,
            trace_data=trace_data,
            trace_id=trace_id
        )

    # AUDIT FIX #1: Devolver campos adicionales sin romper compatibilidad.
    # El frontend solo lee "respuesta", los campos nuevos son opcionales.
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
        "trace_id": trace_id,
        "prompt_id": prompt_id
    }
