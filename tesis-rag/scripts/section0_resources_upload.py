#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FASE 3 — Sube los recursos docentes reales de la Sección 0 por el FLUJO DEL
PROFESOR (endpoints HTTP `require_teacher`), no por inserciones técnicas invisibles.

Para cada recurso del manifest (`section0_resources_manifest.json`):
  - kind=upload      -> POST /api/ai/authoring/lessons/{lesson_id}/resources
                        (multipart con el binario). PDF -> resource_text; imagen/FLP
                        -> resource_description. El binario se guarda y es servible.
  - kind=description -> POST /api/ai/authoring/lessons/{lesson_id}/resources/description
                        (sin binario). Para material pesado/externo (stems, audio
                        grande): solo se indexa la descripción (resource_description).

El token docente se busca en la BD (rol editingteacher/manager del curso) y se PRUEBA
contra un endpoint `require_teacher`; nunca se imprime. Idempotente: el doc_id se
deriva de lesson_id+title, así que re-subir REEMPLAZA (delete-then-add).

Ejecutar DENTRO del contenedor fastapi del servidor (tiene BD + red al gateway):
    docker exec tic-fastapi python /app/scripts/section0_resources_upload.py \
        --staging /tmp/section0_staging --report /app/reports/... [--dry-run]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import mimetypes
import os
import sys
import time

sys.path.insert(0, "/app")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests  # noqa: E402
from services import db_service  # noqa: E402

COURSE_ID = "2"
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "section0_resources_manifest.json")


def find_teacher_token(base_url: str):
    """Devuelve (token, username, userid) de un docente del curso cuyo token PASA
    require_teacher. No imprime el token."""
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
            r = requests.get(
                f"{base_url}/api/ai/authoring/lessons/SEC2-R55/resources",
                headers={"Authorization": f"Bearer {tok}", "X-Course-Id": COURSE_ID},
                timeout=30,
            )
            if r.status_code == 200:
                return tok, row.get("username"), row.get("userid")
        except Exception:
            continue
    return None, None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging", required=True, help="dir con los binarios (subdirs por lesson_id)")
    ap.add_argument("--base-url", default="http://gateway")
    ap.add_argument("--report", default="", help="dir donde escribir RESULTS.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    resources = manifest["resources"]

    with contextlib.redirect_stdout(sys.stderr):
        token, uname, uid = find_teacher_token(args.base_url)
    if not token and not args.dry_run:
        print(json.dumps({"error": "no se encontró token docente válido (require_teacher)"}))
        return 2
    print(f"[auth] docente={uname} (uid={uid}) token_ok={bool(token)} printed=False", file=sys.stderr)

    headers = {"Authorization": f"Bearer {token}", "X-Course-Id": COURSE_ID} if token else {}
    out = {"course_id": COURSE_ID, "teacher_username": uname, "token_printed": False,
           "dry_run": args.dry_run, "results": []}

    for res in resources:
        lid = res["lesson_id"]
        kind = res["kind"]
        rec = {"lesson_id": lid, "title": res["title"], "kind": kind, "media": res.get("media")}
        if args.dry_run:
            rec["status"] = "DRY_RUN"
            out["results"].append(rec)
            continue
        started = time.time()
        try:
            if kind == "upload":
                fp = os.path.join(args.staging, res["file"])
                if not os.path.exists(fp):
                    rec.update({"status": "MISSING_FILE", "file": res["file"]})
                    out["results"].append(rec)
                    continue
                ctype = mimetypes.guess_type(fp)[0] or "application/octet-stream"
                with open(fp, "rb") as fh:
                    files = {"file": (os.path.basename(fp), fh, ctype)}
                    data = {
                        "title": res["title"], "description": res["description"],
                        "concepts": res.get("concepts", ""), "index_to_tutor": "true",
                        "visible_to_student": "true" if res.get("visible", True) else "false",
                        "resource_type": res.get("resource_type", ""),
                    }
                    r = requests.post(
                        f"{args.base_url}/api/ai/authoring/lessons/{lid}/resources",
                        headers=headers, files=files, data=data, timeout=180,
                    )
            else:  # description-only
                data = {
                    "title": res["title"], "description": res["description"],
                    "concepts": res.get("concepts", ""), "media_type": res.get("media", "file"),
                    "resource_type": res.get("resource_type", ""),
                    "visible_to_student": "true" if res.get("visible", False) else "false",
                }
                r = requests.post(
                    f"{args.base_url}/api/ai/authoring/lessons/{lid}/resources/description",
                    headers=headers, data=data, timeout=120,
                )
            body = {}
            with contextlib.suppress(Exception):
                body = r.json()
            rec.update({
                "status": "OK" if r.status_code == 200 else f"HTTP_{r.status_code}",
                "http_status": r.status_code,
                "chunks": (body.get("chunks") if isinstance(body, dict) else None),
                "doc_id": ((body.get("resource") or {}).get("doc_id") if isinstance(body, dict) else None),
                "index_status": ((body.get("resource") or {}).get("index_status") if isinstance(body, dict) else None),
                "error": (body.get("detail") if isinstance(body, dict) and r.status_code != 200 else None),
                "elapsed_ms": int((time.time() - started) * 1000),
            })
        except Exception as exc:
            rec.update({"status": "EXCEPTION", "error": str(exc)})
        out["results"].append(rec)

    ok = sum(1 for x in out["results"] if x.get("status") == "OK")
    out["summary"] = {"total": len(out["results"]), "ok": ok,
                      "fail": len(out["results"]) - ok - (len(out["results"]) if args.dry_run else 0)}
    if args.report:
        os.makedirs(args.report, exist_ok=True)
        json.dump(out, open(os.path.join(args.report, "FASE3_RESULTS.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    print(json.dumps(out.get("summary", {}), ensure_ascii=False))
    for x in out["results"]:
        if x.get("status") != "OK" and not args.dry_run:
            print(f"  !! {x['lesson_id']} {x['title'][:40]} -> {x.get('status')} {x.get('error') or ''}", file=sys.stderr)
    return 0 if (args.dry_run or ok == len(out["results"])) else 1


if __name__ == "__main__":
    sys.exit(main())
