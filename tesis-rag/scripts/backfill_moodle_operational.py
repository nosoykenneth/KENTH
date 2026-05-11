"""
Backfill de persistencia operativa hacia la BD de Moodle.

Origenes migrados:
- course_runtime/lessons/*.json y resources/*.json como semillas operativas.
- course_runtime/pilot/*.json como lecciones/bloques piloto.
- prompts sugeridos antes hardcodeados en frontend.
- bd_chat/chats.db: sesiones, mensajes, trazas y vinculos recurso -> leccion.

No migra contenido editorial ni corpus RAG.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path.insert(0, str(ROOT))

from services import db_service  # noqa: E402


COURSE_ID = "curso_mezcla_masterizacion"
SQLITE_DB = ROOT / "bd_chat" / "chats.db"
RUNTIME_DIR = ROOT / "course_runtime"
PROMPT_SEEDS: Dict[str, Dict[str, Any]] = {
    "E2-L01": {
        "proactive": "Estoy viendo que estas en E2-L01 (HPF y LPF). Si quieres, te ayudo con filtros, punto de corte o pendiente.",
        "suggested": [
            "Corto en solo o en mezcla?",
            "Como se si esto es basura o cuerpo real?",
            "Pendiente fuerte siempre es mejor?",
        ],
    },
    "E3-L03": {
        "proactive": "Estas en E3-L03. Puedo ayudarte a distinguir EQ correctivo y EQ estetico.",
        "suggested": [
            "Que diferencia hay entre EQ correctivo y estetico?",
            "Esto lo evaluo en solo o en contexto?",
            "El barrido es para dejar el boost?",
        ],
    },
    "E4-L01": {
        "proactive": "Estas en E4-L01. Puedo ayudarte con threshold, ratio y knee.",
        "suggested": [
            "Que hace realmente el threshold?",
            "Ratio alto significa mejor control?",
            "Soft knee siempre es mejor para voz?",
        ],
    },
}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rows(table: str) -> Iterable[sqlite3.Row]:
    if not SQLITE_DB.exists():
        return []
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    try:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,),
        ).fetchone()
        if not exists:
            return []
        return [row for row in conn.execute(f"SELECT * FROM {table}")]
    finally:
        conn.close()


def _json(value: Any, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except Exception:
        return fallback


def migrate_runtime_files() -> Dict[str, int]:
    counts = {"lessons": 0, "resources": 0, "pilot_lessons": 0, "blocks": 0, "prompts": 0}

    for path in sorted((RUNTIME_DIR / "lessons").glob("*.json")):
        data = _read_json(path)
        db_service.upsert_lesson(
            lesson_id=data["lesson_id"],
            course_id=COURSE_ID,
            axis_id=data.get("axis_id", ""),
            title=data.get("title", ""),
            order=int(data.get("order", 0) or 0),
            learning_goals=data.get("learning_goals", []),
            expected_actions=data.get("expected_actions", []),
            resources=data.get("resources", []),
            prerequisites=data.get("prerequisites", []),
            notes=data.get("notes", ""),
            metadata={"seed_file": str(path.relative_to(ROOT))},
        )
        counts["lessons"] += 1

    for path in sorted((RUNTIME_DIR / "resources").glob("*.json")):
        data = _read_json(path)
        db_service.upsert_resource(
            resource_id=data["resource_id"],
            course_id=COURSE_ID,
            axis_id=data.get("axis_id", ""),
            lesson_id=data.get("lesson_id", ""),
            resource_type=data.get("type", "lesson_note"),
            title=data.get("title", ""),
            source_uri=data.get("source_uri", ""),
            duration_seconds=data.get("duration_seconds"),
            page_count=data.get("page_count"),
            language=data.get("language", "es"),
            tags=data.get("tags", []),
            metadata={**data.get("metadata", {}), "seed_file": str(path.relative_to(ROOT))},
        )
        counts["resources"] += 1

    for path in sorted((RUNTIME_DIR / "pilot").glob("E*-L*.json")):
        data = _read_json(path)
        blocks = data.get("blocks", [])
        resource_id = data.get("resource_id", "")
        db_service.upsert_lesson(
            lesson_id=data["lesson_id"],
            course_id=COURSE_ID,
            axis_id=data.get("axis_id", ""),
            title=data.get("lesson_title", ""),
            order=0,
            learning_goal=data.get("learning_goal", ""),
            expected_action=data.get("expected_action", ""),
            source_script_file=data.get("source_script_file", ""),
            is_pilot=True,
            resources=[resource_id] if resource_id else [],
            metadata={"seed_file": str(path.relative_to(ROOT))},
        )
        counts["pilot_lessons"] += 1

        if resource_id:
            db_service.upsert_resource(
                resource_id=resource_id,
                course_id=COURSE_ID,
                axis_id=data.get("axis_id", ""),
                lesson_id=data["lesson_id"],
                resource_type=data.get("resource_type", "video"),
                title=data.get("lesson_title", ""),
                source_uri=data.get("source_script_file", ""),
                metadata={"seed_file": str(path.relative_to(ROOT)), "derived_from_pilot": True},
            )

        for idx, block in enumerate(blocks):
            db_service.upsert_lesson_block(
                block_id=block["block_id"],
                lesson_id=data["lesson_id"],
                block_order=idx,
                start_time=block.get("start_time"),
                end_time=block.get("end_time"),
                block_title=block.get("block_title", ""),
                summary=block.get("summary", ""),
                interaction_mode=block.get("interaction_mode", ""),
                tutor_focus=block.get("tutor_focus", ""),
                concepts=block.get("concepts", []),
                preguntas_probables=block.get("preguntas_probables", []),
                metadata={"seed_file": str(path.relative_to(ROOT))},
            )
            counts["blocks"] += 1

    for lesson_id, prompts in PROMPT_SEEDS.items():
        if prompts.get("proactive"):
            db_service.upsert_lesson_prompt(lesson_id, "proactive", prompts["proactive"], 0)
            counts["prompts"] += 1
        for order, text in enumerate(prompts.get("suggested", [])):
            db_service.upsert_lesson_prompt(lesson_id, "suggested", text, order)
            counts["prompts"] += 1

    return counts


def migrate_sqlite_operational() -> Dict[str, int]:
    counts = {"chats": 0, "messages": 0, "message_traces": 0, "interaction_traces": 0, "links": 0}
    if not SQLITE_DB.exists():
        return counts

    for row in _rows("chats"):
        db_service.create_chat(
            user_id=row["user_id"] or "",
            title=row["title"] or "Nuevo chat",
            session_id=row["id"],
        )
        counts["chats"] += 1

    for row in _rows("messages"):
        db_service.ensure_chat_exists(row["chat_id"])
        db_service.add_message(row["chat_id"], row["role"], row["content"] or "")
        counts["messages"] += 1

    for row in _rows("message_traces"):
        trace = _json(row["trace_json"], {})
        if not trace:
            trace = {
                "ruta": row["ruta"],
                "evidence_level": row["evidence_level"],
                "fuentes": _json(row["fuentes_json"], []),
            }
        db_service.save_trace(
            session_id=f"legacy_trace_{row['message_id'] or row['id']}",
            message_id=None,
            trace=trace,
        )
        counts["message_traces"] += 1

    for row in _rows("interaction_traces"):
        trace = _json(row["trace_json"], {})
        session_id = row["session_id"] or "legacy_interactions"
        db_service.save_interaction_trace(
            session_id=session_id,
            question=trace.get("question", ""),
            answer=trace.get("answer", ""),
            context=trace,
            sources=trace.get("sources", []),
        )
        counts["interaction_traces"] += 1

    for row in _rows("resource_lesson_links"):
        db_service.upsert_resource_link(
            resource_id=row["resource_id"],
            course_id=row["course_id"] or "",
            lesson_id=row["lesson_id"],
            axis_id=row["axis_id"] or "",
            resource_type=row["resource_type"] or "",
            resource_subtype=row["resource_subtype"] or "",
        )
        counts["links"] += 1

    return counts


def main() -> None:
    db_service.init_db()
    runtime_counts = migrate_runtime_files()
    sqlite_counts = migrate_sqlite_operational()
    backend = "moodle_db" if db_service.using_moodle_db() else "sqlite_fallback"
    print(json.dumps({
        "backend": backend,
        "runtime": runtime_counts,
        "sqlite_legacy": sqlite_counts,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
