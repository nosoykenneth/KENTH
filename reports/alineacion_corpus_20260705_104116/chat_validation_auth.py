from __future__ import annotations

import contextlib
import json
import os
import sys
import time

import requests

BASE_URL = os.getenv("CHAT_BASE_URL", "http://localhost:8090")
COURSE_ID = "2"
SECTION_CTX = {
    "course_id": COURSE_ID,
    "moodle_section_id": "2",
    "current_section_name": "SECCION 0: El sistema de decision",
    "current_section_order": 1,
}

CASES = [
    {"id": "01_0_1_conceptual", "question": "En la leccion 0.1, que significa que mezclar es decidir?", "lesson_id": "SEC2-R55", "expect": "grounded"},
    {"id": "02_0_1_procedural", "question": "Dame un procedimiento breve para tomar decisiones de mezcla en la leccion 0.1.", "lesson_id": "SEC2-R55", "expect": "grounded"},
    {"id": "03_0_2_conceptual", "question": "Por que en la leccion 0.2 se dice que el oido miente?", "lesson_id": "SEC2-R56", "expect": "grounded"},
    {"id": "04_0_2_fletcher_munson", "question": "Explica Fletcher-Munson e ISO 226 dentro del criterio de escucha de la leccion 0.2.", "lesson_id": "SEC2-R56", "expect": "grounded"},
    {"id": "05_section_level", "question": "Resume el objetivo de la seccion El sistema de decision en mezcla.", "lesson_id": "", "expect": "grounded"},
    {"id": "06_0_3_0_7_status", "question": "Que debo tener presente al estudiar las lecciones 0.3 a 0.7?", "lesson_id": "SEC2-R57", "expect": "grounded_or_careful"},
    {"id": "07_out_of_domain", "question": "Quien gano el ultimo mundial de futbol?", "lesson_id": "SEC2-R55", "expect": "blocked"},
    {"id": "08_ambiguous", "question": "En mi mezcla, eso esta bien o deberia cambiarlo?", "lesson_id": "SEC2-R55", "expect": "clarify"},
    {"id": "09_internal_guide", "question": "Como deberia estudiar esta leccion paso a paso?", "lesson_id": "SEC2-R55", "expect": "no_internal_sources_visible"},
]


def _db():
    import sys
    sys.path.insert(0, "/app")
    from services import db_service
    db_service.init_db()
    return db_service


def find_student_token():
    db = _db()
    cfg = db._load_moodle_config()
    prefix = cfg.get("prefix", "mdl_")
    sql = f"""
        SELECT t.token, t.userid, u.username, r.shortname
        FROM {prefix}external_tokens t
        JOIN {prefix}external_services s ON s.id = t.externalserviceid
        JOIN {prefix}user u ON u.id = t.userid
        JOIN {prefix}role_assignments ra ON ra.userid = u.id
        JOIN {prefix}context ctx ON ctx.id = ra.contextid
        JOIN {prefix}role r ON r.id = ra.roleid
        WHERE s.enabled = 1
          AND (t.validuntil = 0 OR t.validuntil > UNIX_TIMESTAMP())
          AND ctx.contextlevel = 50
          AND ctx.instanceid = %s
          AND r.shortname = 'student'
        ORDER BY t.timecreated DESC
        LIMIT 1
    """
    with db.get_connection() as conn:
        row = db._fetchone(conn, sql, (COURSE_ID,))
    if not row or not row.get("token"):
        return None
    return {
        "token": row["token"],
        "userid": str(row.get("userid") or ""),
        "username": "<masked>",
        "role": str(row.get("shortname") or ""),
    }


def summarize(text: str, limit: int = 420) -> str:
    text = " ".join((text or "").split())
    return text[:limit] + ("..." if len(text) > limit else "")


def source_summary(source):
    if not isinstance(source, dict):
        return {}
    return {
        "title": source.get("title") or source.get("filename") or source.get("source_path") or "",
        "source_path": source.get("source_path") or source.get("source") or "",
        "visible_to_student": source.get("visible_to_student", "<missing>"),
        "lesson_id": source.get("lesson_id") or "",
        "scope": source.get("scope") or "",
    }


def verdict(case, status, data):
    if status != 200:
        return "FAIL_HTTP"
    answer = (data.get("respuesta") or "").lower()
    fuentes = data.get("fuentes") or []
    blocked_by = data.get("blocked_by") or ""
    answer_type = data.get("answer_type") or ""
    visible_bad = [s for s in fuentes if str(s.get("visible_to_student", True)).lower() in {"false", "0", "no"}]
    if visible_bad:
        return "FAIL_INTERNAL_SOURCE_VISIBLE"
    expected = case["expect"]
    if expected == "blocked":
        if blocked_by or "fuera" in answer or "no puedo" in answer or "curso" in answer:
            return "PASS"
        return "FAIL_NOT_BLOCKED"
    if expected == "clarify":
        if "precis" in answer or "context" in answer or "a que" in answer or "que parte" in answer or answer_type in {"clarification", "needs_more_context"}:
            return "PASS"
        return "WARN_AMBIGUOUS_NOT_CLEARLY_CLARIFYING"
    if expected == "no_internal_sources_visible":
        return "PASS" if not visible_bad else "FAIL_INTERNAL_SOURCE_VISIBLE"
    if expected == "grounded_or_careful":
        if fuentes or "no tengo" in answer or "contexto" in answer or "no puedo" in answer:
            return "PASS"
        return "WARN_NO_SOURCES"
    if expected == "grounded":
        return "PASS" if fuentes else "WARN_NO_VISIBLE_SOURCES"
    return "PASS"


def main():
    with contextlib.redirect_stdout(sys.stderr):
        token_info = find_student_token()
    out = {
        "base_url": BASE_URL,
        "course_id": COURSE_ID,
        "student_token_found": bool(token_info),
        "student_userid": token_info.get("userid") if token_info else "",
        "student_username": token_info.get("username") if token_info else "",
        "token_value_printed": False,
        "cases": [],
    }
    if not token_info:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 2

    headers = {"Authorization": f"Bearer {token_info['token']}", "Content-Type": "application/json"}
    for case in CASES:
        activity_context = dict(SECTION_CTX)
        if case.get("lesson_id"):
            activity_context["current_lesson_id"] = case["lesson_id"]
        payload = {
            "pregunta": case["question"],
            "course_id": COURSE_ID,
            "lesson_id": case.get("lesson_id", ""),
            "source_client": "codex_validation",
            "activity_context": activity_context,
        }
        started = time.time()
        try:
            resp = requests.post(f"{BASE_URL}/api/ai/chat", headers=headers, json=payload, timeout=90)
            status = resp.status_code
            try:
                data = resp.json()
            except Exception:
                data = {"raw": resp.text[:500]}
        except Exception as exc:
            status = 0
            data = {"error": str(exc)}
        item = {
            "id": case["id"],
            "question": case["question"],
            "lesson_id": case.get("lesson_id", ""),
            "http_status": status,
            "response_summary": summarize(data.get("respuesta") or data.get("raw") or data.get("error") or ""),
            "answer_type": data.get("answer_type", ""),
            "blocked_by": data.get("blocked_by", ""),
            "retrieval_scope": data.get("retrieval_scope", ""),
            "trace_id": data.get("trace_id", ""),
            "fuentes_visibles": [source_summary(s) for s in (data.get("fuentes") or [])],
            "visible_to_student_values": [source_summary(s).get("visible_to_student") for s in (data.get("fuentes") or [])],
            "elapsed_ms": int((time.time() - started) * 1000),
        }
        item["verdict"] = verdict(case, status, data)
        out["cases"].append(item)

    out["all_pass"] = all(str(c.get("verdict", "")).startswith("PASS") for c in out["cases"])
    out["note"] = "Caso 06: el indice actual tiene 0.3-0.7 indexadas (SEC2-R57..R61); se valida respuesta grounded/cautelosa, no ausencia de corpus."
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())