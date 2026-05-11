"""Retest puntual de los 2 casos previamente fallidos."""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent import graph as agent_graph
from services.context_service import build_envelope, render_context_block

CAPTURED = []

class _LLMProxy:
    def __init__(self, real):
        self._real = real
    def invoke(self, prompt, *a, **kw):
        CAPTURED.append(prompt if isinstance(prompt, str) else str(prompt))
        return self._real.invoke(prompt, *a, **kw)
    def bind(self, *a, **kw):
        return _LLMProxy(self._real.bind(*a, **kw))
    def __getattr__(self, name):
        return getattr(self._real, name)

agent_graph.llm_logico = _LLMProxy(agent_graph.llm_logico)

CASES = [
    {"lesson": "E2-L01", "t": 10,  "block": "E2-L01-B1",
     "q": "Como se si eso de abajo es basura o cuerpo real?"},
    {"lesson": "E3-L03", "t": 380, "block": "E3-L03-B6",
     "q": "Esto lo evaluo en solo o en contexto?"},
]

for idx, c in enumerate(CASES, 1):
    CAPTURED.clear()
    envelope = build_envelope(
        question=c["q"],
        raw_activity_context={"current_lesson_id": c["lesson"], "current_timestamp": float(c["t"])},
        session_id=f"retest-{idx}",
        has_image=False,
    )
    activity_block = render_context_block(envelope)
    state = {
        "pregunta": c["q"], "contexto_leccion": "", "imagen": "", "ruta": "",
        "historial": [], "respuesta_final": "", "evidencias": [], "evidence_level": "",
        "intent": "", "answer_type": "", "course_module": "", "evaluation_category": "",
        "requires_course_evidence": True, "warnings": [], "retrieved_chunks": [],
        "trace_id": f"retest-{idx}", "model_used": "", "prompt_id": "",
        "activity_context_block": activity_block, "tutor_envelope": envelope,
    }
    res = agent_graph.super_agente.invoke(state)
    blk = (envelope.pilot_block or {}).get("block_id")
    block_in_prompt = any(
        ("BLOQUE ACTIVO DEL VIDEO (PRIORIDAD MAXIMA)" in p and (blk or "") in p)
        for p in CAPTURED
    )
    print(json.dumps({
        "case": idx,
        "lesson": c["lesson"],
        "timestamp": c["t"],
        "expected_block": c["block"],
        "resolved_block": blk,
        "block_match": blk == c["block"],
        "block_in_prompt": block_in_prompt,
        "intent": res.get("intent"),
        "answer_type": res.get("answer_type"),
        "answer": (res.get("respuesta_final") or "").strip(),
        "n_prompts": len(CAPTURED),
    }, ensure_ascii=False, indent=2))
    print("---")
