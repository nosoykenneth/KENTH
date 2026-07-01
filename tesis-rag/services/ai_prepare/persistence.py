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
from typing import Any, Dict, List, Optional

from services import db_service


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


def _apply_moments_to_blocks(
    existing_blocks: List[Dict[str, Any]], moments: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Funde los campos pedagógicos de los momentos en los bloques EXISTENTES.

    Solo por block_id que ya existe. Preserva start/end/order/interaction_mode/metadata.
    Los momentos con existing_block_id nulo/desconocido se IGNORAN (crear bloques es
    estructura técnica = admin, no se hace al aceptar un borrador).
    """
    by_id: Dict[str, Dict[str, Any]] = {}
    for m in moments or []:
        bid = str(m.get("existing_block_id") or "").strip()
        if bid:
            by_id[bid] = m
    merged: List[Dict[str, Any]] = []
    for b in existing_blocks:
        bid = str(b.get("block_id"))
        m = by_id.get(bid)
        merged.append({
            "block_id": bid,
            "block_order": b.get("block_order"),
            "start_time": b.get("start_time"),      # preservado
            "end_time": b.get("end_time"),          # preservado
            "block_title": (m.get("title") if m and m.get("title") else b.get("block_title", "")),
            "summary": (m.get("summary") if m and m.get("summary") else b.get("summary", "")),
            "interaction_mode": b.get("interaction_mode", ""),
            "tutor_focus": (m.get("pedagogical_intent") if m and m.get("pedagogical_intent") else b.get("tutor_focus", "")),
            "concepts": (m.get("key_concepts") if m and m.get("key_concepts") else b.get("concepts", [])),
            "preguntas_probables": (m.get("probable_questions") if m and m.get("probable_questions") else b.get("preguntas_probables", [])),
            "metadata": b.get("metadata", {}),
        })
    return merged


def promote_draft(
    lesson_id: str,
    course_id: str,
    user_id: str,
    draft: Dict[str, Any],
    *,
    apply_moments: bool = True,
) -> Dict[str, Any]:
    """Promueve un borrador (ya validado) a los campos VIVOS del tutor.

    `draft` es el borrador final aprobado por el profesor (puede haberlo editado).
    Solo se promueven los campos no vacíos (replace); los vacíos no borran lo previo.
    Devuelve un resumen de lo aplicado.
    """
    lesson = db_service.get_lesson(lesson_id, course_id)
    if not lesson:
        return {"ok": False, "error": "Lección no encontrada."}

    changed: List[str] = []

    # 1) Campos vivos de la lección (inyectados por el tutor).
    learning_goal = (draft.get("learning_goal") or "").strip()
    tutor_focus = draft.get("tutor_focus") or []           # -> delegated_to_tutor
    must_not = draft.get("tutor_must_not_do") or []        # -> attribution_constraints

    new_learning_goal = learning_goal or lesson.get("learning_goal", "") or ""
    new_delegated = tutor_focus if tutor_focus else (lesson.get("delegated_to_tutor", []) or [])
    new_attribution = must_not if must_not else (lesson.get("attribution_constraints", []) or [])
    if learning_goal:
        changed.append("learning_goal")
    if tutor_focus:
        changed.append("delegated_to_tutor")
    if must_not:
        changed.append("attribution_constraints")

    # 2) metadata.pedagogy (lo que ya consume render_context_block).
    meta = dict(lesson.get("metadata") or {})
    ped = dict(meta.get("pedagogy") or {})
    if draft.get("recommended_tone"):
        ped["tutor_tone"] = draft["recommended_tone"]; changed.append("pedagogy.tutor_tone")
    if draft.get("recommended_help_level"):
        ped["help_level"] = draft["recommended_help_level"]; changed.append("pedagogy.help_level")
    if draft.get("lesson_rules"):
        ped["lesson_rules"] = "\n".join(draft["lesson_rules"]); changed.append("pedagogy.lesson_rules")
    if draft.get("common_mistakes"):
        ped["common_mistakes"] = draft["common_mistakes"]; changed.append("pedagogy.common_mistakes")
    meta["pedagogy"] = ped

    # 3) Estados de aceptación. requires_reindex=False (campos inyectados, no indexados).
    ai = dict(meta.get("ai_prepare") or {})
    ai["accepted_draft"] = draft
    meta["ai_prepare"] = ai
    meta.update({
        "ai_prepared": True,
        "ai_prepare_status": "accepted",
        "requires_review": False,
        "requires_reindex": False,
        "teacher_reviewed_at": _now_iso(),
        "teacher_reviewed_by": user_id,
    })

    db_service.upsert_lesson(
        lesson_id=lesson_id,
        course_id=lesson.get("course_id") or course_id,
        axis_id="",
        moodle_section_id=lesson.get("moodle_section_id", "") or "",
        title=lesson.get("title", "") or lesson.get("lesson_title", ""),
        order=int(lesson.get("order", 0) or 0),
        learning_goal=new_learning_goal,
        expected_action=lesson.get("expected_action", "") or "",
        is_pilot=bool(lesson.get("is_pilot")),
        learning_goals=lesson.get("learning_goals", []) or [],
        resources=lesson.get("resources", []) or [],
        prerequisites=lesson.get("prerequisites", []) or [],
        delegated_to_tutor=new_delegated,
        attribution_constraints=new_attribution,
        notes=lesson.get("notes", "") or "",
        metadata=meta,
    )

    # 4) Momentos -> bloques existentes (preservando tiempos/orden).
    moments_applied = 0
    if apply_moments and draft.get("moments"):
        existing_blocks = db_service.list_lesson_blocks(lesson_id)
        if existing_blocks:
            merged = _apply_moments_to_blocks(existing_blocks, draft["moments"])
            db_service.replace_lesson_blocks(lesson_id, merged)
            moments_applied = sum(
                1 for m in draft["moments"]
                if str(m.get("existing_block_id") or "") in {str(b.get("block_id")) for b in existing_blocks}
            )
            if moments_applied:
                changed.append(f"moments({moments_applied})")

    return {
        "ok": True,
        "changed": changed,
        "moments_applied": moments_applied,
        "requires_reindex": False,
    }
