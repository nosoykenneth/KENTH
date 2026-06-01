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


def _axis_dir(axis_slug_or_number: str) -> Optional[str]:
    """Resuelve la carpeta del eje a partir de un slug ("eje_0") o número ("0", "Eje 0")."""
    if not axis_slug_or_number:
        return None
    raw = str(axis_slug_or_number).strip()
    candidates = []
    if raw.startswith("eje_"):
        candidates.append(raw)
    if raw.lower().startswith("eje "):
        candidates.append(f"eje_{raw.split()[-1]}")
    if raw.isdigit():
        candidates.append(f"eje_{raw}")
    candidates.append(raw)
    for slug in candidates:
        path = os.path.join(_AXES_DIR, slug)
        if os.path.isdir(path):
            return path
    return None


def _canonical_axis_id(axis_id: str) -> str:
    """Normaliza 'eje_2' / '2' / 'Eje 2' a la forma canónica 'Eje 2' (la que vive en BD)."""
    if not axis_id:
        return ""
    raw = str(axis_id).strip()
    if raw.lower().startswith("eje_"):
        return f"Eje {raw.split('_', 1)[1]}"
    if raw.lower().startswith("eje "):
        return f"Eje {raw.split()[-1]}"
    if raw.isdigit():
        return f"Eje {raw}"
    return raw


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
# MANIFEST POR EJE
# ==========================================

def _axis_manifest_from_db(db_axis: dict, course_id: Optional[str] = None) -> dict:
    """Construye un manifest de eje (shape compatible con el JSON) desde la fila de BD."""
    canonical = db_axis.get("axis_id", "")
    lessons = [row.get("lesson_id", "") for row in db_service.list_lessons(axis_id=canonical, course_id=course_id)]
    meta = db_axis.get("metadata", {}) or {}
    return {
        "axis_id": canonical,
        "axis_number": db_axis.get("axis_number", 0),
        "axis_slug": db_axis.get("axis_slug", ""),
        "axis_title": db_axis.get("axis_title") or db_axis.get("title", ""),
        "pedagogical_role": db_axis.get("pedagogical_role", ""),
        "doc_root": db_axis.get("doc_root", ""),
        "primary_resources": meta.get("primary_resources", []),
        "derived_resources": meta.get("derived_resources", []),
        "lessons": lessons,
        "status": db_axis.get("status", ""),
    }


def load_axis_manifest(axis_id: str, course_id: Optional[str] = None) -> Optional[dict]:
    """Manifiesto del eje (axis_id puede ser 'Eje 0', 'eje_0' o '0').

    Resolución: BD (local_tesisai_axes) primero. El fallback al JSON
    course_runtime/axes/eje_N/manifest.json **solo aplica en modo legacy/mono-curso**:
    si el llamador pidió un course_id explícito y la BD no lo conoce, se devuelve
    None (estricto multi-curso — no fugar contenido de otro curso).
    """
    db_axis = db_service.get_axis(_canonical_axis_id(axis_id), course_id)
    if db_axis:
        return _axis_manifest_from_db(db_axis, course_id)
    if course_id:
        return None
    folder = _axis_dir(axis_id)
    if not folder:
        return None
    return _load_json(os.path.join(folder, "manifest.json"))


def list_axes(course_id: Optional[str] = None) -> List[dict]:
    """Lista todos los ejes (orden por axis_number).

    DB-first. El escaneo de carpetas `course_runtime/axes/eje_N/manifest.json`
    **solo aplica en modo legacy/mono-curso** (sin course_id). Si el llamador
    pidió un course_id específico y la BD no devuelve ejes para ese curso, se
    devuelve [] — no se filtra contenido global del JSON para aislar cursos.
    """
    db_axes = db_service.list_axes(course_id)
    if db_axes:
        out = [_axis_manifest_from_db(a, course_id) for a in db_axes]
        out.sort(key=lambda a: a.get("axis_number", 99))
        return out
    if course_id:
        return []
    if not os.path.isdir(_AXES_DIR):
        return []
    axes: List[dict] = []
    for entry in sorted(os.listdir(_AXES_DIR)):
        manifest_path = os.path.join(_AXES_DIR, entry, "manifest.json")
        data = _load_json(manifest_path)
        if data:
            axes.append(data)
    axes.sort(key=lambda a: a.get("axis_number", 99))
    return axes


# ==========================================
# LECCIONES
# ==========================================

def load_lesson(lesson_id: str, course_id: Optional[str] = None) -> Optional[dict]:
    """Devuelve la lección como dict plano.

    Mantiene el mismo shape que las antiguas lecciones piloto:
    lesson_id, axis_id, lesson_title, resource_id, resource_type,
    learning_goal, expected_action, blocks, learning_goals,
    expected_actions, resources, prerequisites.

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
            "lesson_title": row.get("title", ""),
            "order": row.get("order", 0),
            "resource_id": resource_id,
            "resource_type": resource.type.value if resource else "",
            "source_script_file": row.get("source_script_file", ""),
            "learning_goal": row.get("learning_goal", ""),
            "expected_action": row.get("expected_action", ""),
            "learning_goals": row.get("learning_goals", []),
            "expected_actions": row.get("expected_actions", []),
            "resources": resources,
            "prerequisites": row.get("prerequisites", []),
            "suggested_prompts": row.get("suggested_prompts", []),
            "proactive_message": row.get("proactive_message", ""),
            "blocks": db_service.list_lesson_blocks(lesson_id),
            "notes": row.get("notes", ""),
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
                "axis_service.fallback_json",
                extra={"entity": "lesson", "lesson_id": lesson_id, "path": lesson_path},
            )
            return _load_json(lesson_path)
    return None


def _lesson_summary(lesson: dict) -> dict:
    return {
        "lesson_id": lesson.get("lesson_id", ""),
        "axis_id": lesson.get("axis_id", ""),
        "lesson_title": lesson.get("lesson_title", ""),
        "order": lesson.get("order", 0),
        "learning_goal": lesson.get("learning_goal", ""),
        "expected_action": lesson.get("expected_action", ""),
        "has_blocks": bool(lesson.get("blocks")),
    }


def list_lessons_of_axis(axis_id: str, course_id: Optional[str] = None) -> List[dict]:
    """Lista las lecciones de un eje en formato resumido.

    DB-first: deriva las lecciones de la BD por axis_id (así una lección creada
    por el panel del profesor aparece sin tocar JSON). Fallback: lecciones del
    manifest JSON del eje.
    """
    canonical = _canonical_axis_id(axis_id)
    db_rows = db_service.list_lessons(axis_id=canonical, course_id=course_id)
    if db_rows:
        out = []
        for row in db_rows:
            summary = _lesson_summary(row)
            summary["has_blocks"] = bool(db_service.list_lesson_blocks(row.get("lesson_id", "")))
            out.append(summary)
        out.sort(key=lambda l: l.get("order", 99))
        return out
    if course_id:
        return []

    manifest = load_axis_manifest(axis_id, course_id)
    if not manifest:
        return []
    out = []
    for lesson_id in manifest.get("lessons", []):
        lesson = load_lesson(lesson_id, course_id)
        if not lesson:
            continue
        out.append(_lesson_summary(lesson))
    out.sort(key=lambda l: l.get("order", 99))
    return out


def list_all_lessons(course_id: Optional[str] = None) -> List[dict]:
    """Lista resumida de todas las lecciones del curso (todos los ejes)."""
    out: List[dict] = []
    for axis in list_axes(course_id):
        out.extend(list_lessons_of_axis(axis.get("axis_id", ""), course_id))
    return out


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


def list_resources_of_axis(axis_id: str, course_id: Optional[str] = None) -> List[dict]:
    """Lista los recursos declarados en el manifest del eje."""
    manifest = load_axis_manifest(axis_id, course_id) or {}
    ids = (manifest.get("primary_resources", []) or []) + (manifest.get("derived_resources", []) or [])
    out: List[dict] = []
    for rid in ids:
        data = load_resource(rid)
        if data:
            out.append(data)
    return out


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
