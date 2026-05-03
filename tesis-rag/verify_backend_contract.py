"""Smoke tests for the /chat contract after thesis hardening phases.

Run with the FastAPI backend already started:
    python verify_backend_contract.py

Optional image case:
    python verify_backend_contract.py --include-image
"""
import argparse
import base64
import json
import sqlite3
import sys
import time
from pathlib import Path
from urllib import request, error


BASE_URL = "http://127.0.0.1:8000/chat"
REQUIRED_KEYS = ["respuesta"]
OPTIONAL_KEYS = [
    "answer_type",
    "intent",
    "course_module",
    "evaluation_category",
    "evidence_level",
    "fuentes",
    "warnings",
    "trace_id",
    "prompt_id",
]


def _post_chat(payload: dict, timeout: int):
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        BASE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with request.urlopen(req, timeout=timeout) as response:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        data = json.loads(response.read().decode("utf-8"))
    return data, elapsed_ms


def _tiny_png_base64():
    # 1x1 transparent PNG. Useful only to verify image contract path, not audio semantics.
    raw = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
        b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def _cases(include_image: bool):
    session_id = "verify-contract-session"
    cases = [
        {
            "name": "aclaracion_concepto_sin_session",
            "payload": {"pregunta": "Que es el headroom?", "contexto_leccion": ""},
            "expected_answer_type": {"rag_answer", "needs_more_context"},
        },
        {
            "name": "diagnostico_tecnico_con_session",
            "payload": {
                "pregunta": "Por que mi mezcla pierde fuerza en mono?",
                "contexto_leccion": "",
                "session_id": session_id,
                "source_client": "smoke_test",
            },
            "expected_intent": {"diagnostico_tecnico", "aclaracion_concepto"},
        },
        {
            "name": "ambigua_con_session",
            "payload": {
                "pregunta": "Y a cuantos dB?",
                "session_id": session_id,
                "source_client": "smoke_test",
            },
            "expected_answer_type": {"clarification"},
        },
        {
            "name": "fuera_dominio",
            "payload": {"pregunta": "Quien gano el mundial?", "contexto_leccion": ""},
            "expected_answer_type": {"out_of_domain"},
        },
        {
            "name": "busqueda_fuente",
            "payload": {
                "pregunta": "Que recurso reviso para entender Q constante y proporcional?",
                "contexto_leccion": "",
            },
            "expected_answer_type": {"source_lookup"},
        },
        {
            "name": "usar_internet_true",
            "payload": {
                "pregunta": "Busca informacion externa sobre plugins de medicion para mastering",
                "usar_internet": True,
            },
            "expected_answer_type": {"web_answer"},
        },
    ]

    if include_image:
        cases.append({
            "name": "imagen_no_audio_minima",
            "payload": {
                "pregunta": "Que ves en esta imagen?",
                "imagen": _tiny_png_base64(),
            },
            "expected_answer_type": {"image_feedback"},
        })

    return cases


def _check_db_traces(trace_ids):
    db_path = Path(__file__).resolve().parent / "bd_chat" / "chats.db"
    if not db_path.exists():
        return {"db_exists": False, "interaction_hits": 0, "message_hits": 0}

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    interaction_hits = 0
    message_hits = 0
    try:
        cursor.execute(
            f"SELECT COUNT(*) FROM interaction_traces WHERE id IN ({','.join('?' for _ in trace_ids)})",
            trace_ids,
        )
        interaction_hits = cursor.fetchone()[0]
    except Exception:
        interaction_hits = -1

    try:
        cursor.execute(
            f"SELECT COUNT(*) FROM message_traces WHERE id IN ({','.join('?' for _ in trace_ids)})",
            trace_ids,
        )
        message_hits = cursor.fetchone()[0]
    except Exception:
        message_hits = -1

    conn.close()
    return {"db_exists": True, "interaction_hits": interaction_hits, "message_hits": message_hits}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--include-image", action="store_true")
    args = parser.parse_args()

    trace_ids = []
    failures = []

    for case in _cases(args.include_image):
        name = case["name"]
        try:
            data, elapsed_ms = _post_chat(case["payload"], args.timeout)
        except error.URLError as exc:
            print(f"[FAIL] {name}: backend unreachable or timeout: {exc}")
            return 2
        except Exception as exc:
            print(f"[FAIL] {name}: {exc}")
            return 2

        missing_required = [key for key in REQUIRED_KEYS if key not in data]
        missing_optional = [key for key in OPTIONAL_KEYS if key not in data]
        fuentes = data.get("fuentes") or []
        trace_id = data.get("trace_id")
        if trace_id:
            trace_ids.append(trace_id)

        expected_answer_type = case.get("expected_answer_type")
        if expected_answer_type and data.get("answer_type") not in expected_answer_type:
            failures.append(f"{name}: answer_type={data.get('answer_type')} expected={sorted(expected_answer_type)}")

        expected_intent = case.get("expected_intent")
        if expected_intent and data.get("intent") not in expected_intent:
            failures.append(f"{name}: intent={data.get('intent')} expected={sorted(expected_intent)}")

        if missing_required:
            failures.append(f"{name}: missing required keys {missing_required}")

        print(
            f"[OK] {name} | {elapsed_ms}ms | "
            f"answer_type={data.get('answer_type')} | "
            f"intent={data.get('intent')} | "
            f"evidence={data.get('evidence_level')} | "
            f"fuentes_count={len(fuentes)} | "
            f"trace_id={trace_id} | "
            f"prompt_id={data.get('prompt_id')}"
        )
        if missing_optional:
            print(f"     optional_missing={missing_optional}")
        print(f"     respuesta={(data.get('respuesta') or '')[:180].replace(chr(10), ' ')}")

    if trace_ids:
        db_status = _check_db_traces(trace_ids)
        print(f"[DB] {db_status}")
        if db_status["db_exists"] and db_status["interaction_hits"] < len(trace_ids):
            failures.append("interaction_traces did not persist every trace_id")

    if failures:
        print("\nFAILURES:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nAll contract smoke tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
