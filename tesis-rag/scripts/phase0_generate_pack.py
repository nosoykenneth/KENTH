"""Fase 0 — Generador del Domain Pack de course_id=2 (Mezcla y Masterizacion).

Bootstrap de una sola vez: importa los modulos del agente (post-Pass-1) y vuelca
el conocimiento de dominio a domain_packs/2.json EN VIVO, para garantizar fidelidad
verbatim (sin transcripcion manual, incluido el mojibake). Las respuestas
controladas se extraen llamando a la funcion original con un disparador por regla.

Tras este bootstrap, 2.json es la fuente de verdad editable. NO es runtime.

Uso: python scripts/phase0_generate_pack.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent import routing, prompts, verification
from services.agent import graph as agent_graph
from services.agent import vision as agent_vision

PACK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "domain_packs")

# Reglas de respuestas controladas: (all_of OR-groups, disparador). El termino
# match usa q PADDEADA con espacios (" eq " queda como palabra). El orden replica
# el if/elif de _respuesta_conceptual_controlada. Los textos se EXTRAEN en vivo.
CONTROLLED_RULES = [
    ([["frecuencia"], ["tono"], ["diferencia", "diferencia hay"]], "cual es la diferencia entre frecuencia y tono"),
    ([["espuma"], ["grave", "graves"]], "la espuma sirve para los graves"),
    ([["serie"], ["paralelo"], ["diferencia", "diferencia hay"]], "que diferencia hay entre serie y paralelo"),
    ([["frecuencia de corte"], ["que es", "explicame", "defineme", "define"]], "que es la frecuencia de corte"),
    ([["compresor"], ["que hace", "que es", "para que sirve"]], "que hace un compresor"),
    ([["comprimir", "comprimo", "compresion"], ["ecualizador", "ecualizacion", " eq "]], "como comprimo un ecualizador"),
    ([["master"], ["clipea", "clip"], ["bien"]], "el master no clipea esta bien"),
    ([["revisar en mono"]], "por que revisar en mono"),
    ([["por que"], ["mono"]], "por que revisar en mono"),
    ([["polaridad"], ["invierto", "invertir", "inversion"]], "que es la polaridad y cuando la invierto"),
    ([["mezclar bien"], ["plugin", "plugins", "aplicar"]], "como mezclar bien aplicando plugins a todo"),
    ([["correlacion", "correlaci", "correlator", "correlometro"]], "que es la correlacion"),
]


def _build_controlled_answers():
    out = []
    for all_of, trigger in CONTROLLED_RULES:
        answer = verification._respuesta_conceptual_controlada(trigger)
        if not answer:
            raise RuntimeError(f"El disparador no activo respuesta controlada: {trigger!r}")
        out.append({"all_of": all_of, "answer": answer})
    return out


def build_pack():
    return {
        "domain_id": "mezcla_masterizacion",
        "course_id": "2",
        "description": "Domain Pack del curso Mezcla y Masterizacion (course_id Moodle = 2).",
        "persona": {
            "tutor_name": "KENTH",
            "domain_label": "mezcla y masterizacion",
        },
        "taxonomy": {
            "course_axes": routing.COURSE_AXES,
            "strong_axis_terms": routing.STRONG_AXIS_TERMS,
        },
        "lexicon": {
            "concept_patterns": [[c, list(a)] for c, a in routing.TECHNICAL_CONCEPT_PATTERNS],
            "technical_word_list": list(routing.TECHNICAL_WORD_LIST),
            "domain_hint_terms": list(routing.DOMAIN_HINT_TERMS),
            "lookup_stopwords": sorted(routing.LOOKUP_STOPWORDS),
        },
        "blocklist": {
            "unsupported_terms": list(routing.SPECIFIC_UNSUPPORTED_TERMS),
        },
        "intents": {
            "common_rules": prompts.PROMPT_COMMON_RULES,
            "by_intent": prompts.PROMPTS_BY_INTENT,
            "selection_keywords": [[i, list(kw)] for i, kw in routing.INTENT_SELECTION_KEYWORDS],
        },
        "node_prompts": {
            "rag_system": agent_graph.RAG_SYSTEM_PROMPT,
            "vision_rag_intro": agent_graph.VISION_RAG_INTRO,
            "vision_rag_rules": agent_graph.VISION_RAG_RULES,
            "lost_intro": agent_graph.LOST_INTRO,
            "lost_rules": agent_graph.LOST_RULES,
            "web_query_suffix": agent_graph.WEB_QUERY_SUFFIX,
            "web_intro": agent_graph.WEB_INTRO,
            "web_rules": agent_graph.WEB_RULES,
            "guard_reply": agent_graph.GUARD_REPLY,
            "greetings": agent_graph.GREETINGS,
            "vision_classify": agent_vision.VISION_CLASSIFY_PROMPT,
            "vision_caption": agent_vision.VISION_CAPTION_PROMPT,
            "vision_no_evidence": agent_vision.VISION_NO_EVIDENCE_PROMPT,
        },
        "controlled_answers": _build_controlled_answers(),
    }


def main():
    os.makedirs(PACK_DIR, exist_ok=True)
    pack = build_pack()
    out = os.path.join(PACK_DIR, "2.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
    print(f"Domain Pack escrito en {out}")
    print(f"  axes={len(pack['taxonomy']['course_axes'])} concepts={len(pack['lexicon']['concept_patterns'])} "
          f"intents={len(pack['intents']['by_intent'])} controlled={len(pack['controlled_answers'])}")


if __name__ == "__main__":
    main()
