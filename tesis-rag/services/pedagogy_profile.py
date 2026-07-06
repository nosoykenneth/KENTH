"""Modelo pedagógico CANÓNICO de la lección (perfil único del tutor).

Un solo objeto lógico que usan por igual la Vista Profesor, el Editor Avanzado
(admin), el endpoint de IA (`ai-prepare`) y el tutor (`context_service`). No hay
campos paralelos con nombres distintos: la diferencia entre vistas es solo de
presentación.

El perfil NO es una tabla nueva: es una NORMALIZACIÓN sobre el almacenamiento
existente (sin migración de esquema, sin perder datos):

    learning_goal        <-> lessons.learning_goal
    lesson_summary       <-> metadata.pedagogy.lesson_summary
    tutor_tone           <-> metadata.pedagogy.tutor_tone
    help_level           <-> metadata.pedagogy.help_level
    lesson_rules[]       <-> metadata.pedagogy.lesson_rules
    key_concepts[]       <-> metadata.pedagogy.key_concepts        (inyectado)
    common_mistakes[]    <-> metadata.pedagogy.common_mistakes
    probable_questions[] <-> metadata.pedagogy.probable_questions  (inyectado)
    tutor_focus[]        <-> lessons.delegated_to_tutor
    tutor_must_not_do[]  <-> lessons.attribution_constraints
    proactive_message    <-> lesson_prompts (proactive)   [student-facing]
    suggested_prompts[]  <-> lesson_prompts (suggested)    [student-facing]
    moments[]            <-> lesson_blocks (+ block.metadata.common_mistakes)

`requires_reindex` es SIEMPRE False para el perfil: estos campos se INYECTAN en
el prompt, no se INDEXAN en Chroma (arquitectura inject-vs-index). Solo la
transcripción y los recursos reindexan, por su propio flujo.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from services import db_service


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_list(value: Any) -> List[str]:
    """Normaliza a lista de strings, tolerando string con saltos de línea."""
    if value is None:
        return []
    if isinstance(value, str):
        return [ln.strip() for ln in value.split("\n") if ln.strip()]
    if isinstance(value, (list, tuple)):
        return [str(x).strip() for x in value if str(x).strip()]
    return []


def _block_to_moment(b: Dict[str, Any]) -> Dict[str, Any]:
    meta = b.get("metadata") or {}
    return {
        "block_id": b.get("block_id", ""),
        "title": b.get("block_title", "") or "",
        "summary": b.get("summary", "") or "",
        "pedagogical_intent": b.get("tutor_focus", "") or "",
        "key_concepts": list(b.get("concepts") or []),
        "common_mistakes": list(meta.get("common_mistakes") or []),
        "probable_questions": list(b.get("preguntas_probables") or []),
        # Tiempos SOLO para mostrar el rango humano; el profesor no los edita.
        "start_time": b.get("start_time"),
        "end_time": b.get("end_time"),
    }


def build_profile(lesson: Dict[str, Any]) -> Dict[str, Any]:
    """Construye el perfil canónico desde una lección (shape de load_lesson)."""
    lesson = lesson or {}
    meta = lesson.get("metadata") or {}
    ped = meta.get("pedagogy") or {}
    return {
        "learning_goal": lesson.get("learning_goal", "") or "",
        "lesson_summary": ped.get("lesson_summary", "") or "",
        "tutor_tone": ped.get("tutor_tone", "") or "",
        "help_level": ped.get("help_level", "") or "",
        "lesson_rules": _as_list(ped.get("lesson_rules")),
        "key_concepts": _as_list(ped.get("key_concepts")),
        "common_mistakes": _as_list(ped.get("common_mistakes")),
        "probable_questions": _as_list(ped.get("probable_questions")),
        "tutor_focus": list(lesson.get("delegated_to_tutor") or []),
        "tutor_must_not_do": list(lesson.get("attribution_constraints") or []),
        "proactive_message": lesson.get("proactive_message", "") or "",
        "suggested_prompts": list(lesson.get("suggested_prompts") or []),
        "moments": [_block_to_moment(b) for b in (lesson.get("blocks") or [])],
        "ai_prepared": bool(meta.get("ai_prepared")),
        "requires_review": bool(meta.get("requires_review")),
        "requires_reindex": False,
    }


def _moment_field(m: Dict[str, Any], *keys):
    """Primer valor no vacío entre varias claves alias (block_id/existing_block_id…)."""
    for k in keys:
        v = m.get(k)
        if v:
            return v
    return None


def _moment_time(m: Dict[str, Any], key: str):
    """Tiempo del momento en segundos (float) o None si no es numérico."""
    v = m.get(key)
    if v is None or v == "":
        return None
    try:
        t = float(v)
    except (TypeError, ValueError):
        return None
    return max(0.0, round(t, 3))


def fuse_moments(
    existing_blocks: List[Dict[str, Any]],
    moments: List[Dict[str, Any]],
    lesson_id: str = "",
    replace_blocks: bool = False,
) -> List[Dict[str, Any]]:
    """Funde los campos pedagógicos de los momentos en los bloques EXISTENTES y, si
    algún momento trae TIEMPOS válidos y no mapea a un bloque, CREA ese bloque.

    - Fusión por block_id existente (PRESERVA start/end salvo que el momento traiga
      tiempos): así la IA puede actualizar título/resumen/intención/concepts + el modo.
    - Momentos con tiempos válidos sin id existente -> bloque NUEVO (la IA distribuye
      los momentos por la línea de tiempo en vez de apilarlos). Sin tiempos válidos se
      IGNORAN (compat: no se inventan bloques sin tiempo).
    - `common_mistakes` por momento va a `block.metadata.common_mistakes`.
    Acepta el shape del borrador IA (`existing_block_id`, `pedagogical_intent`,
    `key_concepts`, `probable_questions`, `start_time`, `end_time`, `interaction_mode`)
    y el canónico (`block_id`, …).

    replace_blocks=True: REGENERACIÓN LIMPIA. Ignora los bloques previos (útil cuando
    la grabación/transcripción cambió y los bloques viejos son de otro tema) y arma la
    línea de tiempo SOLO desde los momentos entrantes con tiempos válidos. Evita que
    momentos de una grabación anterior sobrevivan a un re-`ai_prepare`.
    """
    if replace_blocks:
        existing_blocks = []
        moments = [
            {k: v for k, v in (m or {}).items() if k not in ("block_id", "existing_block_id")}
            for m in (moments or [])
        ]

    by_id: Dict[str, Dict[str, Any]] = {}
    for m in moments or []:
        bid = str(_moment_field(m, "block_id", "existing_block_id") or "").strip()
        if bid:
            by_id[bid] = m
    existing_ids = {str(b.get("block_id")) for b in existing_blocks}

    merged: List[Dict[str, Any]] = []
    for b in existing_blocks:
        bid = str(b.get("block_id"))
        m = by_id.get(bid)
        bmeta = dict(b.get("metadata") or {})
        if m is not None and m.get("common_mistakes") is not None:
            bmeta["common_mistakes"] = list(m.get("common_mistakes") or [])
        m_start = _moment_time(m or {}, "start_time")
        m_end = _moment_time(m or {}, "end_time")
        m_mode = str((m or {}).get("interaction_mode") or "").strip()
        merged.append({
            "block_id": bid,
            "block_order": b.get("block_order"),
            # El momento puede reajustar tiempos (solo si trae ambos y son coherentes).
            "start_time": (m_start if (m_start is not None and m_end is not None and m_end > m_start) else b.get("start_time")),
            "end_time": (m_end if (m_start is not None and m_end is not None and m_end > m_start) else b.get("end_time")),
            "block_title": (m.get("title") if m and m.get("title") else b.get("block_title", "")),
            "summary": (m.get("summary") if m and m.get("summary") else b.get("summary", "")),
            "interaction_mode": (m_mode or b.get("interaction_mode", "")),
            "tutor_focus": (_moment_field(m or {}, "pedagogical_intent", "tutor_focus") or b.get("tutor_focus", "")),
            "concepts": (m.get("key_concepts") if m and m.get("key_concepts") else b.get("concepts", [])),
            "preguntas_probables": (m.get("probable_questions") if m and m.get("probable_questions") else b.get("preguntas_probables", [])),
            "metadata": bmeta,
        })

    # Bloques NUEVOS: momentos con tiempos válidos que no mapean a un bloque existente.
    new_blocks: List[Dict[str, Any]] = []
    for m in moments or []:
        mid = str(_moment_field(m, "block_id", "existing_block_id") or "").strip()
        if mid and mid in existing_ids:
            continue
        st = _moment_time(m, "start_time")
        et = _moment_time(m, "end_time")
        if st is None or et is None or et <= st:
            continue  # sin tiempos válidos -> no se crea (compat)
        new_blocks.append({
            "block_id": None,
            "start_time": st,
            "end_time": et,
            "block_title": m.get("title", "") or "",
            "summary": m.get("summary", "") or "",
            "interaction_mode": str(m.get("interaction_mode") or "").strip(),
            "tutor_focus": _moment_field(m, "pedagogical_intent", "tutor_focus") or "",
            "concepts": list(m.get("key_concepts") or []),
            "preguntas_probables": list(m.get("probable_questions") or []),
            "metadata": {"common_mistakes": list(m.get("common_mistakes") or [])},
        })

    if not new_blocks:
        return merged

    # Con bloques nuevos: ordena por tiempo y renumera block_order; conserva ids
    # existentes y asigna ids frescos (sin colisión) a los nuevos.
    allb = merged + new_blocks
    allb.sort(key=lambda x: float(x.get("start_time") or 0))
    prefix = (lesson_id or (str(existing_blocks[0].get("block_id")).rsplit("-B", 1)[0]
                            if existing_blocks else "L")).strip() or "L"
    used = {str(b.get("block_id")) for b in merged}
    counter = len(allb)
    for i, b in enumerate(allb):
        b["block_order"] = i
        if not b.get("block_id"):
            counter += 1
            nid = f"{prefix}-B{counter}"
            while nid in used:
                counter += 1
                nid = f"{prefix}-B{counter}"
            b["block_id"] = nid
            used.add(nid)
    return allb


def apply_profile(
    lesson_id: str,
    course_id: str,
    user_id: str,
    profile: Dict[str, Any],
    *,
    mode: str = "replace",
    apply_moments: bool = False,
    replace_blocks: bool = False,
) -> Dict[str, Any]:
    """Escribe el perfil canónico al almacenamiento (lección + pedagogy + prompts).

    mode="replace": escribe EXACTAMENTE lo del perfil (permite limpiar campos) —
      lo usan los editores (Profesor/Admin) al Guardar.
    mode="merge": solo los campos NO vacíos del perfil pisan lo existente —
      lo usa la promoción del borrador IA (no borra lo que el modelo dejó vacío).

    NUNCA toca estructura técnica: title/order/section/notes/legacy se preservan.
    Los momentos solo se tocan si apply_moments=True (IA); los editores usan
    /moments (profesor) o /blocks (admin) para los momentos.
    """
    lesson = db_service.get_lesson(lesson_id, course_id)
    if not lesson:
        return {"ok": False, "error": "Lección no encontrada."}

    replace = (mode != "merge")
    changed: List[str] = []

    def _str(field: str, current: str) -> str:
        v = (profile.get(field) or "").strip() if isinstance(profile.get(field), str) else profile.get(field)
        if replace:
            if v != current:
                changed.append(field)
            return v or ""
        if v:
            changed.append(field)
            return v
        return current or ""

    def _list(field: str, current: List[str]) -> List[str]:
        v = profile.get(field)
        if replace:
            new = _as_list(v)
            if new != (current or []):
                changed.append(field)
            return new
        if v:
            changed.append(field)
            return _as_list(v)
        return current or []

    # Campos vivos de la lección (inyectados por el tutor).
    new_learning_goal = _str("learning_goal", lesson.get("learning_goal", "") or "")
    new_delegated = _list("tutor_focus", lesson.get("delegated_to_tutor", []) or [])
    new_attribution = _list("tutor_must_not_do", lesson.get("attribution_constraints", []) or [])

    # metadata.pedagogy (consumida por render_context_block).
    meta = dict(lesson.get("metadata") or {})
    ped = dict(meta.get("pedagogy") or {})
    ped["lesson_summary"] = _str("lesson_summary", ped.get("lesson_summary", "") or "")
    ped["tutor_tone"] = _str("tutor_tone", ped.get("tutor_tone", "") or "")
    ped["help_level"] = _str("help_level", ped.get("help_level", "") or "")
    ped["lesson_rules"] = _list("lesson_rules", _as_list(ped.get("lesson_rules")))
    ped["key_concepts"] = _list("key_concepts", _as_list(ped.get("key_concepts")))
    ped["common_mistakes"] = _list("common_mistakes", _as_list(ped.get("common_mistakes")))
    ped["probable_questions"] = _list("probable_questions", _as_list(ped.get("probable_questions")))
    meta["pedagogy"] = ped
    meta["requires_reindex"] = False
    meta["edited_by"] = user_id

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

    # Prompts al alumno (proactive/suggested). student-facing: se conservan como campos propios.
    if replace:
        db_service.set_lesson_prompts(
            lesson_id,
            proactive_message=(profile.get("proactive_message") or "") if isinstance(profile.get("proactive_message"), str) else "",
            suggested_prompts=_as_list(profile.get("suggested_prompts")),
        )
        changed.append("prompts")
    else:
        pm = profile.get("proactive_message")
        sp = profile.get("suggested_prompts")
        if pm or sp:
            db_service.set_lesson_prompts(
                lesson_id,
                proactive_message=(pm or lesson.get("proactive_message", "") or ""),
                suggested_prompts=(_as_list(sp) if sp else (lesson.get("suggested_prompts", []) or [])),
            )
            changed.append("prompts")

    # Momentos -> bloques (solo IA). Funde en los existentes y CREA bloques nuevos
    # para momentos con tiempos válidos (aunque la lección aún no tenga bloques).
    moments_applied = 0
    if apply_moments and profile.get("moments"):
        existing_blocks = db_service.list_lesson_blocks(lesson_id)
        existing_ids = {str(b.get("block_id")) for b in existing_blocks}
        merged = fuse_moments(existing_blocks, profile["moments"], lesson_id=lesson_id,
                              replace_blocks=replace_blocks)
        # En regeneración limpia solo pisamos si hay bloques nuevos (no borra a ciegas).
        # Normal: escribimos si hay algo (evita crear bloques de la nada sin tiempos).
        write = bool(merged) if replace_blocks else bool(merged or existing_blocks)
        if write:
            db_service.replace_lesson_blocks(lesson_id, merged)
            for m in profile["moments"]:
                mid = str(_moment_field(m, "block_id", "existing_block_id") or "")
                if mid and mid in existing_ids:
                    moments_applied += 1
                elif _moment_time(m, "start_time") is not None and _moment_time(m, "end_time") is not None:
                    moments_applied += 1  # bloque nuevo creado desde el momento
            if moments_applied:
                changed.append(f"moments({moments_applied})")

    return {"ok": True, "changed": changed, "moments_applied": moments_applied, "requires_reindex": False}
