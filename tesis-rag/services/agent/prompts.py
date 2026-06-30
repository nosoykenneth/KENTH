TEXT_MODEL_NAME = "llama3.2:3b"

from services.domain import get_domain_pack

# Fase 0: los prompts por intencion y las reglas comunes viven en el Domain Pack
# (datos en domain_packs/<course_id>.json), no aqui. _PACK resuelve el curso por
# defecto para el piloto mono-curso.
_PACK = get_domain_pack()

PROMPT_COMMON_RULES = _PACK.prompt_common_rules()

PROMPTS_BY_INTENT = _PACK.prompts_by_intent()


def _prompt_info_por_intent(intent: str):
    return PROMPTS_BY_INTENT.get(intent, PROMPTS_BY_INTENT["aclaracion_concepto"])


def _prompt_por_intent(intent: str):
    info = _prompt_info_por_intent(intent)
    return PROMPT_COMMON_RULES + info["text"]


def _prompt_id_por_intent(intent: str):
    return _prompt_info_por_intent(intent)["id"]


def _campos_pedagogicos(state: dict, **overrides):
    data = {
        "intent": state.get("intent", "aclaracion_concepto"),
        "answer_type": state.get("answer_type", "rag_answer"),
        "course_module": state.get("course_module", ""),
        "evaluation_category": state.get("evaluation_category", ""),
        "requires_course_evidence": state.get("requires_course_evidence", True),
        "warnings": list(state.get("warnings", []) or []),
        "retrieved_chunks": list(state.get("retrieved_chunks", []) or []),
        # Observabilidad scope-aware: nivel de contexto que sustenta la respuesta
        # (block/lesson/section/course_global/course/none) y si hubo ampliación
        # de alcance (fallback). Lo setea retrieval._buscar_evidencia sobre `state`.
        "retrieval_scope": state.get("retrieval_scope", ""),
        "retrieval_fallback": bool(state.get("retrieval_fallback", False)),
        "model_used": state.get("model_used", TEXT_MODEL_NAME),
        "prompt_id": state.get("prompt_id", "")
    }
    data.update(overrides)
    if not data.get("prompt_id"):
        data["prompt_id"] = _prompt_id_por_intent(data.get("intent", "aclaracion_concepto"))
    return data
