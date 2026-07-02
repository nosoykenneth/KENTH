"""Persistencia del asistente: guardar borrador y PROMOVER al aceptar (Fases 4 y 10).

Modelo de datos (decisión "draft aislado + promover al aceptar"):
  - El borrador vive en `metadata.ai_prepare` y NO alimenta al tutor.
  - El tutor solo usa los campos VIVOS (learning_goal, delegated_to_tutor,
    attribution_constraints, metadata.pedagogy.*, y los campos pedagógicos de los
    bloques) — que se pueblan SOLO cuando el profesor ACEPTA.
  - Aceptar promueve los campos no vacíos (replace) y funde los momentos en los
    bloques EXISTENTES preservando timestamps/orden (mismo muro que /moments).

requires_reindex al aceptar es FALSE a propósito: estos campos se INYECTAN en el
prompt, no se INDEXAN en Chroma (arquitectura inject-vs-index del proyecto). La
transcripción —lo único que sí se indexa— tiene su propio flujo.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from services import db_service
from services import pedagogy_profile


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_draft(
    lesson_id: str,
    course_id: str,
    user_id: str,
    result: Dict[str, Any],
    quality: str,
) -> Optional[Dict[str, Any]]:
    """Guarda el borrador generado en metadata.ai_prepare (aislado) + estados."""
    draft = result.get("draft") or {}
    review = result.get("review")
    model_info = result.get("models") or {}
    status = "reviewed" if review else "draft"
    patch = {
        "ai_prepared": True,
        "ai_prepare_status": status,
        "requires_review": True,
        # El borrador NO cambia el índice; solo al aceptar cambian campos inyectados.
        "requires_reindex": False,
        "ai_prepare_model": model_info.get("draft_model"),
        "ai_prepare_review_model": model_info.get("review_model"),
        "ai_prepared_at": _now_iso(),
        "ai_prepared_by": user_id,
        "ai_prepare": {
            "draft": draft,
            "review": review,
            "quality": quality,
            "repaired": result.get("repaired", False),
            "transcript_info": result.get("transcript_info", {}),
            "elapsed_seconds": result.get("elapsed_seconds"),
            "generated_at": _now_iso(),
        },
    }
    return db_service.merge_lesson_metadata(lesson_id, course_id, patch)


def save_review_only(
    lesson_id: str, course_id: str, user_id: str, review: Dict[str, Any], review_model: Optional[str]
) -> Optional[Dict[str, Any]]:
    """Modo review: adjunta una revisión al borrador existente sin regenerarlo."""
    lesson = db_service.get_lesson(lesson_id, course_id)
    if not lesson:
        return None
    meta = dict(lesson.get("metadata") or {})
    ai = dict(meta.get("ai_prepare") or {})
    ai["review"] = review
    ai["reviewed_at"] = _now_iso()
    patch = {
        "ai_prepare": ai,
        "ai_prepare_status": "reviewed",
        "ai_prepare_review_model": review_model,
        "requires_review": True,
    }
    return db_service.merge_lesson_metadata(lesson_id, course_id, patch)


def _draft_to_profile(draft: Dict[str, Any]) -> Dict[str, Any]:
    """Traduce el borrador IA al perfil pedagógico CANÓNICO (nombres unificados)."""
    return {
        "learning_goal": draft.get("learning_goal", ""),
        "lesson_summary": draft.get("lesson_summary", ""),
        "tutor_tone": draft.get("recommended_tone", ""),
        "help_level": draft.get("recommended_help_level", ""),
        "lesson_rules": draft.get("lesson_rules", []),
        "key_concepts": draft.get("key_concepts", []),
        "common_mistakes": draft.get("common_mistakes", []),
        "probable_questions": draft.get("probable_questions", []),
        "tutor_focus": draft.get("tutor_focus", []),
        "tutor_must_not_do": draft.get("tutor_must_not_do", []),
        # La IA no genera prompts al alumno; se omiten (merge conserva lo existente).
        "moments": draft.get("moments", []),
    }


def promote_draft(
    lesson_id: str,
    course_id: str,
    user_id: str,
    draft: Dict[str, Any],
    *,
    apply_moments: bool = True,
) -> Dict[str, Any]:
    """Promueve un borrador (ya validado) al PERFIL CANÓNICO vivo del tutor.

    Reusa el MISMO escritor que los editores (`pedagogy_profile.apply_profile`),
    en modo "merge" (los campos vacíos del borrador NO borran lo previo). Así la IA
    y la edición manual rellenan el mismo modelo. Luego marca el estado de aceptación.
    """
    lesson = db_service.get_lesson(lesson_id, course_id)
    if not lesson:
        return {"ok": False, "error": "Lección no encontrada."}

    summary = pedagogy_profile.apply_profile(
        lesson_id, course_id, user_id, _draft_to_profile(draft),
        mode="merge", apply_moments=apply_moments,
    )
    if not summary.get("ok"):
        return summary

    # Estado de aceptación. requires_reindex=False (campos inyectados, no indexados).
    db_service.merge_lesson_metadata(lesson_id, course_id, {
        "ai_prepared": True,
        "ai_prepare_status": "accepted",
        "requires_review": False,
        "requires_reindex": False,
        "teacher_reviewed_at": _now_iso(),
        "teacher_reviewed_by": user_id,
        "ai_prepare": {**((lesson.get("metadata") or {}).get("ai_prepare") or {}), "accepted_draft": draft},
    })

    return {
        "ok": True,
        "changed": summary.get("changed", []),
        "moments_applied": summary.get("moments_applied", 0),
        "requires_reindex": False,
    }
