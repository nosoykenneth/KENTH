"""
Servicio de lecciones piloto del tutor contextual KENTH.

Vertical slice fase 1: solo carga los manifiestos piloto bajo
`course_runtime/pilot/`, resuelve el bloque activo segun timestamp y
expone el bloque para que el `context_service` lo inyecte al envelope.

NO toca:
- el RAG documental por ejes (Capa 1)
- los manifiestos generales en `course_runtime/lessons|resources/`
- la base vectorial
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from services import db_service


_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PILOT_DIR = os.path.join(_BASE_DIR, "course_runtime", "pilot")
_PILOT_MANIFEST = os.path.join(_PILOT_DIR, "manifest.json")


# ==========================================
# CARGADORES
# ==========================================

def _load_json(path: str) -> Optional[dict]:
    if not os.path.exists(path):
        return None
    print(f"[DB FALLBACK] source=json entity=pilot reason=pilot_manifest_or_lesson_missing_in_moodle path={path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_pilot_manifest() -> dict:
    lessons = db_service.list_lessons(is_pilot=True)
    if lessons:
        return {
            "lessons": [
                {
                    "lesson_id": lesson.get("lesson_id", ""),
                    "axis_id": lesson.get("axis_id", ""),
                    "lesson_title": lesson.get("title", ""),
                    "learning_goal": lesson.get("learning_goal", ""),
                    "expected_action": lesson.get("expected_action", ""),
                }
                for lesson in lessons
            ]
        }
    data = _load_json(_PILOT_MANIFEST)
    return data or {"lessons": []}


def load_pilot_lesson(lesson_id: str) -> Optional[dict]:
    """Devuelve el manifiesto plano de una leccion piloto.

    Mantiene el shape exacto del archivo JSON (lesson_id, axis_id,
    lesson_title, resource_id, resource_type, source_script_file,
    learning_goal, expected_action, blocks).
    """
    if not lesson_id:
        return None
    row = db_service.get_lesson(lesson_id)
    if row and row.get("is_pilot"):
        resources = row.get("resources", []) or []
        resource_id = resources[0] if resources else ""
        resource = db_service.get_resource(resource_id) if resource_id else None
        return {
            "lesson_id": row.get("lesson_id", ""),
            "axis_id": row.get("axis_id", ""),
            "lesson_title": row.get("title", ""),
            "resource_id": resource_id,
            "resource_type": resource.type.value if resource else "",
            "source_script_file": row.get("source_script_file", ""),
            "learning_goal": row.get("learning_goal", ""),
            "expected_action": row.get("expected_action", ""),
            "suggested_prompts": row.get("suggested_prompts", []),
            "proactive_message": row.get("proactive_message", ""),
            "blocks": db_service.list_lesson_blocks(lesson_id),
        }
    path = os.path.join(_PILOT_DIR, f"{lesson_id}.json")
    return _load_json(path)


def list_pilot_lessons() -> List[dict]:
    """Lista resumida de las lecciones piloto disponibles."""
    manifest = load_pilot_manifest()
    return manifest.get("lessons", [])


def is_pilot_lesson(lesson_id: str) -> bool:
    if not lesson_id:
        return False
    return any(item.get("lesson_id") == lesson_id for item in list_pilot_lessons())


# ==========================================
# RESOLUCION DE BLOQUE POR TIMESTAMP
# ==========================================

def find_block_at_timestamp(lesson: dict, timestamp: Optional[float]) -> Optional[dict]:
    """Devuelve el bloque del video cuyo rango contiene el timestamp.

    Si timestamp es None, devuelve None (el caller decide que hacer).
    Si el timestamp queda fuera de todos los rangos, devuelve el bloque
    mas cercano por start_time. Esto evita que un timestamp ligeramente
    fuera por floating-point pierda el bloque actual.
    """
    if not lesson:
        return None
    blocks = lesson.get("blocks") or []
    if not blocks:
        return None
    if timestamp is None:
        return None

    for block in blocks:
        start = float(block.get("start_time", 0))
        end = float(block.get("end_time", 0))
        if start <= timestamp <= end:
            return block

    # fallback: el bloque cuyo rango este mas cerca del timestamp
    def _distance(b: dict) -> float:
        start = float(b.get("start_time", 0))
        end = float(b.get("end_time", 0))
        if timestamp < start:
            return start - timestamp
        if timestamp > end:
            return timestamp - end
        return 0.0

    return min(blocks, key=_distance)


def resolve_pilot_block(
    lesson_id: str,
    timestamp: Optional[float],
) -> Dict[str, Optional[dict]]:
    """Atajo: devuelve {lesson, block} o {lesson: None, block: None}.

    No lanza excepciones si la leccion no es piloto: simplemente
    devuelve None para que el flujo degrade limpio.
    """
    lesson = load_pilot_lesson(lesson_id)
    if not lesson:
        return {"lesson": None, "block": None}
    block = find_block_at_timestamp(lesson, timestamp)
    return {"lesson": lesson, "block": block}
