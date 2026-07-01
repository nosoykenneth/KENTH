"""
Servicio de ejes y lecciones del tutor contextual KENTH.

Reemplaza al antiguo `pilot_service`: la capa operativa ya no se llama
"piloto" sino que es la estructura formal de 8 ejes bajo
`course_runtime/axes/eje_N/`.

Responsabilidades:
- Cargar el manifiesto global del curso y los manifests por eje.
- Cargar lecciones individuales por lesson_id (desde DB Moodle primero,
  fallback a JSON en `course_runtime/axes/eje_N/lessons/<lesson_id>.json`).
- Resolver el bloque activo de una lección dada un timestamp de video.
- Listar y filtrar lecciones por eje.

NO toca:
- el RAG documental por ejes (Capa 1, base vectorial)
- los servicios de chat ni de sesión
"""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Dict, List, Optional

from services import db_service


_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RUNTIME_DIR = os.path.join(_BASE_DIR, "course_runtime")
_AXES_DIR = os.path.join(_RUNTIME_DIR, "axes")
_RESOURCES_DIR = os.path.join(_RUNTIME_DIR, "resources")
_COURSE_MANIFEST = os.path.join(_RUNTIME_DIR, "manifest.json")


logger = logging.getLogger(__name__)


# ==========================================
# CARGADORES (helpers)
# ==========================================

def _load_json(path: str) -> Optional[dict]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================
# MANIFEST GLOBAL DEL CURSO
# ==========================================

def load_course_manifest() -> dict:
    """Carga el manifest global con la lista de los 8 ejes y sus lecciones.

    Si la BD Moodle tiene lecciones, las usa para enriquecer; si no,
    cae al archivo JSON de course_runtime/manifest.json.
    """
    manifest = _load_json(_COURSE_MANIFEST) or {
        "course_id": "curso_mezcla_masterizacion",
        "axes": [],
    }

    db_lessons = db_service.list_lessons()
    if db_lessons:
        by_axis: Dict[str, List[str]] = {}
        for row in db_lessons:
            by_axis.setdefault(row.get("axis_id", ""), []).append(row.get("lesson_id", ""))
        for axis in manifest.get("axes", []):
            db_ids = by_axis.get(axis.get("axis_id", ""), [])
            if db_ids:
                axis["lessons"] = db_ids
    return manifest


# ==========================================
# LECCIONES
# ==========================================

def load_lesson(lesson_id: str, course_id: Optional[str] = None) -> Optional[dict]:
    """Devuelve la lección como dict plano.

    Shape: lesson_id, axis_id, lesson_title, resource_id, resource_type,
    learning_goal, learning_goals (criterios de logro), expected_action,
    prerequisites, delegated_to_tutor, attribution_constraints, prompts,
    blocks, notes (interno del profe, no se inyecta).

    Resolución:
      1. Intenta DB (`db_service.get_lesson`) — Moodle si está disponible.
      2. Fallback: lee JSON en `axes/eje_N/lessons/<lesson_id>.json`.
    """
    if not lesson_id:
        return None

    row = db_service.get_lesson(lesson_id, course_id)
    if row:
        resources = row.get("resources", []) or []
        resource_id = resources[0] if resources else ""
        resource = db_service.get_resource(resource_id) if resource_id else None
        return {
            "lesson_id": row.get("lesson_id", ""),
            "axis_id": row.get("axis_id", ""),
            "moodle_section_id": row.get("moodle_section_id", ""),
            "lesson_title": row.get("title", ""),
            "order": row.get("order", 0),
            "resource_id": resource_id,
            "resource_type": resource.type.value if resource else "",
            "learning_goal": row.get("learning_goal", ""),
            "expected_action": row.get("expected_action", ""),
            "learning_goals": row.get("learning_goals", []),
            "resources": resources,
            "prerequisites": row.get("prerequisites", []),
            "delegated_to_tutor": row.get("delegated_to_tutor", []),
            "attribution_constraints": row.get("attribution_constraints", []),
            "suggested_prompts": row.get("suggested_prompts", []),
            "proactive_message": row.get("proactive_message", ""),
            "blocks": db_service.list_lesson_blocks(lesson_id),
            "notes": row.get("notes", ""),
            # metadata incluye pedagogy (tono/nivel/reglas/errores) que el profesor
            # personaliza; se inyecta de forma aditiva en render_context_block.
            "metadata": row.get("metadata", {}) or {},
        }

    if course_id:
        return None
    return _find_lesson_in_axes(lesson_id)


def _find_lesson_in_axes(lesson_id: str) -> Optional[dict]:
    """Busca el JSON de la lección recorriendo axes/eje_N/lessons/."""
    if not os.path.isdir(_AXES_DIR):
        return None
    for entry in os.listdir(_AXES_DIR):
        lesson_path = os.path.join(_AXES_DIR, entry, "lessons", f"{lesson_id}.json")
        if os.path.exists(lesson_path):
            logger.info(
                "lesson_service.fallback_json",
                extra={"entity": "lesson", "lesson_id": lesson_id, "path": lesson_path},
            )
            return _load_json(lesson_path)
    return None


def _lesson_summary(lesson: dict) -> dict:
    return {
        "lesson_id": lesson.get("lesson_id", ""),
        "axis_id": lesson.get("axis_id", ""),
        "moodle_section_id": lesson.get("moodle_section_id", ""),
        "lesson_title": lesson.get("lesson_title", ""),
        "order": lesson.get("order", 0),
        "learning_goal": lesson.get("learning_goal", ""),
        "expected_action": lesson.get("expected_action", ""),
        "has_blocks": bool(lesson.get("blocks")),
    }


def is_known_lesson(lesson_id: str, course_id: Optional[str] = None) -> bool:
    """True si la lección existe (en DB o como JSON en algún eje)."""
    if not lesson_id:
        return False
    return load_lesson(lesson_id, course_id) is not None


# ==========================================
# RECURSOS
# ==========================================

def load_resource(resource_id: str) -> Optional[dict]:
    """Carga el manifest de un recurso (json plano)."""
    if not resource_id:
        return None
    path = os.path.join(_RESOURCES_DIR, f"{resource_id}.json")
    return _load_json(path)


# ==========================================
# RESOLUCION DE BLOQUE POR TIMESTAMP
# ==========================================

def find_block_at_timestamp(lesson: dict, timestamp: Optional[float]) -> Optional[dict]:
    """Devuelve el bloque del video cuyo rango contiene el timestamp.

    Reglas:
      - Si la lección no tiene blocks o el timestamp es None → None.
      - Si el timestamp queda dentro de algún bloque → ese bloque.
      - Si queda fuera de todos los rangos → bloque más cercano por
        distancia (evita perder el bloque actual por floating-point).
    """
    if not lesson:
        return None
    blocks = lesson.get("blocks") or []
    if not blocks or timestamp is None:
        return None

    for block in blocks:
        start = float(block.get("start_time", 0))
        end = float(block.get("end_time", 0))
        if start <= timestamp <= end:
            return block

    def _distance(b: dict) -> float:
        start = float(b.get("start_time", 0))
        end = float(b.get("end_time", 0))
        if timestamp < start:
            return start - timestamp
        if timestamp > end:
            return timestamp - end
        return 0.0

    return min(blocks, key=_distance)


def resolve_lesson_block(
    lesson_id: str,
    timestamp: Optional[float],
) -> Dict[str, Optional[dict]]:
    """Atajo: devuelve {lesson, block} o {lesson: None, block: None}.

    No lanza excepciones si la lección no existe: degrada limpio.
    """
    lesson = load_lesson(lesson_id)
    if not lesson:
        return {"lesson": None, "block": None}
    block = find_block_at_timestamp(lesson, timestamp)
    return {"lesson": lesson, "block": block}
