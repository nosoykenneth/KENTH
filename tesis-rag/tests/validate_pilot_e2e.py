"""
Validacion funcional E2E de la vertical slice piloto.

Ejecuta los 9 casos de prueba contra el flujo real (super_agente),
capturando:
  - lesson_id y current_timestamp enviados
  - pilot_block resuelto por el backend
  - prompt completo que recibe el LLM (intercept)
  - respuesta final del tutor

Requiere Ollama corriendo (TEXT_MODEL).
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar el grafo y monkeypatch del LLM ANTES de invocar.
from services.agent import graph as agent_graph
from services.context_service import build_envelope, render_context_block

CAPTURED_PROMPTS = []

class _LLMProxy:
    def __init__(self, real):
        self._real = real
    def invoke(self, prompt, *args, **kwargs):
        CAPTURED_PROMPTS.append(prompt if isinstance(prompt, str) else str(prompt))
        return self._real.invoke(prompt, *args, **kwargs)
    def bind(self, *args, **kwargs):
        return _LLMProxy(self._real.bind(*args, **kwargs))
    def __getattr__(self, name):
        return getattr(self._real, name)

agent_graph.llm_logico = _LLMProxy(agent_graph.llm_logico)


CASES = [
    {"lesson": "E2-L01", "t": 10,  "block": "E2-L01-B1", "q": "Como se si eso de abajo es basura o cuerpo real?"},
    {"lesson": "E2-L01", "t": 250, "block": "E2-L01-B4", "q": "El HPF se decide en solo o en mezcla?"},
    {"lesson": "E2-L01", "t": 430, "block": "E2-L01-B7", "q": "Pendiente fuerte siempre es mejor?"},
    {"lesson": "E3-L03", "t": 60,  "block": "E3-L03-B2", "q": "Que diferencia hay entre EQ correctivo y EQ estetico?"},
    {"lesson": "E3-L03", "t": 380, "block": "E3-L03-B6", "q": "Esto lo evaluo en solo o en contexto?"},
    {"lesson": "E3-L03", "t": 130, "block": "E3-L03-B3", "q": "El barrido es para dejar el boost o solo para encontrar la zona?"},
    {"lesson": "E4-L01", "t": 120, "block": "E4-L01-B3", "q": "Que hace realmente el threshold?"},
    {"lesson": "E4-L01", "t": 200, "block": "E4-L01-B4", "q": "Ratio alto significa mejor control?"},
    {"lesson": "E4-L01", "t": 270, "block": "E4-L01-B5", "q": "Soft knee siempre es mejor para voz?"},
]


def run_case(case, idx):
    CAPTURED_PROMPTS.clear()
    activity_context = {
        "current_lesson_id": case["lesson"],
        "current_timestamp": float(case["t"]),
    }
    envelope = build_envelope(
        question=case["q"],
        raw_activity_context=activity_context,
        session_id=f"validate-{idx}",
        has_image=False,
    )
    activity_block = render_context_block(envelope)

    state = {
        "pregunta": case["q"],
        "contexto_leccion": "",
        "imagen": "",
        "ruta": "",
        "historial": [],
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
        "trace_id": f"validate-{idx}",
        "model_used": "",
        "prompt_id": "",
        "activity_context_block": activity_block,
        "tutor_envelope": envelope,
    }
    result = agent_graph.super_agente.invoke(state)

    pilot_block_id = (envelope.pilot_block or {}).get("block_id")
    block_in_prompt = any(
        ("BLOQUE ACTIVO DEL VIDEO (PUNTO DE PARTIDA)" in p and (pilot_block_id or "") in p)
        for p in CAPTURED_PROMPTS
    )
    prompt_sample = next(
        (p for p in CAPTURED_PROMPTS if "BLOQUE ACTIVO DEL VIDEO" in p),
        CAPTURED_PROMPTS[0] if CAPTURED_PROMPTS else "",
    )
    return {
        "idx": idx,
        "lesson": case["lesson"],
        "timestamp": case["t"],
        "expected_block": case["block"],
        "resolved_block": pilot_block_id,
        "block_match": pilot_block_id == case["block"],
        "block_in_prompt": block_in_prompt,
        "answer": (result.get("respuesta_final") or "").strip(),
        "ruta": result.get("ruta", ""),
        "intent": result.get("intent", ""),
        "answer_type": result.get("answer_type", ""),
        "evidence_level": result.get("evidence_level", ""),
        "warnings": result.get("warnings", []),
        "n_prompts_captured": len(CAPTURED_PROMPTS),
        "prompt_sample_head": prompt_sample[:1200],
    }


def main():
    out = []
    for idx, c in enumerate(CASES, 1):
        print(f"\n=== CASE {idx}: {c['lesson']} t={c['t']} ===", flush=True)
        try:
            r = run_case(c, idx)
        except Exception as e:
            r = {"idx": idx, "lesson": c["lesson"], "timestamp": c["t"], "error": str(e)}
        out.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "prompt_sample_head"}, ensure_ascii=False, indent=2))

    path = os.path.join(os.path.dirname(__file__), "pilot_validation_report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nReport saved to {path}")


if __name__ == "__main__":
    main()
