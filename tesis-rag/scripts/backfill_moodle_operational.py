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

import argparse
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


def _seed_axes(course_id: str, only_missing: bool) -> int:
    """Siembra los ejes en local_tesisai_axes desde el manifest global + manifests por eje."""
    course_manifest_path = RUNTIME_DIR / "manifest.json"
    if not course_manifest_path.exists():
        return 0
    course_manifest = _read_json(course_manifest_path)
    count = 0
    for axis in course_manifest.get("axes", []):
        axis_id = axis.get("axis_id", "")
        if not axis_id:
            continue
        if only_missing and db_service.get_axis(axis_id, course_id):
            continue
        # Enriquecer con el manifest del eje (pedagogical_role, doc_root, recursos).
        eje_manifest: Dict[str, Any] = {}
        manifest_path = RUNTIME_DIR / "axes" / axis.get("axis_slug", "") / "manifest.json"
        if manifest_path.exists():
            eje_manifest = _read_json(manifest_path)
        db_service.upsert_axis(
            axis_id=axis_id,
            course_id=course_id,
            axis_number=int(axis.get("axis_number", 0) or 0),
            axis_slug=axis.get("axis_slug", ""),
            title=axis.get("axis_title") or eje_manifest.get("axis_title", ""),
            pedagogical_role=eje_manifest.get("pedagogical_role", ""),
            doc_root=eje_manifest.get("doc_root", ""),
            status=axis.get("status", "") or eje_manifest.get("status", ""),
            axis_order=int(axis.get("axis_number", 0) or 0),
            metadata={
                "primary_resources": eje_manifest.get("primary_resources", []),
                "derived_resources": eje_manifest.get("derived_resources", []),
                "seed_file": str(course_manifest_path.relative_to(ROOT)),
            },
        )
        count += 1
    return count


def migrate_runtime_files(course_id: str = COURSE_ID, only_missing: bool = True) -> Dict[str, int]:
    counts = {"axes": 0, "lessons": 0, "resources": 0, "blocks": 0, "prompts": 0, "skipped": 0}

    counts["axes"] = _seed_axes(course_id, only_missing)

    # Recursos: viven en course_runtime/resources/*.json (formato Pydantic Resource).
    for path in sorted((RUNTIME_DIR / "resources").glob("*.json")):
        data = _read_json(path)
        resource_id = data["resource_id"]
        if only_missing and db_service.get_resource(resource_id):
            counts["skipped"] += 1
            continue
        db_service.upsert_resource(
            resource_id=resource_id,
            course_id=course_id,
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

    # Lecciones: viven en course_runtime/axes/eje_N/lessons/<lesson_id>.json.
    # Una lección puede tener bloques de video (segmentación temporal) o no.
    for path in sorted((RUNTIME_DIR / "axes").glob("eje_*/lessons/*.json")):
        data = _read_json(path)
        lesson_id = data["lesson_id"]
        # Seed-safe: si la lección ya existe en BD, no la pisamos (protege ediciones del profe).
        if only_missing and db_service.get_lesson(lesson_id):
            counts["skipped"] += 1
            continue
        blocks = data.get("blocks", []) or []
        resource_id = data.get("resource_id", "")
        resources = data.get("resources") or ([resource_id] if resource_id else [])
        db_service.upsert_lesson(
            lesson_id=lesson_id,
            course_id=course_id,
            axis_id=data.get("axis_id", ""),
            title=data.get("lesson_title") or data.get("title", ""),
            order=int(data.get("order", 0) or 0),
            learning_goal=data.get("learning_goal", ""),
            expected_action=data.get("expected_action", ""),
            learning_goals=data.get("learning_goals", []),
            expected_actions=data.get("expected_actions", []),
            source_script_file=data.get("source_script_file", ""),
            resources=resources,
            prerequisites=data.get("prerequisites", []),
            notes=data.get("notes", ""),
            metadata={"seed_file": str(path.relative_to(ROOT))},
        )
        counts["lessons"] += 1

        db_service.replace_lesson_blocks(lesson_id, blocks)
        counts["blocks"] += len(blocks)

        # Prompts: preferimos los del propio JSON de la lección; si no, los semilla hardcodeada.
        proactive = data.get("proactive_message", "")
        suggested = data.get("suggested_prompts", []) or []
        if not proactive and not suggested and lesson_id in PROMPT_SEEDS:
            proactive = PROMPT_SEEDS[lesson_id].get("proactive", "")
            suggested = PROMPT_SEEDS[lesson_id].get("suggested", [])
        if proactive or suggested:
            db_service.set_lesson_prompts(
                lesson_id,
                proactive_message=proactive,
                suggested_prompts=suggested,
            )
            counts["prompts"] += (1 if proactive else 0) + len(suggested)

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
    parser = argparse.ArgumentParser(description="Backfill operativo course_runtime -> BD Moodle.")
    parser.add_argument("--course-id", default=COURSE_ID, help="course_id destino (default: %(default)s).")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-siembra TODO desde JSON, pisando lo que exista en BD (peligroso: borra ediciones del profe).",
    )
    parser.add_argument(
        "--skip-legacy-sqlite",
        action="store_true",
        help="No migrar sesiones/mensajes legacy de bd_chat/chats.db.",
    )
    args = parser.parse_args()

    db_service.init_db()
    runtime_counts = migrate_runtime_files(course_id=args.course_id, only_missing=not args.force)
    sqlite_counts = {} if args.skip_legacy_sqlite else migrate_sqlite_operational()
    backend = "moodle_db" if db_service.using_moodle_db() else "sqlite_fallback"
    print(json.dumps({
        "backend": backend,
        "course_id": args.course_id,
        "mode": "force" if args.force else "only_missing",
        "runtime": runtime_counts,
        "sqlite_legacy": sqlite_counts,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
