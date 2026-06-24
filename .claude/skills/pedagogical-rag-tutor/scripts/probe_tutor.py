#!/usr/bin/env python3
"""Golpea el endpoint real del tutor (/chat) e imprime respuesta + diagnóstico.

Sirve para reproducir un turno end-to-end (no funciones aisladas) durante una
auditoría o al validar un fix: construye el payload `Consulta` con el contexto de
actividad anidado correctamente y muestra los campos de trazabilidad que devuelve
el backend (ruta/selected_route, intent, evidence_level, warnings,
runtime_context, source_policy).

Solo stdlib. No embebe credenciales: el token y la URL salen de variables de
entorno o de argumentos. Agnóstico al curso.

Variables de entorno (opcionales):
    KENTH_AI_BASE_URL   URL base del servicio de IA (def. http://localhost:8000)
    KENTH_TOKEN         token Moodle (Authorization: Bearer ...)
    KENTH_USER_ID       solo para dev sin Moodle (header X-User-Id)

Ejemplos:
    # Tutor dentro de lección, con timestamp -> debe resolver bloque activo
    python probe_tutor.py --course-id 2 --lesson-id L_123 --section-id 7 \
        --resource-id R_9 --timestamp 142.0 \
        --message "¿qué hago con el clipping aquí?"

    # Misma pregunta SIN timestamp -> debe seguir a nivel de lección
    python probe_tutor.py --course-id 2 --lesson-id L_123 \
        --message "¿qué hago con el clipping aquí?"

    # Tutor general del curso (sin lesson_id) -> no debe inventar bloque/video
    python probe_tutor.py --course-id 2 --message "¿por dónde empiezo el curso?"

    # Tema delegado al tutor que NO está en el RAG -> no debe bloquear
    python probe_tutor.py --course-id 2 --lesson-id L_123 \
        --message "¿cómo hago este paso en otra herramienta?"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# Evita UnicodeEncodeError al imprimir acentos en consolas Windows cp1252.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

DIAG_FIELDS = [
    "ruta", "intent", "answer_type", "course_module", "evaluation_category",
    "evidence_level", "blocked_by", "applied_policies", "warnings",
    "runtime_context", "source_policy", "trace_id",
]


def build_payload(args) -> dict:
    activity: dict = {}
    if args.section_id:
        activity["moodle_section_id"] = str(args.section_id)
    if args.lesson_id:
        activity["current_lesson_id"] = str(args.lesson_id)
    if args.resource_id:
        activity["current_resource_id"] = str(args.resource_id)
    if args.timestamp is not None:
        activity["current_timestamp"] = float(args.timestamp)
    if args.page is not None:
        activity["current_page"] = int(args.page)

    payload: dict = {
        "pregunta": args.message,
        "course_id": str(args.course_id) if args.course_id is not None else "",
        "usar_internet": bool(args.usar_internet),
        "source_client": args.source_client,
    }
    if args.lesson_id:
        payload["lesson_id"] = str(args.lesson_id)
    if args.session_id:
        payload["session_id"] = args.session_id
    if activity:
        payload["activity_context"] = activity
    return payload


def post(url: str, payload: dict, token: str, user_id: str, timeout: float) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if user_id:
        req.add_header("X-User-Id", user_id)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--message", "-m", required=True, help="Pregunta del alumno.")
    ap.add_argument("--course-id", default=os.environ.get("KENTH_COURSE_ID", "2"))
    ap.add_argument("--lesson-id", default=None)
    ap.add_argument("--section-id", default=None)
    ap.add_argument("--resource-id", default=None)
    ap.add_argument("--timestamp", type=float, default=None, help="Segundos de video (resuelve bloque activo).")
    ap.add_argument("--page", type=int, default=None, help="Página de PDF.")
    ap.add_argument("--session-id", default=None)
    ap.add_argument("--source-client", default="probe")
    ap.add_argument("--usar-internet", action="store_true")
    ap.add_argument("--base-url", default=os.environ.get("KENTH_AI_BASE_URL", "http://localhost:8000"))
    ap.add_argument("--path", default="/chat", help="Ruta del endpoint (def. /chat).")
    ap.add_argument("--token", default=os.environ.get("KENTH_TOKEN", ""))
    ap.add_argument("--user-id", default=os.environ.get("KENTH_USER_ID", ""))
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--raw", action="store_true", help="Imprime el JSON completo de respuesta.")
    ap.add_argument("--show-payload", action="store_true", help="Imprime el payload enviado.")
    args = ap.parse_args(argv)

    url = args.base_url.rstrip("/") + args.path
    payload = build_payload(args)

    if args.show_payload:
        print("# Payload enviado:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print()

    try:
        result = post(url, payload, args.token, args.user_id, args.timeout)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} desde {url}\n{detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"No se pudo conectar a {url}: {e.reason}\n"
              f"¿Está el backend levantado? (cd tesis-rag && python main.py)", file=sys.stderr)
        return 1

    if args.raw:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print("=" * 70)
    print("RESPUESTA DEL TUTOR")
    print("=" * 70)
    print(result.get("respuesta", "<sin respuesta>"))
    print()
    print("-" * 70)
    print("DIAGNÓSTICO / TRAZABILIDAD")
    print("-" * 70)
    for f in DIAG_FIELDS:
        if f in result:
            val = result[f]
            if isinstance(val, (dict, list)):
                val = json.dumps(val, ensure_ascii=False)
            print(f"  {f:18s}: {val}")
    fuentes = result.get("fuentes") or []
    print(f"  {'fuentes (#)':18s}: {len(fuentes)}")
    imgs = result.get("imagenes") or []
    recs = result.get("recursos") or []
    if imgs:
        print(f"  {'imagenes (#)':18s}: {len(imgs)}")
    if recs:
        print(f"  {'recursos (#)':18s}: {len(recs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
