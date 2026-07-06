#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FASE 8 (extra) — Preguntas sobre RECURSOS de la Sección 0. Verifica que el tutor
responde sobre PDFs, imágenes, proyectos de DAW (.flp), audio y stems apoyándose en
resource_text/resource_description (no en canonical_md, que ya no es fuente activa).

Ejecutar DENTRO del contenedor fastapi:
    docker exec tic-fastapi python /app/scripts/section0_resource_questions.py \
        --report /tmp/section0_report
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import time

sys.path.insert(0, "/app")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests  # noqa: E402
from services import db_service  # noqa: E402

COURSE_ID = "2"
SECTION_ID = "2"

# (lesson_id, pregunta, palabras que deberían aparecer en una respuesta grounded)
CASES = [
    ("SEC2-R59", "¿Qué contiene el proyecto 0_5_gain_staging_hot.flp y para qué sirve?", ["nivel", "gain"]),
    ("SEC2-R55", "¿Para qué uso la bitácora de decisiones de mezcla?", ["decisi"]),
    ("SEC2-R58", "¿Qué muestra el diagrama de flujo de señal?", ["señal", "insert", "bus", "fader"]),
    ("SEC2-R61", "¿Qué debería practicar con el checklist de sesión lista para mezclar?", ["checklist", "sesi"]),
    ("SEC2-R55", "¿Qué son los stems base y para qué sirven en la práctica?", ["stem", "pista"]),
    ("SEC2-R56", "¿Para qué sirve el fragmento de audio de 60 segundos de la lección?", ["audio", "escuch", "nivel"]),
]


def find_student_token(base_url):
    db_service.init_db()
    cfg = db_service._load_moodle_config()
    p = cfg.get("prefix", "mdl_")
    sql = f"""
        SELECT t.token FROM {p}external_tokens t
        JOIN {p}external_services s ON s.id=t.externalserviceid AND s.enabled=1
        JOIN {p}role_assignments ra ON ra.userid=t.userid
        JOIN {p}context ctx ON ctx.id=ra.contextid AND ctx.contextlevel=50 AND ctx.instanceid=%s
        JOIN {p}role r ON r.id=ra.roleid
        WHERE r.shortname='student' AND (t.validuntil=0 OR t.validuntil>UNIX_TIMESTAMP())
        ORDER BY t.timecreated DESC LIMIT 1
    """
    with db_service.get_connection() as c:
        row = db_service._fetchone(c, sql, (COURSE_ID,))
    return row.get("token") if row else None


def is_resource(src):
    sp = str(src.get("source_path") or src.get("source") or "")
    st = str(src.get("source_type") or src.get("resource_type") or "")
    mt = str(src.get("media_type") or src.get("content_type") or "")
    dt = str(src.get("doc_type") or "")
    return sp.startswith("resource:") or st in ("resource_file",) or mt in ("image", "audio", "template", "document") or dt in ("pdf", "image_description")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://gateway")
    ap.add_argument("--report", default="")
    args = ap.parse_args()

    with contextlib.redirect_stdout(sys.stderr):
        token = find_student_token(args.base_url)
    if not token:
        print(json.dumps({"error": "no student token"}))
        return 2
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    out = {"course_id": COURSE_ID, "token_printed": False, "cases": []}
    for lid, q, kws in CASES:
        payload = {"pregunta": q, "course_id": COURSE_ID, "lesson_id": lid,
                   "source_client": "section0_resource_questions",
                   "activity_context": {"course_id": COURSE_ID, "moodle_section_id": SECTION_ID,
                                        "current_lesson_id": lid}}
        try:
            r = requests.post(f"{args.base_url}/api/ai/chat", headers=headers, json=payload, timeout=90)
            data = r.json() if r.text else {}
            status = r.status_code
        except Exception as exc:
            status, data = 0, {"error": str(exc)}
        fuentes = data.get("fuentes") or []
        ans = " ".join((data.get("respuesta") or data.get("error") or "").split())
        low = ans.lower()
        has_resource = any(is_resource(s) for s in fuentes if isinstance(s, dict))
        no_canonical = not any(str((s or {}).get("source_type") or "").endswith("canonical_md") or
                               str((s or {}).get("source") or "") == "canonical_md" for s in fuentes)
        kw_hit = any(k in low for k in kws)
        grounded = status == 200 and len(ans) > 40 and data.get("answer_type") not in ("out_of_domain", "refused")
        verdict = "PASS" if (grounded and (has_resource or kw_hit) and no_canonical) else "REVIEW"
        out["cases"].append({
            "lesson_id": lid, "question": q, "http_status": status,
            "answer_type": data.get("answer_type", ""), "verdict": verdict,
            "has_resource_source": has_resource, "kw_hit": kw_hit, "no_canonical": no_canonical,
            "answer": ans[:320],
            "fuentes": [{"t": (s or {}).get("title") or (s or {}).get("source_path"),
                         "st": (s or {}).get("source_type") or (s or {}).get("resource_type"),
                         "mt": (s or {}).get("media_type")} for s in fuentes[:5] if isinstance(s, dict)],
        })
        time.sleep(2)
    summary = {"total": len(out["cases"]), "pass": sum(1 for c in out["cases"] if c["verdict"] == "PASS")}
    out["summary"] = summary
    if args.report:
        os.makedirs(args.report, exist_ok=True)
        json.dump(out, open(os.path.join(args.report, "FASE8_resource_questions.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False))
    for c in out["cases"]:
        print(f"  [{c['verdict']}] {c['lesson_id']} res={c['has_resource_source']} kw={c['kw_hit']} :: {c['answer'][:90]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
