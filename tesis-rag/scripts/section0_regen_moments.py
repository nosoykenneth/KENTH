#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FASE 6 — Regenera los MOMENTOS/bloques de las lecciones cuyos bloques eran de una
grabación anterior (tema equivocado) o estaban vacíos, usando el FLUJO DEL PROFESOR:

    POST /authoring/lessons/{id}/ai-prepare            (borrador desde la transcripción)
    POST /authoring/lessons/{id}/ai-prepare/accept     (regenerate_moments=true)

`regenerate_moments=true` descarta los bloques previos (replace_blocks) y arma la
línea de tiempo SOLO desde la transcripción actual de esa lección; luego publica el
contexto aprobado (teacher_context) para que la evidencia quede alineada al tema.

Ejecutar DENTRO del contenedor fastapi (tiene Ollama + BD + red al gateway):
    docker exec tic-fastapi python /app/scripts/section0_regen_moments.py \
        --lessons SEC2-R56,SEC2-R57,SEC2-R61 --report /app/reports/... [--dry-run]
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
from services import db_service, pedagogy_profile  # noqa: E402
from services.lesson_service import load_lesson  # noqa: E402

COURSE_ID = "2"


def find_teacher_token(base_url: str):
    db_service.init_db()
    cfg = db_service._load_moodle_config()
    p = cfg.get("prefix", "mdl_")
    sql = f"""
        SELECT t.token, u.id AS userid, u.username, r.shortname
        FROM {p}role_assignments ra
        JOIN {p}context ctx ON ctx.id = ra.contextid AND ctx.contextlevel = 50 AND ctx.instanceid = %s
        JOIN {p}role r ON r.id = ra.roleid
        JOIN {p}user u ON u.id = ra.userid
        JOIN {p}external_tokens t ON t.userid = u.id
        JOIN {p}external_services s ON s.id = t.externalserviceid AND s.enabled = 1
        WHERE r.shortname IN ('editingteacher','manager')
          AND (t.validuntil = 0 OR t.validuntil > UNIX_TIMESTAMP())
        ORDER BY FIELD(r.shortname,'editingteacher','manager'), t.timecreated DESC
    """
    with db_service.get_connection() as c:
        rows = db_service._fetchall(c, sql, (COURSE_ID,))
    for row in rows or []:
        tok = row.get("token")
        if not tok:
            continue
        try:
            r = requests.get(f"{base_url}/api/ai/authoring/lessons/SEC2-R55/resources",
                             headers={"Authorization": f"Bearer {tok}", "X-Course-Id": COURSE_ID}, timeout=30)
            if r.status_code == 200:
                return tok, row.get("username")
        except Exception:
            continue
    return None, None


def moment_titles(lesson_id: str):
    l = load_lesson(lesson_id, COURSE_ID)
    if not l:
        return []
    prof = pedagogy_profile.build_profile(l)
    return [(m.get("title") or "").strip() for m in (prof.get("moments") or [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lessons", default="SEC2-R56,SEC2-R57,SEC2-R61")
    ap.add_argument("--base-url", default="http://gateway")
    ap.add_argument("--quality", default="balanced")
    ap.add_argument("--report", default="")
    ap.add_argument("--no-clear", action="store_true",
                    help="NO vaciar los bloques antes de generar (por defecto sí se vacían)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    lessons = [x.strip() for x in args.lessons.split(",") if x.strip()]

    with contextlib.redirect_stdout(sys.stderr):
        token, uname = find_teacher_token(args.base_url)
    if not token and not args.dry_run:
        print(json.dumps({"error": "no teacher token"}))
        return 2
    print(f"[auth] docente={uname} token_ok={bool(token)} printed=False", file=sys.stderr)
    headers = {"Authorization": f"Bearer {token}", "X-Course-Id": COURSE_ID} if token else {}

    out = {"course_id": COURSE_ID, "quality": args.quality, "results": []}
    for lid in lessons:
        rec = {"lesson_id": lid, "before": moment_titles(lid)}
        if args.dry_run:
            rec["status"] = "DRY_RUN"
            out["results"].append(rec)
            continue
        t0 = time.time()
        try:
            # Reset de bloques ANTES de generar: el prompt de ai-prepare recibe los
            # bloques existentes y el modelo REPRODUCE sus títulos. Si son de una
            # grabación anterior (tema equivocado), la regeneración los repetiría. Al
            # vaciarlos primero, el modelo propone momentos SOLO desde la transcripción
            # actual. Es una reparación puntual de datos stale (documentada).
            if not args.no_clear:
                db_service.replace_lesson_blocks(lid, [])
                rec["cleared_stale_blocks"] = True
            rp = requests.post(f"{args.base_url}/api/ai/authoring/lessons/{lid}/ai-prepare",
                               headers=headers, json={"mode": "draft", "quality": args.quality,
                                                      "include_resources": True}, timeout=600)
            rec["prepare_status"] = rp.status_code
            ra = requests.post(f"{args.base_url}/api/ai/authoring/lessons/{lid}/ai-prepare/accept",
                               headers=headers, json={"apply_moments": True, "regenerate_moments": True},
                               timeout=180)
            rec["accept_status"] = ra.status_code
            body = {}
            with contextlib.suppress(Exception):
                body = ra.json()
            rec["moments_applied"] = body.get("moments_applied")
            rec["teacher_context_chunks"] = body.get("teacher_context_chunks")
            rec["index_status"] = body.get("index_status")
            rec["after"] = moment_titles(lid)
            rec["status"] = "OK" if (rp.status_code == 200 and ra.status_code == 200) else "FAIL"
            rec["elapsed_ms"] = int((time.time() - t0) * 1000)
        except Exception as exc:
            rec["status"] = "EXCEPTION"
            rec["error"] = str(exc)
        out["results"].append(rec)
        print(f"[{lid}] {rec.get('status')} before={len(rec['before'])} after={len(rec.get('after', []))} "
              f"applied={rec.get('moments_applied')}", file=sys.stderr)

    if args.report:
        os.makedirs(args.report, exist_ok=True)
        json.dump(out, open(os.path.join(args.report, "FASE6_REGEN.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    print(json.dumps({"lessons": len(out["results"]),
                      "ok": sum(1 for r in out["results"] if r.get("status") == "OK")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
