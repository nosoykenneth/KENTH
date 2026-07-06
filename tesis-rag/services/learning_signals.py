"""learning_signals — desempeño del estudiante en las actividades H5P (mod_hvp
InteractiveVideo) transformado en SEÑALES pedagógicas que el tutor inyecta como
contexto dinámico.

Principio (ver docs/BUENAS_PRACTICAS_RAG_EDUCATIVO):
- RAG = contenido del curso (Chroma, teacher_flow). NO cambia aquí.
- learning_signals = desempeño del alumno. Se LEEN de Moodle/H5P
  (mdl_hvp_xapi_results + gradebook, vía db_service) y se mapean a CONCEPTOS con
  el manifest `data/learning_signals/<course>_interactions.json`.
- NUNCA se indexan en Chroma ni se añaden a la query vectorial: se inyectan como
  estado runtime del alumno (Capa 3) en el bloque de contexto del tutor.

El manifest es la fuente única que también generó las interacciones H5P, así que
cada resultado por interacción se puede atribuir a un concepto y a una
remediación (timestamp + recurso real + micro-práctica).
"""
from __future__ import annotations

import json
import hashlib
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from services import db_service

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "learning_signals"

# Umbrales de nivel (porcentaje de aciertos en la actividad).
LEVEL_NEEDS = "needs_reinforcement"   # < 60
LEVEL_PARTIAL = "partial"             # 60–79
LEVEL_READY = "ready"                 # >= 80


# ------------------------------------------------------------------
# Manifest
# ------------------------------------------------------------------
@lru_cache(maxsize=8)
def _load_manifest(course_id: str) -> Optional[dict]:
    path = _DATA_DIR / f"course_{course_id}_interactions.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def lesson_plan(course_id: str, lesson_id: str) -> Optional[dict]:
    manifest = _load_manifest(str(course_id))
    if not manifest:
        return None
    for lesson in manifest.get("lessons", []):
        if lesson.get("lesson_id") == lesson_id:
            return lesson
    return None


def has_plan(course_id: str, lesson_id: str) -> bool:
    return lesson_plan(str(course_id), lesson_id) is not None


# ------------------------------------------------------------------
# Resolución del content_id de H5P
# ------------------------------------------------------------------
_LESSON_CMID_RE = re.compile(r"R(\d+)\s*$")


def _cmid_from_lesson_id(lesson_id: str) -> Optional[int]:
    """SEC{n}-R{cmid} -> cmid (identidad anclada al course_module de Moodle)."""
    if not lesson_id:
        return None
    m = _LESSON_CMID_RE.search(lesson_id)
    return int(m.group(1)) if m else None


def resolve_hvp_content_id(course_id: str, lesson_id: str) -> Optional[int]:
    """Devuelve el id de instancia de mdl_hvp (content_id de xAPI/gradebook).

    Preferimos resolver por el cmid real (course_modules) para no depender de un
    valor hardcodeado; si la BD no está (dev), usamos el del manifest.
    """
    cmid = _cmid_from_lesson_id(lesson_id)
    if cmid is not None:
        try:
            resolved = db_service.get_hvp_instance_id_by_cmid(cmid)
            if resolved:
                return int(resolved)
        except Exception:
            pass
    plan = lesson_plan(str(course_id), lesson_id)
    if plan and plan.get("hvp_content_id"):
        return int(plan["hvp_content_id"])
    return None


# ------------------------------------------------------------------
# Normalización y mapeo descripción->interacción
# ------------------------------------------------------------------
def _norm(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", str(text))          # quita HTML
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)            # quita puntuación/…/¿
    return re.sub(r"\s+", " ", text).strip()


def _match_interaction(desc_norm: str, interactions: List[dict]) -> Optional[dict]:
    """Empareja la descripción xAPI con la interacción del manifest por su enunciado."""
    if not desc_norm:
        return None
    best = None
    best_len = 0
    for it in interactions:
        q = _norm(it.get("question", ""))
        if not q:
            continue
        if desc_norm == q or desc_norm.startswith(q) or q.startswith(desc_norm) or q in desc_norm or desc_norm in q:
            # prefiere el enunciado más largo que casa (más específico)
            if len(q) > best_len:
                best, best_len = it, len(q)
    return best


def _map_children_to_interactions(children: List[dict], graded: List[dict]) -> List[Dict[str, Any]]:
    """Empareja filas hijo (xAPI) con interacciones graduadas. Primario: enunciado.
    Respaldo: orden de aparición (ambos ordenados)."""
    mapped: List[Dict[str, Any]] = []
    used_ids = set()
    ordered_graded = sorted(graded, key=lambda i: i.get("order", 0))
    order_idx = 0
    for ch in children:
        it = _match_interaction(_norm(ch.get("description", "")), graded)
        if it is None or it.get("interaction_id") in used_ids:
            # respaldo por orden
            while order_idx < len(ordered_graded) and ordered_graded[order_idx].get("interaction_id") in used_ids:
                order_idx += 1
            it = ordered_graded[order_idx] if order_idx < len(ordered_graded) else None
        if it is None:
            continue
        used_ids.add(it.get("interaction_id"))
        raw = _to_num(ch.get("raw_score"))
        mx = _to_num(ch.get("max_score")) or int(it.get("max_score", 1))
        mapped.append({
            "interaction_id": it.get("interaction_id"),
            "concept": it.get("concept"),
            "raw": raw, "max": mx,
            "correct": raw >= mx and mx > 0,
            "interaction": it,
        })
    return mapped


def _to_num(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _level(percentage: float) -> str:
    if percentage >= 80:
        return LEVEL_READY
    if percentage >= 60:
        return LEVEL_PARTIAL
    return LEVEL_NEEDS


# ------------------------------------------------------------------
# Señales del estudiante para una lección
# ------------------------------------------------------------------
def get_lesson_signals(user_id: str, lesson_id: str, course_id: str) -> Dict[str, Any]:
    plan = lesson_plan(str(course_id), lesson_id)
    base = {
        "lesson_id": lesson_id,
        "course_id": str(course_id),
        "status": "empty",
        "h5p_configured": bool(plan),
        "h5p_content_id": None,
        "score": 0, "max_score": 0, "percentage": 0,
        "completion": False, "attempts": 0,
        "attempt_id": "",
        "updated_at": None,
        "signal_hash": "",
        "level": None,
        "weak_concepts": [],
        "recommended_review": [],
    }
    if not plan:
        base["status"] = "empty"       # no hay manifest/actividad configurada
        return base

    content_id = resolve_hvp_content_id(str(course_id), lesson_id)
    base["h5p_content_id"] = content_id
    if not content_id or not db_service.using_moodle_db():
        base["status"] = "empty"
        return base

    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        base["status"] = "error"
        return base

    try:
        rows = db_service.get_hvp_xapi_results(content_id, uid)
        grade = db_service.get_hvp_grade(content_id, uid, course_id)
    except Exception:
        base["status"] = "error"
        return base

    parent = next((r for r in rows if r.get("parent_id") in (None, 0)), None)
    children = [r for r in rows if r.get("parent_id") not in (None, 0)]

    if not rows and not (grade and grade.get("finalgrade") is not None):
        base["status"] = "not_attempted"
        return base

    graded = [it for it in plan.get("interactions", []) if it.get("graded", True)]
    mapped = _map_children_to_interactions(children, graded)

    # Puntaje: preferimos la suma de interacciones mapeadas (robusto y por-concepto);
    # respaldo, el padre IV; último respaldo, la nota del gradebook escalada.
    if mapped:
        score = sum(m["raw"] for m in mapped)
        max_score = sum(m["max"] for m in mapped)
    elif parent:
        score = _to_num(parent.get("raw_score"))
        max_score = _to_num(parent.get("max_score"))
    else:
        score = _to_num((grade or {}).get("finalgrade"))
        max_score = _to_num((grade or {}).get("grademax")) or 0

    percentage = round((score / max_score) * 100) if max_score else 0
    completion = bool((grade and grade.get("finalgrade") is not None) or parent is not None)
    updated_at = (grade or {}).get("timemodified")
    max_row_id = max((_to_num(r.get("id")) for r in rows), default=0)
    attempt_basis = {
        "lesson_id": lesson_id,
        "content_id": content_id,
        "user_id": uid,
        "updated_at": updated_at,
        "max_row_id": max_row_id,
        "score": round(score, 2),
        "max_score": round(max_score, 2),
        "percentage": percentage,
        "completion": completion,
    }
    signal_hash = hashlib.sha256(
        json.dumps(attempt_basis, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]
    attempt_id = (
        f"hvp:{content_id}:u:{uid}:t:{updated_at}"
        if updated_at
        else f"hvp:{content_id}:u:{uid}:x:{int(max_row_id)}:{signal_hash}"
    )

    # Conceptos a reforzar: aquellos con alguna interacción fallada.
    labels = plan.get("concept_labels", {})
    weak_ids: List[str] = []
    for m in mapped:
        if not m["correct"] and m["concept"] not in weak_ids:
            weak_ids.append(m["concept"])

    # Remediación: primera interacción por concepto débil, en orden pedagógico, tope 3.
    review: List[Dict[str, Any]] = []
    seen = set()
    for it in sorted(graded, key=lambda i: i.get("order", 0)):
        c = it.get("concept")
        if c in weak_ids and c not in seen:
            seen.add(c)
            rr = it.get("recommended_review", {}) or {}
            review.append({
                "concept": c,
                "concept_label": labels.get(c, c),
                "timestamp": rr.get("timestamp", ""),
                "timestamp_seconds": rr.get("timestamp_seconds"),
                "resource": rr.get("resource", ""),
                "micro_practice": rr.get("micro_practice", ""),
                "message": rr.get("message", ""),
            })
        if len(review) >= 3:
            break

    base.update({
        "status": "available",
        "score": round(score, 2), "max_score": round(max_score, 2),
        "percentage": percentage,
        "completion": completion,
        "attempts": 1 if rows else (1 if completion else 0),
        "attempt_id": attempt_id,
        "updated_at": updated_at,
        "signal_hash": signal_hash,
        "level": _level(percentage),
        "weak_concepts": [{"concept": c, "label": labels.get(c, c)} for c in weak_ids],
        "recommended_review": review,
    })
    return base


def build_guidance_message(signals: Dict[str, Any]) -> str:
    """Mensaje deterministico para UI. No llama al modelo ni usa Chroma."""
    status = signals.get("status")
    if status == "not_attempted" or status != "available":
        return ""

    level = signals.get("level")
    if level == LEVEL_READY:
        return (
            "Buen avance en esta actividad. Puedes pasar a la practica o pedirme "
            "un reto aplicado para comprobarlo en una situacion real."
        )

    weak = signals.get("weak_concepts") or []
    review = signals.get("recommended_review") or []
    labels = [w.get("label") or w.get("concept") for w in weak[:2] if (w.get("label") or w.get("concept"))]
    concepts = ", ".join(labels) if labels else "los puntos donde hubo mas duda"

    first = review[0] if review else {}
    timestamp = first.get("timestamp") or "la parte relacionada del video"
    resource = first.get("resource") or "el recurso de apoyo de la leccion"
    micro = first.get("micro_practice") or "explica el concepto con tus palabras y contrasta una decision correcta con una incorrecta"

    return (
        f"Revise tus respuestas del video interactivo. Conviene reforzar {concepts}. "
        f"Te recomiendo volver al minuto {timestamp} y usar el recurso {resource}. "
        f"Luego realiza esta micro-practica: {micro}. "
        "Quieres que lo repasemos juntos?"
    )


def guidance_for(user_id: str, lesson_id: str, course_id: str) -> Dict[str, Any]:
    """Guidance listo para UI, derivado solo de learning_signals del usuario."""
    signals = get_lesson_signals(user_id, lesson_id, str(course_id))
    status = signals.get("status")
    level = signals.get("level")
    weak = signals.get("weak_concepts") or []
    should_notify = (
        status == "available"
        and level in {LEVEL_NEEDS, LEVEL_PARTIAL}
        and bool(weak)
    )
    message = build_guidance_message(signals)
    guidance_id = signals.get("attempt_id") or signals.get("signal_hash") or ""
    return {
        "lesson_id": lesson_id,
        "course_id": str(course_id),
        "attempt_id": signals.get("attempt_id") or "",
        "signal_hash": signals.get("signal_hash") or "",
        "guidance_id": guidance_id,
        "should_notify": should_notify,
        "level": level,
        "status": status,
        "message": message,
        "weak_concepts": weak,
        "recommended_review": signals.get("recommended_review") or [],
        "signals": signals,
    }


# ------------------------------------------------------------------
# Bloque de contexto para el tutor (Capa 3 — NO es evidencia RAG)
# ------------------------------------------------------------------
def render_signals_block(signals: Dict[str, Any]) -> str:
    """Texto compacto y no punitivo que se APENDA al bloque de contexto activo del
    alumno. Incluye pauta de orientación por nivel (inyección runtime, no toca los
    prompts globales del tutor)."""
    status = signals.get("status")
    if status not in {"available", "not_attempted"}:
        return ""

    lines: List[str] = ["--- SEÑALES DE APRENDIZAJE DEL ESTUDIANTE (runtime, NO ES EVIDENCIA RAG) ---"]

    if status == "not_attempted":
        lines.append("El estudiante aún NO ha realizado la actividad interactiva (video H5P) de esta lección.")
        lines.append(
            "PAUTA: invítalo con calma a hacer el video interactivo para diagnosticar su punto de partida. "
            "No inventes desempeño ni supongas fallos que no ocurrieron."
        )
        lines.append("------------------------")
        return "\n".join(lines)

    pct = signals.get("percentage", 0)
    score = signals.get("score", 0)
    mx = signals.get("max_score", 0)
    lines.append(f"Actividad interactiva de esta lección: {'completada' if signals.get('completion') else 'iniciada'}.")
    lines.append(f"Resultado interno (para tu criterio, no lo recites como cifra salvo que ayude): {pct}% ({score:g}/{mx:g}).")

    weak = signals.get("weak_concepts", [])
    if weak:
        lines.append("Conviene reforzar: " + "; ".join(w["label"] for w in weak) + ".")
    review = signals.get("recommended_review", [])
    if review:
        lines.append(
            "INSTRUCCIÓN DE RESPUESTA: orienta sobre estos conceptos y MENCIONA EXPLÍCITAMENTE, "
            "para cada uno, el minuto exacto del video al que volver Y el nombre del recurso de la "
            "lección que debe usar. Cierra con una micro-práctica concreta."
        )
        for r in review:
            ts = r.get("timestamp") or ""
            res = r.get("resource") or ""
            micro = r.get("micro_practice", "")
            # Frase lista para copiar: el modelo pequeño relaya mejor si le damos el
            # texto exacto con minuto Y nombre del recurso.
            frase = "Dile literalmente: «"
            frase += f"vuelve al minuto {ts} del video" if ts else "revisa esa parte del video"
            if res:
                frase += f" y apóyate en el recurso “{res}”"
            frase += "»."
            tail = f" Micro-práctica: {micro}" if micro else ""
            lines.append(f"  - {r['concept_label']}: {frase}{tail}")

    level = signals.get("level")
    if level == LEVEL_NEEDS:
        lines.append(
            "PAUTA DE ORIENTACIÓN (conviene reforzar): orienta con calma; prioriza 1–2 conceptos; "
            "da un timestamp y un recurso; propón una micro-práctica concreta; no avances demasiado rápido."
        )
    elif level == LEVEL_PARTIAL:
        lines.append(
            "PAUTA DE ORIENTACIÓN (refuerzo puntual): corrige la confusión principal, "
            "apóyala con un timestamp/recurso y propón una actividad breve."
        )
    else:  # ready
        lines.append(
            "PAUTA DE ORIENTACIÓN (buen avance): reconoce el progreso y propón una aplicación práctica o un reto."
        )
    lines.append(
        "TONO: nunca etiquetes de forma punitiva ('vas mal', 'nivel bajo'); usa 'conviene reforzar'. "
        "Orienta como tutor; no expongas identificadores internos ni la cifra si no aporta."
    )
    lines.append("------------------------")
    return "\n".join(lines)


def signals_block_for(user_id: str, lesson_id: str, course_id: str) -> str:
    """Atajo defensivo para el flujo de chat: nunca lanza; si algo falla, no inyecta."""
    try:
        if not lesson_id or not has_plan(str(course_id), lesson_id):
            return ""
        signals = get_lesson_signals(user_id, lesson_id, str(course_id))
        return render_signals_block(signals)
    except Exception:
        return ""


# ------------------------------------------------------------------
# Resumen para profesor/admin
# ------------------------------------------------------------------
def get_lesson_summary(course_id: str, lesson_id: str) -> Dict[str, Any]:
    plan = lesson_plan(str(course_id), lesson_id)
    out = {
        "lesson_id": lesson_id, "course_id": str(course_id),
        "status": "empty", "h5p_configured": bool(plan),
        "interactions_count": len(plan.get("interactions", [])) if plan else 0,
        "concepts": sorted({it.get("concept") for it in plan.get("interactions", [])}) if plan else [],
        "students_with_results": 0, "completion_count": 0,
        "average_percentage": 0,
        "level_distribution": {LEVEL_NEEDS: 0, LEVEL_PARTIAL: 0, LEVEL_READY: 0},
        "most_failed_concepts": [],
    }
    if not plan:
        return out
    content_id = resolve_hvp_content_id(str(course_id), lesson_id)
    out["h5p_content_id"] = content_id
    if not content_id or not db_service.using_moodle_db():
        return out
    try:
        parents = db_service.get_hvp_xapi_parents_all(content_id)
        children = db_service.get_hvp_xapi_children_all(content_id)
    except Exception:
        out["status"] = "error"
        return out

    if not parents:
        out["status"] = "no_results"
        return out

    graded = [it for it in plan.get("interactions", []) if it.get("graded", True)]
    labels = plan.get("concept_labels", {})
    pcts = []
    for p in parents:
        mx = _to_num(p.get("max_score"))
        pct = round((_to_num(p.get("raw_score")) / mx) * 100) if mx else 0
        pcts.append(pct)
        out["level_distribution"][_level(pct)] += 1
    out["students_with_results"] = len(parents)
    out["completion_count"] = len(parents)
    out["average_percentage"] = round(sum(pcts) / len(pcts)) if pcts else 0

    # Conceptos más fallados (agregado por interacción -> concepto).
    fail_by_concept: Dict[str, int] = {}
    total_by_concept: Dict[str, int] = {}
    for ch in children:
        it = _match_interaction(_norm(ch.get("description", "")), graded)
        if not it:
            continue
        c = it.get("concept")
        total_by_concept[c] = total_by_concept.get(c, 0) + 1
        if _to_num(ch.get("raw_score")) < (_to_num(ch.get("max_score")) or 1):
            fail_by_concept[c] = fail_by_concept.get(c, 0) + 1
    ranked = sorted(fail_by_concept.items(), key=lambda kv: kv[1], reverse=True)
    out["most_failed_concepts"] = [
        {"concept": c, "label": labels.get(c, c), "failures": n, "answered": total_by_concept.get(c, 0)}
        for c, n in ranked
    ]
    out["status"] = "available"
    return out


def sync_lesson(course_id: str, lesson_id: str) -> Dict[str, Any]:
    """Sincroniza/recalcula señales desde Moodle/H5P. Los resultados YA viven en
    Moodle (mdl_hvp_xapi_results + gradebook); esta operación es idempotente:
    recomputa el resumen actual y lo devuelve. No escribe datos sensibles."""
    summary = get_lesson_summary(str(course_id), lesson_id)
    return {
        "lesson_id": lesson_id,
        "synced": summary.get("status") in {"available", "no_results"},
        "students_with_results": summary.get("students_with_results", 0),
        "status": summary.get("status"),
        "summary": summary,
    }

def sync_lesson_for_user(user_id: str, course_id: str, lesson_id: str) -> Dict[str, Any]:
    """Recalculo idempotente para el estudiante autenticado."""
    signals = get_lesson_signals(user_id, lesson_id, str(course_id))
    return {
        "lesson_id": lesson_id,
        "course_id": str(course_id),
        "synced": signals.get("status") in {"available", "not_attempted", "empty"},
        "status": signals.get("status"),
        "attempt_id": signals.get("attempt_id") or "",
        "signal_hash": signals.get("signal_hash") or "",
        "signals": signals,
    }
