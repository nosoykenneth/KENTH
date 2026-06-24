#!/usr/bin/env python
"""
run_tutor_eval.py — Evaluacion de calidad del tutor IA (OE4: precision MEDIBLE).

Ejecuta los casos de `tutor_eval_set.jsonl` contra el tutor y calcula metricas
defendibles para la tesis. Dos modos:

  --mode mock  (por defecto)  No necesita Ollama ni Chroma. Usa el ROUTING
      DETERMINISTA REAL del agente (services.agent.routing.nodo_supervisor) para
      predecir el COMPORTAMIENTO (responder / rechazar / pedir mas contexto). Es
      la capa mas critica para la defensa (compuertas de dominio/ambiguedad) y
      corre en cualquier maquina. Las metricas de CONTENIDO (uso de fuentes,
      no-alucinacion, no-afirmar-analisis-de-audio, latencia) requieren modo real.

  --mode real  Invoca el agente COMPLETO (super_agente.invoke) por caso, igual
      que el endpoint /chat. Requiere Ollama corriendo (y, para fuentes, el indice
      Chroma del corpus). Calcula TODAS las metricas + latencia.

Salida: imprime un resumen y guarda un JSON en evaluation/results/. Con --out
guarda ademas en la ruta indicada (se usa para el ejemplo versionado).

Uso:
  python evaluation/run_tutor_eval.py                         # mock
  python evaluation/run_tutor_eval.py --mode real --course-id 2
  python evaluation/run_tutor_eval.py --mode mock --out evaluation/results/example_results.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# Permite importar `services...` al correr desde tesis-rag/ o desde evaluation/.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_ROOT = os.path.dirname(_THIS_DIR)
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

EVAL_SET = os.path.join(_THIS_DIR, "tutor_eval_set.jsonl")
RESULTS_DIR = os.path.join(_THIS_DIR, "results")

# Comportamientos validos del tutor.
RESPOND = "respond"
REJECT = "reject"
ASK = "ask_more_context"

# Heuristica de no-alucinacion: nombres propios de DAW/sintes que el tutor NO debe
# inventar si no estan en la evidencia (espejo del blocklist del Domain Pack).
FORBIDDEN_TOOL_NAMES = [
    "ableton", "fl studio", "logic pro", "cubase", "pro tools", "reaper",
    "serum", "massive", "sylenth", "vital", "kontakt",
]

# Frases que delatan que el tutor FINGE haber escuchado/analizado el audio.
AUDIO_CLAIM_MARKERS = [
    "escuche tu", "escuché tu", "al escuchar tu", "cuando escuche", "he escuchado",
    "escuchando tu", "oi tu", "oí tu", "al oir", "al oír", "analice el audio",
    "analicé el audio", "analizando tu audio", "tras escuchar", "ya escuche",
    "tu audio suena", "tu mezcla suena", "tu master suena", "tu máster suena",
]


def _norm(text: str) -> str:
    return (text or "").strip().lower()


def load_cases(path: str) -> list:
    cases = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))
    return cases


# ==========================================================================
# MODO MOCK — routing determinista real, sin Ollama/Chroma
# ==========================================================================

def predict_behavior_mock(question: str) -> dict:
    """Predice el comportamiento usando el supervisor REAL (sin LLM ni retrieval).

    El clasificador LLM de routing solo actua en la "zona incierta" y aqui no esta
    configurado, asi que el supervisor cae a su rama determinista (bloqueo seguro
    para contenido ajeno). Es exactamente lo que queremos validar offline.
    """
    from services.agent.routing import nodo_supervisor, _es_pregunta_ambigua

    state = {"pregunta": question, "contexto_leccion": "", "imagen": "", "ruta": ""}
    out = nodo_supervisor(state)
    ruta = out.get("ruta", "")
    if ruta == "bloqueo":
        behavior = REJECT
    elif ruta == "teoria" and _es_pregunta_ambigua(question):
        behavior = ASK
    else:
        behavior = RESPOND
    return {
        "behavior": behavior,
        "route": ruta,
        "blocked_by": out.get("blocked_by", ""),
        "intent": out.get("intent", ""),
        "answer": None,
        "sources_count": None,
        "latency_ms": None,
        "error": "",
    }


# ==========================================================================
# MODO REAL — agente completo (requiere Ollama)
# ==========================================================================

def _build_state_real(case: dict, course_id: str):
    from services.context_service import build_envelope, render_context_block
    from services.db_service import resolve_course_numeric

    question = case["question"]
    envelope = build_envelope(
        question=question,
        raw_activity_context=case.get("activity_context"),
        session_id="",
        has_image=False,
    )
    scoped_course = resolve_course_numeric(course_id) or course_id
    return {
        "pregunta": question,
        "course_id": scoped_course,
        "current_lesson_id": envelope.activity_context.current_lesson_id,
        "moodle_section_id": envelope.activity_context.moodle_section_id,
        "current_section_name": envelope.activity_context.current_section_name,
        "current_section_order": envelope.activity_context.current_section_order,
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
        "trace_id": "eval",
        "model_used": "",
        "prompt_id": "",
        "activity_context_block": render_context_block(envelope),
        "tutor_envelope": envelope,
    }


def run_real(case: dict, course_id: str) -> dict:
    from services.agent_service import super_agente

    state = _build_state_real(case, course_id)
    t0 = time.perf_counter()
    try:
        result = super_agente.invoke(state)
    except Exception as exc:  # Ollama caido / error de red: no tumbamos la corrida.
        return {
            "behavior": "error", "route": "", "blocked_by": "", "intent": "",
            "answer": None, "sources_count": None,
            "latency_ms": int((time.perf_counter() - t0) * 1000), "error": str(exc),
        }
    latency_ms = int((time.perf_counter() - t0) * 1000)

    answer = result.get("respuesta_final", "") or ""
    answer_type = result.get("answer_type", "")
    blocked_by = result.get("blocked_by", "")
    intent = result.get("intent", "")
    fuentes = result.get("evidencias", []) or []

    if blocked_by or answer_type == "out_of_domain":
        behavior = REJECT
    elif answer_type == "clarification" or intent == "ambigua":
        behavior = ASK
    else:
        # needs_more_context = el tutor SI responde (declara que no hay evidencia);
        # no es ni rechazo de dominio ni pedido de desambiguar un referente.
        behavior = RESPOND

    return {
        "behavior": behavior,
        "route": result.get("ruta", ""),
        "blocked_by": blocked_by,
        "intent": intent,
        "answer": answer,
        "answer_type": answer_type,
        "sources_count": len(fuentes),
        "latency_ms": latency_ms,
        "error": "",
    }


# ==========================================================================
# Chequeos de contenido (solo aplican en modo real, cuando hay texto)
# ==========================================================================

def check_no_audio_claim(answer: str) -> bool:
    a = _norm(answer)
    return not any(marker in a for marker in AUDIO_CLAIM_MARKERS)


def check_no_hallucinated_tool(answer: str) -> bool:
    a = _norm(answer)
    return not any(name in a for name in FORBIDDEN_TOOL_NAMES)


def check_used_sources(observed: dict) -> bool:
    return bool(observed.get("sources_count"))


# ==========================================================================
# Scoring + metricas
# ==========================================================================

def score_case(case: dict, observed: dict, mode: str) -> dict:
    expected = case["expected_behavior"]
    behavior_ok = observed["behavior"] == expected

    row = {
        "id": case["id"],
        "category": case["category"],
        "weight": case.get("weight", 1),
        "expected_behavior": expected,
        "observed_behavior": observed["behavior"],
        "behavior_ok": behavior_ok,
        "route": observed.get("route", ""),
        "blocked_by": observed.get("blocked_by", ""),
        "latency_ms": observed.get("latency_ms"),
        "error": observed.get("error", ""),
        # Chequeos de contenido: None en mock (no hay texto).
        "no_audio_claim": None,
        "no_hallucinated_tool": None,
        "used_sources": None,
    }

    if mode == "real" and observed.get("answer") is not None:
        if case.get("must_not_claim_audio_analysis"):
            row["no_audio_claim"] = check_no_audio_claim(observed["answer"])
        # No-alucinacion aplica a respuestas (no a rechazos limpios).
        if observed["behavior"] == RESPOND:
            row["no_hallucinated_tool"] = check_no_hallucinated_tool(observed["answer"])
        if case.get("requires_sources"):
            row["used_sources"] = check_used_sources(observed)

    return row


def _rate(values: list):
    vals = [v for v in values if isinstance(v, bool)]
    if not vals:
        return None
    return round(sum(1 for v in vals if v) / len(vals), 4)


def aggregate(cases: list, rows: list, mode: str) -> dict:
    n = len(rows)
    behavior_oks = [r["behavior_ok"] for r in rows]
    behavior_accuracy = round(sum(1 for b in behavior_oks if b) / n, 4) if n else None

    # Accuracy ponderada por severidad.
    tot_w = sum(r["weight"] for r in rows) or 1
    weighted = round(sum(r["weight"] for r in rows if r["behavior_ok"]) / tot_w, 4)

    by_case = {c["id"]: c for c in cases}

    def subset(pred):
        return [r for r in rows if pred(by_case[r["id"]])]

    reject_rows = subset(lambda c: c["expected_behavior"] == REJECT)
    ask_rows = subset(lambda c: c["expected_behavior"] == ASK)
    oos_rows = subset(lambda c: c.get("should_reject_out_of_scope"))

    metrics = {
        "behavior_accuracy": behavior_accuracy,
        "behavior_accuracy_weighted": weighted,
        "correct_rejection_rate": _rate([r["behavior_ok"] for r in reject_rows]),
        "out_of_scope_blocked_rate": _rate([r["observed_behavior"] == REJECT for r in oos_rows]),
        "ask_more_context_accuracy": _rate([r["behavior_ok"] for r in ask_rows]),
        "non_hallucination_rate": _rate([r["no_hallucinated_tool"] for r in rows]),
        "source_usage_rate": _rate([r["used_sources"] for r in rows]),
        "audio_claim_avoidance_rate": _rate([r["no_audio_claim"] for r in rows]),
    }

    latencies = [r["latency_ms"] for r in rows if isinstance(r.get("latency_ms"), int) and not r.get("error")]
    metrics["avg_latency_ms"] = round(sum(latencies) / len(latencies), 1) if latencies else None

    # Desglose por categoria.
    by_category = {}
    for r in rows:
        cat = r["category"]
        slot = by_category.setdefault(cat, {"n": 0, "behavior_ok": 0})
        slot["n"] += 1
        slot["behavior_ok"] += 1 if r["behavior_ok"] else 0

    errors = [r for r in rows if r.get("error")]

    return {
        "mode": mode,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "eval_set": os.path.basename(EVAL_SET),
        "n_cases": n,
        "n_errors": len(errors),
        "metrics": metrics,
        "by_category": by_category,
        "notes": (
            "Modo mock: las metricas de contenido (non_hallucination_rate, "
            "source_usage_rate, audio_claim_avoidance_rate, avg_latency_ms) son null "
            "porque no hay texto generado; requieren --mode real con Ollama."
            if mode == "mock" else
            "Modo real: source_usage_rate depende de que el indice Chroma del corpus "
            "este construido; sin corpus indexado sera bajo aunque el tutor responda."
        ),
        "per_case": rows,
    }


def print_summary(report: dict) -> None:
    m = report["metrics"]
    print("\n" + "=" * 64)
    print(f"  EVALUACION DEL TUTOR  ({report['mode']})  —  {report['n_cases']} casos")
    print("=" * 64)
    def fmt(v):
        return "n/a" if v is None else (f"{v*100:.1f}%" if isinstance(v, float) and v <= 1 else str(v))
    print(f"  Behavior accuracy ............. {fmt(m['behavior_accuracy'])}")
    print(f"  Behavior accuracy (ponderada) . {fmt(m['behavior_accuracy_weighted'])}")
    print(f"  Rechazo correcto .............. {fmt(m['correct_rejection_rate'])}")
    print(f"  Fuera de alcance bloqueado .... {fmt(m['out_of_scope_blocked_rate'])}")
    print(f"  Pedir-mas-contexto correcto ... {fmt(m['ask_more_context_accuracy'])}")
    print(f"  No-alucinacion ................ {fmt(m['non_hallucination_rate'])}")
    print(f"  Uso de fuentes ................ {fmt(m['source_usage_rate'])}")
    print(f"  No afirma analisis de audio ... {fmt(m['audio_claim_avoidance_rate'])}")
    print(f"  Latencia promedio (ms) ........ {m['avg_latency_ms'] if m['avg_latency_ms'] is not None else 'n/a'}")
    if report["n_errors"]:
        print(f"  [!] casos con error de ejecucion: {report['n_errors']}")
    print("  Por categoria:")
    for cat, s in sorted(report["by_category"].items()):
        print(f"    - {cat:28s} {s['behavior_ok']}/{s['n']}")
    print("=" * 64 + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluacion de calidad del tutor IA.")
    parser.add_argument("--mode", choices=["mock", "real"], default="mock",
                        help="mock = routing determinista offline; real = agente completo (Ollama).")
    parser.add_argument("--course-id", default="2", help="course_id Moodle para scoping (modo real).")
    parser.add_argument("--eval-set", default=EVAL_SET, help="ruta al .jsonl de casos.")
    parser.add_argument("--out", default="", help="ruta extra para guardar el JSON (p. ej. example).")
    args = parser.parse_args()

    cases = load_cases(args.eval_set)
    if not cases:
        print(f"[ERROR] sin casos en {args.eval_set}")
        return 2

    rows = []
    for case in cases:
        if args.mode == "mock":
            observed = predict_behavior_mock(case["question"])
        else:
            observed = run_real(case, args.course_id)
        rows.append(score_case(case, observed, args.mode))

    report = aggregate(cases, rows, args.mode)
    print_summary(report)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_out = os.path.join(RESULTS_DIR, f"{args.mode}_{stamp}.json")
    with open(default_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"[OK] resultados guardados en {default_out}")

    if args.out:
        out_abs = args.out if os.path.isabs(args.out) else os.path.join(_BACKEND_ROOT, args.out)
        os.makedirs(os.path.dirname(out_abs), exist_ok=True)
        with open(out_abs, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[OK] copia guardada en {out_abs}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
