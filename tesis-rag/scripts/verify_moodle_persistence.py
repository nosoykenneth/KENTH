"""
Verifica que los flujos operativos del tutor leen/escriben en Moodle DB.

No reindexa, no migra y no toca corpus editorial. Usa registros probe
pequenos y deterministas para validar escrituras.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services import db_service  # noqa: E402


EXPECTED_TABLES = [
    "lessons",
    "lesson_blocks",
    "course_resources",
    "resource_lesson_links",
    "lesson_prompts",
    "tutor_sessions",
    "tutor_messages",
    "message_traces",
    "interaction_traces",
    "session_context",
]


def _count_table(logical: str) -> int:
    with db_service.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) AS c FROM {db_service.table_name(logical)}")
        row = cur.fetchone()
        cur.close()
    return int(row["c"] if isinstance(row, dict) else row[0])


def main() -> None:
    db_service.init_db()
    if not db_service.using_moodle_db():
        raise SystemExit("ERROR: source is not moodle_db")

    table_counts = {name: _count_table(name) for name in EXPECTED_TABLES}

    lessons = db_service.list_lessons()
    blocks = db_service.list_lesson_blocks("E2-L01")
    prompts = db_service.list_lesson_prompts("E2-L01")
    links_signed = db_service.list_resource_links("Mi42YjU4ZDdhMDdkMjE=")
    links_numeric = db_service.list_resource_links("2")

    link = db_service.upsert_resource_link(
        resource_id="40",
        course_id="Mi42YjU4ZDdhMDdkMjE=",
        lesson_id="E2-L01",
        axis_id="Eje 2",
        resource_type="web_page",
        resource_subtype="h5p_video",
    )

    session_id = "verify_moodle_persistence_probe"
    chat = db_service.create_chat(user_id="verify-user", title="Verify Moodle persistence", session_id=session_id)
    user_message = db_service.add_message(session_id, "user", "probe user message")
    assistant_message = db_service.add_message(session_id, "assistant", "probe assistant message")
    db_service.save_trace(
        session_id=session_id,
        message_id=assistant_message["id"],
        trace={"probe": True, "source": "verify_moodle_persistence.py"},
    )
    db_service.save_interaction_trace(
        session_id=session_id,
        question="probe question",
        answer="probe answer",
        context={"probe": True},
        sources=[],
        trace_id="verify-probe",
    )
    db_service.upsert_session_context(
        session_id,
        student_id="verify-user",
        active_context={"current_lesson_id": "E2-L01", "current_resource_id": "40"},
        state={"probe": True},
    )

    messages = db_service.get_chat_messages(session_id, limit=10)
    context = db_service.get_session_context(session_id)

    result = {
        "source": "moodle_db" if db_service.using_moodle_db() else "not_moodle",
        "tables": table_counts,
        "reads": {
            "lessons": len(lessons),
            "E2-L01_blocks": len(blocks),
            "E2-L01_prompts": prompts,
            "links_signed": len(links_signed),
            "links_numeric": len(links_numeric),
        },
        "writes": {
            "link_resource_id": link.get("resource_id"),
            "chat_session_id": chat["session_id"],
            "user_message_id": user_message["id"],
            "assistant_message_id": assistant_message["id"],
            "messages_read_back": len(messages),
            "session_context_read_back": bool(context),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
