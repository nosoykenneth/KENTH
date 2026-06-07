"""Fase 0 — Snapshot DETERMINISTA del comportamiento dependiente de dominio.

Captura, sin invocar LLM ni Chroma, la salida de TODAS las funciones del agente
que consumen conocimiento de dominio (routing, prompts, verificacion, scoring de
retrieval) sobre un corpus fijo, mas las constantes crudas. Sirve como gate de
regresion para la extraccion al Domain Pack: el snapshot ANTES y DESPUES del
refactor debe ser byte-identico para course_id=2.

Uso:
    python scripts/phase0_snapshot.py <ruta_salida.json>
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document

from services.agent import routing, prompts, verification, retrieval
from services.agent import graph as agent_graph
from services.agent import vision as agent_vision


# ==========================================
# CORPUS FIJO (no cambiar entre baseline y after)
# ==========================================

CORPUS = [
    "quien es napoleon",
    "que es el headroom",
    "como comprimo un ecualizador",
    "diferencia entre compresion y ecualizacion",
    "diferencia entre filtro y ecualizacion",
    "que es la frecuencia de corte",
    "que es el factor q",
    "en que modulo hablan de frecuencia de corte",
    "en que minuto reviso el gain staging",
    "que pdf tengo que leer sobre headroom",
    "eso cuando conviene",
    "y eso",
    "que es eso",
    "a cuantos db",
    "no entiendo nada me rindo",
    "explicame desde cero",
    "necesito plugins de serum y wavetable",
    "como uso ableton para masterizar",
    "que es la sintesis fm",
    "cual es la diferencia entre frecuencia y tono",
    "el master no clipea esta bien",
    "por que revisar en mono",
    "que es la correlacion",
    "como mezclar bien aplicando plugins a todo",
    "que diferencia hay entre serie y paralelo",
    "como controlo el hiss y el doubling en los toms",
    "que es 0 vu y dbfs y el overhead",
    "tengo bleed y resonancia en la compuerta gate",
    "la espuma sirve para los graves",
    "que reverb uso para dar profundidad",
    "como hago el mastering para streaming con lufs",
    "que es la polaridad y cuando la invierto",
    "que relacion tiene la espuma con la interfaz",
    "puedo ecualizar con mis audios ya procesados",
    "que recurso reviso para entender compresion paralela",
    "que es en serie y en paralelo",
    "que hace un compresor",
    "hola",
    "gracias",
    "ok",
    # Una por eje (terminos fuertes) para ejercitar _eje_fuerte_pregunta / categoria
    "curvas isofonicas sala acustica resonadores",
    "gain staging headroom fader trim clip gain flujo de senal",
    "polaridad fase mono monocompatibilidad correlacion estereo",
    "frecuencia de corte filtro pendiente factor q eq",
    "compresor compresion threshold ratio ataque release dinamica",
    "reverb delay espacialidad profundidad ambiencia",
    "mezcla integradora criterio de mezcla jerarquia contexto",
    "mastering lufs limitador streaming normalizacion",
]

HISTORIAL_FIJO = [
    {"role": "user", "content": "que es la compresion paralela"},
    {"role": "assistant", "content": "La compresion paralela mezcla la senal comprimida con la original."},
]

# Chunks sinteticos para ejercitar el scoring (_prioridad_evidencia) sin Chroma.
SYNTH_CHUNKS = [
    {
        "page_content": "La frecuencia de corte se define como el punto de transicion del filtro. tabla criterio",
        "metadata": {
            "filename": "E3_guia_canonica.md", "doc_type": "markdown",
            "axis": "Eje 3", "axis_id": "Eje 3", "layer": "canonico",
            "topic": "filtros", "lesson_id": "E3-L01", "course_id": "2",
            "scope": "lesson", "resource_title": "guia canonica eje 3",
        },
    },
    {
        "page_content": "El compresor controla la dinamica con threshold ratio ataque release. en serie y en paralelo",
        "metadata": {
            "filename": "E4_glosario.json", "doc_type": "json",
            "axis": "Eje 4", "axis_id": "Eje 4", "layer": "limpio",
            "topic": "dinamica", "lesson_id": "E4-L02", "course_id": "2",
            "scope": "axis", "resource_title": "glosario eje 4",
        },
    },
    {
        "page_content": "Conocimiento universal de mezcla y escucha critica.",
        "metadata": {
            "filename": "global_leeme.txt", "doc_type": "texto",
            "axis": "", "axis_id": "", "layer": "general",
            "topic": "", "lesson_id": "", "course_id": "",
            "scope": "global", "is_global": True, "resource_title": "",
        },
    },
    {
        "page_content": "Ruteo de bus auxiliar y envios para reverb. faq ruteo",
        "metadata": {
            "filename": "E1_faq.json", "doc_type": "json",
            "axis": "Eje 1", "axis_id": "Eje 1", "layer": "general",
            "topic": "ruteo", "lesson_id": "E1-L03", "course_id": "2",
            "scope": "lesson", "resource_title": "faq eje 1",
        },
    },
]

SYNTH_STATES = [
    {"course_id": "2", "current_axis_id": "Eje 3", "current_lesson_id": "E3-L01"},
    {"course_id": "2", "current_axis_id": "Eje 4", "current_lesson_id": ""},
    {"course_id": "2", "current_axis_id": "", "current_lesson_id": ""},
]

SYNTH_EVIDENCIAS = [
    {"document": Document(page_content=c["page_content"], metadata=dict(c["metadata"])), "score": 0.5}
    for c in SYNTH_CHUNKS
]


def _r(value):
    """Redondea floats para evitar ruido de repr; deja el resto intacto."""
    if isinstance(value, float):
        return round(value, 10)
    if isinstance(value, tuple):
        return [_r(v) for v in value]
    if isinstance(value, list):
        return [_r(v) for v in value]
    return value


def build_snapshot():
    snap = {}

    # --- Constantes crudas ---
    snap["constants"] = {
        "routing.COURSE_AXES": routing.COURSE_AXES,
        "routing.STRONG_AXIS_TERMS": routing.STRONG_AXIS_TERMS,
        "routing.TECHNICAL_CONCEPT_PATTERNS": [[c, list(a)] for c, a in routing.TECHNICAL_CONCEPT_PATTERNS],
        "routing.SPECIFIC_UNSUPPORTED_TERMS": list(routing.SPECIFIC_UNSUPPORTED_TERMS),
        "routing.LOOKUP_STOPWORDS": sorted(routing.LOOKUP_STOPWORDS),
        "routing.AMBIGUOUS_MAX_WORDS": routing.AMBIGUOUS_MAX_WORDS,
        "retrieval.SPECIFIC_UNSUPPORTED_TERMS": list(retrieval.SPECIFIC_UNSUPPORTED_TERMS),
        "retrieval.CURRENT_AXIS_BOOST": _r(retrieval.CURRENT_AXIS_BOOST),
        "retrieval.PREVIOUS_AXIS_SUPPORT_BOOST": _r(retrieval.PREVIOUS_AXIS_SUPPORT_BOOST),
        "retrieval.FUTURE_AXIS_DEFAULT_PENALTY": _r(retrieval.FUTURE_AXIS_DEFAULT_PENALTY),
        "retrieval.FUTURE_AXIS_REQUESTED_BOOST": _r(retrieval.FUTURE_AXIS_REQUESTED_BOOST),
        "retrieval.MIN_RELEVANCE_SCORE": _r(retrieval.MIN_RELEVANCE_SCORE),
        "retrieval.RETRIEVAL_K": retrieval.RETRIEVAL_K,
        "prompts.PROMPT_COMMON_RULES": prompts.PROMPT_COMMON_RULES,
        "prompts.PROMPTS_BY_INTENT": prompts.PROMPTS_BY_INTENT,
    }

    # --- Prompts de nodo (graph.py / vision.py) ---
    snap["node_prompts"] = {
        "graph.RAG_SYSTEM_PROMPT": agent_graph.RAG_SYSTEM_PROMPT,
        "graph.VISION_RAG_INTRO": agent_graph.VISION_RAG_INTRO,
        "graph.VISION_RAG_RULES": agent_graph.VISION_RAG_RULES,
        "graph.LOST_INTRO": agent_graph.LOST_INTRO,
        "graph.LOST_RULES": agent_graph.LOST_RULES,
        "graph.WEB_QUERY_SUFFIX": agent_graph.WEB_QUERY_SUFFIX,
        "graph.WEB_INTRO": agent_graph.WEB_INTRO,
        "graph.WEB_RULES": agent_graph.WEB_RULES,
        "graph.GUARD_REPLY": agent_graph.GUARD_REPLY,
        "graph.GREETINGS": agent_graph.GREETINGS,
        "vision.VISION_CLASSIFY_PROMPT": agent_vision.VISION_CLASSIFY_PROMPT,
        "vision.VISION_CAPTION_PROMPT": agent_vision.VISION_CAPTION_PROMPT,
        "vision.VISION_NO_EVIDENCE_PROMPT": agent_vision.VISION_NO_EVIDENCE_PROMPT,
    }

    # --- Prompts por intent (todas) ---
    snap["prompts_por_intent"] = {
        intent: {
            "text": prompts._prompt_por_intent(intent),
            "id": prompts._prompt_id_por_intent(intent),
        }
        for intent in prompts.PROMPTS_BY_INTENT.keys()
    }

    # --- Funciones puras de routing/verification/retrieval sobre el corpus ---
    snap["por_pregunta"] = {}
    for q in CORPUS:
        snap["por_pregunta"][q] = {
            "normalizar": routing._normalizar_texto(q),
            "eje_fuerte": routing._eje_fuerte_pregunta(q),
            "inferir_modulo_categoria": list(routing._inferir_modulo_categoria(q)),
            "clasificacion_pedagogica": routing._clasificacion_pedagogica(q),
            "es_estudiante_perdido": routing._es_estudiante_perdido(q),
            "es_pregunta_lookup": routing._es_pregunta_lookup(q),
            "es_pregunta_ambigua": routing._es_pregunta_ambigua(q),
            "es_pregunta_conceptual_directa": routing._es_pregunta_conceptual_directa(q),
            "tiene_termino_tecnico": routing._tiene_termino_tecnico_curso(q),
            "conceptos_relevantes": routing._conceptos_relevantes_pregunta(q),
            "conceptos_en_texto": routing._conceptos_en_texto(q),
            "parece_dominio": routing._parece_consulta_del_dominio_curso(q),
            "tokens_lookup": routing._tokens_lookup(q),
            "resolver_referente_ambiguo": list(routing._resolver_referente_ambiguo(q, HISTORIAL_FIJO)),
            # verification
            "respuesta_conceptual_controlada": verification._respuesta_conceptual_controlada(q),
            # retrieval (puras)
            "query_aliases": retrieval._query_retrieval_con_aliases(q),
            "concepto_definicion_directa": retrieval._concepto_definicion_directa(q),
            "comparativa_multiconcepto": retrieval._es_pregunta_comparativa_multiconcepto(q),
            "extraer_frases_lookup": list(retrieval._extraer_frases_lookup(q)),
            "terminos_no_soportados": retrieval._terminos_especificos_no_soportados(q, SYNTH_EVIDENCIAS),
        }

    # --- Scoring del re-ranker (_prioridad_evidencia) sobre matriz pregunta x chunk x state ---
    snap["scoring"] = {}
    for q in CORPUS:
        for si, state in enumerate(SYNTH_STATES):
            for ci, chunk in enumerate(SYNTH_CHUNKS):
                item = {
                    "document": Document(page_content=chunk["page_content"], metadata=dict(chunk["metadata"])),
                    "score": 0.5,
                }
                key = f"q={q}|s={si}|c={ci}"
                snap["scoring"][key] = _r(retrieval._prioridad_evidencia(item, q, state))

    return snap


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/phase0_snapshot.py <ruta_salida.json>")
        sys.exit(1)
    out = sys.argv[1]
    snap = build_snapshot()
    with open(out, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"Snapshot escrito en {out}")
    print(f"  preguntas={len(snap['por_pregunta'])} scoring_keys={len(snap['scoring'])} intents={len(snap['prompts_por_intent'])}")


if __name__ == "__main__":
    main()
