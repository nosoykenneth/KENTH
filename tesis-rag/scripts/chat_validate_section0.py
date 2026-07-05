#!/usr/bin/env python
"""Validación de chat por lección (Sección 0) por INVOCACIÓN DIRECTA del agente.

No usa HTTP ni token: construye el envelope y llama a super_agente, igual que
api/routes/chat.py. Sirve para probar el flujo docente (transcripción aprobada +
teacher_approved_context) contra el tutor real, localmente o en el servidor.

Uso (desde tesis-rag/, con Ollama arriba):
  python scripts/chat_validate_section0.py                 # lecciones presentes en BD
  python scripts/chat_validate_section0.py --lessons SEC2-R55
  python scripts/chat_validate_section0.py --report DIR    # escribe CHAT_VALIDATION.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

COURSE_ID = "2"
SECTION_ID = "2"

# Preguntas por lección: general + conceptual + aplicada. Anti-cruce incluido.
LESSON_QUESTIONS = {
    "SEC2-R55": [
        "¿De qué trata esta lección?",
        "¿Cuáles son los pasos del ciclo de trabajo al mezclar?",
        "¿Cómo verifico honestamente si un cambio mejoró la mezcla?",
    ],
    "SEC2-R56": [
        "¿De qué trata esta lección?",
        "¿Por qué se dice que el oído miente?",
        "¿Qué debería hacer con el nivel de escucha al mezclar?",
    ],
    "SEC2-R57": ["¿De qué trata esta lección?", "¿Monitores o auriculares?", "¿Cómo trabajo con lo que tengo?"],
    "SEC2-R58": ["¿De qué trata esta lección?", "¿Qué es el ruteo en el mixer?", "¿Cómo aplico esto en cualquier DAW?"],
    "SEC2-R59": ["¿De qué trata esta lección?", "¿Qué es el gain staging?", "¿Cómo ajusto la ganancia de entrada?"],
    "SEC2-R60": ["¿De qué trata esta lección?", "¿Nativo o emulación analógica?", "¿Cuándo conviene cada uno?"],
    "SEC2-R61": ["¿De qué trata esta lección?", "¿Qué reviso antes de mezclar?", "¿Cómo dejo la sesión lista?"],
}

# Casos globales (no atados a una lección).
EDGE_CASES = [
    ("out_of_domain", "¿Cuál es la capital de Francia?", "SEC2-R55"),
]


def _ask(question: str, lesson_id: str) -> dict:
    from services.context_service import build_envelope, render_context_block
    from services.agent_service import super_agente
    from services.db_service import resolve_course_numeric

    raw_ctx = {"current_lesson_id": lesson_id, "moodle_section_id": SECTION_ID}
    envelope = build_envelope(question=question, raw_activity_context=raw_ctx,
                              session_id=None, has_image=False)
    block = render_context_block(envelope)
    scoped = resolve_course_numeric(COURSE_ID) or COURSE_ID
    estado = {
        "pregunta": question, "course_id": scoped,
        "current_lesson_id": lesson_id, "moodle_section_id": SECTION_ID,
        "current_section_name": envelope.activity_context.current_section_name,
        "current_section_order": envelope.activity_context.current_section_order,
        "contexto_leccion": "", "imagen": None, "ruta": "", "historial": [],
        "respuesta_final": "", "evidencias": [], "evidence_level": "", "intent": "",
        "answer_type": "", "course_module": "", "evaluation_category": "",
        "requires_course_evidence": True, "warnings": [], "retrieved_chunks": [],
        "trace_id": "chatval", "model_used": "", "prompt_id": "",
        "activity_context_block": block, "tutor_envelope": envelope,
    }
    out = super_agente.invoke(estado)
    fuentes = out.get("evidencias", []) or []
    src_titles = []
    for f in fuentes[:5]:
        meta = (f.get("document").metadata if f.get("document") else {}) or {}
        src_titles.append({
            "lesson_id": meta.get("lesson_id"), "source": meta.get("source"),
            "source_type": meta.get("source_type"), "title": meta.get("title") or meta.get("lesson_title"),
            "visible": meta.get("visible_to_student"),
        })
    return {
        "respuesta": out.get("respuesta_final", ""),
        "ruta": out.get("ruta", ""),
        "retrieval_scope": out.get("retrieval_scope", ""),
        "evidence_level": out.get("evidence_level", ""),
        "blocked_by": out.get("blocked_by", ""),
        "fuentes": src_titles,
    }


def _checks(lesson_id: str, question: str, r: dict) -> list:
    """Heurísticas de aceptación (Fase 11)."""
    resp = (r.get("respuesta") or "")
    low = resp.lower()
    issues = []
    if lesson_id and any(f.get("lesson_id") and f["lesson_id"] != lesson_id for f in r["fuentes"]):
        # otra lección entre las fuentes top: sólo aviso si NINGUNA es de la lección
        if not any(f.get("lesson_id") == lesson_id for f in r["fuentes"]):
            issues.append("fuentes de OTRA lección (posible herencia)")
    if "sec2-r" in low:
        issues.append("expone ID técnico SEC2-R en la respuesta")
    if "según la evidencia" in low:
        issues.append("usa muletilla 'según la evidencia'")
    if not resp.strip():
        issues.append("respuesta vacía")
    return issues


def run(lessons: list, report_dir: str) -> dict:
    from services import db_service
    db_service.init_db()
    present = []
    for lid in lessons:
        if db_service.get_lesson(lid, COURSE_ID):
            present.append(lid)
    results = []
    for lid in present:
        for q in LESSON_QUESTIONS.get(lid, []):
            r = _ask(q, lid)
            r.update({"lesson_id": lid, "question": q, "issues": _checks(lid, q, r)})
            results.append(r)
            print(f"[{lid}] Q: {q}\n  ruta={r['ruta']} scope={r['retrieval_scope']} "
                  f"ev={r['evidence_level']} issues={r['issues']}\n  A: {r['respuesta'][:180]}\n")
    edge = []
    for name, q, lid in EDGE_CASES:
        r = _ask(q, lid)
        ok_refuse = r["ruta"] in ("bloqueo", "guardia") or "no" in (r["respuesta"] or "").lower()[:40]
        r.update({"case": name, "question": q, "expected": "refuse", "ruta_ok": ok_refuse})
        edge.append(r)
        print(f"[edge {name}] ruta={r['ruta']} blocked_by={r['blocked_by']} A: {r['respuesta'][:120]}\n")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "course_id": COURSE_ID, "lessons_tested": present,
        "results": results, "edge_cases": edge,
    }
    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, "chat_validation.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lessons", nargs="*", default=list(LESSON_QUESTIONS.keys()))
    ap.add_argument("--report", default="")
    args = ap.parse_args()
    run(args.lessons, args.report)


if __name__ == "__main__":
    main()
