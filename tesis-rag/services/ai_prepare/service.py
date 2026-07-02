"""Orquestación del asistente "Preparar tutor con IA" (Fases 4 y 7).

Pipeline puro (sin DB, testeable monkeypatcheando `models`):
  transcripción -> [resumen jerárquico si es larga] -> generación JSON
  -> validación (+reparación 1 vez) -> reconciliación de block_id -> [revisión max].

No toca Chroma, ni timestamps, ni el conjunto de bloques. El resultado es un
BORRADOR que el endpoint persiste en metadata.ai_prepare (aislado).
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

import config
from services.ai_prepare import models, prompts, schema


def transcript_to_text(segments: List[Dict[str, Any]]) -> str:
    """Une los segmentos de transcripción en un texto plano."""
    parts: List[str] = []
    for seg in segments or []:
        txt = (seg.get("text") or "").strip()
        if txt:
            parts.append(txt)
    return " ".join(parts).strip()


def _mmss(seconds: float) -> str:
    s = int(max(0, seconds))
    return f"{s // 60}:{s % 60:02d}"


def transcript_to_timestamped_text(segments: List[Dict[str, Any]]) -> str:
    """Texto de la transcripción con marca [m:ss] por segmento, para que la IA
    pueda situar los momentos en la línea de tiempo real del video."""
    lines: List[str] = []
    for seg in segments or []:
        txt = (seg.get("text") or "").strip()
        if not txt:
            continue
        lines.append(f"[{_mmss(float(seg.get('start_time') or 0))}] {txt}")
    return "\n".join(lines).strip()


def transcript_duration(segments: List[Dict[str, Any]]) -> float:
    """Duración aproximada del video = mayor end_time de la transcripción (segundos)."""
    end = 0.0
    for seg in segments or []:
        try:
            end = max(end, float(seg.get("end_time") or 0))
        except (TypeError, ValueError):
            continue
    return round(end, 3)


def _chunk(text: str, size: int) -> List[str]:
    return [text[i:i + size] for i in range(0, len(text), size)] or [""]


def _summarize_long(text: str, domain_label: str) -> str:
    """Resumen jerárquico con el modelo de contexto largo (Fase 2).

    Divide la transcripción en trozos, resume cada uno preservando conceptos,
    términos técnicos y estructura, y concatena. No inventa: solo condensa.
    """
    dom = (domain_label or "").strip() or "el curso"
    sys = (
        f"Eres un asistente que condensa la transcripción de una clase de {dom} sin "
        "perder conceptos, términos técnicos ni la secuencia de temas. No inventes; "
        "solo resume fielmente. Responde en texto plano, en español."
    )
    chunks = _chunk(text, 8000)
    resumenes: List[str] = []
    for idx, ch in enumerate(chunks):
        usr = (
            f"Resume fielmente este fragmento {idx + 1}/{len(chunks)} de la clase, "
            "conservando conceptos y términos técnicos tal como aparecen:\n\n" + ch
        )
        try:
            out = models.invoke_text(
                models.TASK_LONG_CONTEXT, sys, usr, temperature=0.1
            )
        except Exception:
            out = ch[:2000]  # si el modelo largo falla, degradamos al recorte
        resumenes.append(out.strip())
    return "\n\n".join(resumenes).strip()


def prepare_transcript_text(segments: List[Dict[str, Any]], domain_label: str) -> Dict[str, Any]:
    """Devuelve el texto (con marcas [m:ss]) que se enviará al modelo + metadatos.

    Preferimos el texto CON marcas de tiempo (para situar los momentos). Solo si es
    muy largo caemos al resumen jerárquico (que pierde las marcas): en el piloto los
    videos son cortos y este camino rara vez se usa.
    """
    stamped = transcript_to_timestamped_text(segments)
    plain = transcript_to_text(segments)
    original_chars = len(stamped)
    summarized = False
    if len(plain) > config.AI_PREP_LONG_CONTEXT_THRESHOLD:
        text = _summarize_long(plain[: config.AI_PREP_TRANSCRIPT_CHAR_LIMIT], domain_label)
        summarized = True
    elif len(stamped) > config.AI_PREP_TRANSCRIPT_CHAR_LIMIT:
        text = stamped[: config.AI_PREP_TRANSCRIPT_CHAR_LIMIT]
    else:
        text = stamped
    return {
        "text": text,
        "original_chars": original_chars,
        "processed_chars": len(text),
        "summarized": summarized,
        "duration_seconds": transcript_duration(segments),
    }


def _reconcile_block_ids(draft: Dict[str, Any], blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Anula existing_block_id que no correspondan a un bloque real (anti-invención)."""
    valid = {str(b.get("block_id")) for b in (blocks or []) if b.get("block_id")}
    for m in draft.get("moments", []) or []:
        bid = m.get("existing_block_id")
        if bid and str(bid) not in valid:
            m["existing_block_id"] = None
    return draft


def generate_draft(
    *,
    lesson_title: str,
    section_name: str,
    blocks: List[Dict[str, Any]],
    transcript_text: str,
    domain_label: str,
    extra_context: str = "",
    duration_seconds: float = 0,
) -> Dict[str, Any]:
    """Genera y valida el JSON pedagógico. Repara una vez si es inválido.

    Devuelve {"ok": bool, "draft": dict|None, "errors": [...], "repaired": bool}.
    """
    sys = prompts.system_prompt(domain_label)
    usr = prompts.user_prompt(
        lesson_title=lesson_title,
        section_name=section_name,
        existing_blocks=blocks,
        transcript_text=transcript_text,
        extra_context=extra_context,
        duration_seconds=duration_seconds,
    )
    raw = models.invoke_text(models.TASK_DRAFT, sys, usr, force_json=True, temperature=0.2)
    draft, errors = schema.parse_and_validate(raw)
    repaired = False
    if draft is None:
        # Reparación única (Fase 5): re-pedir SOLO el JSON válido.
        repaired = True
        rep = prompts.repair_prompt(raw, errors)
        raw2 = models.invoke_text(
            models.TASK_DRAFT, sys, rep, force_json=True, temperature=0.1
        )
        draft, errors = schema.parse_and_validate(raw2)
    if draft is None:
        return {"ok": False, "draft": None, "errors": errors, "repaired": repaired}

    draft_dict = schema.draft_to_public(draft)
    draft_dict = _reconcile_block_ids(draft_dict, blocks)
    return {"ok": True, "draft": draft_dict, "errors": [], "repaired": repaired}


def review_draft(
    draft_dict: Dict[str, Any], domain_label: str, *, model: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Revisión de calidad (quality=max). No reescribe: audita y recomienda.

    Devuelve un dict con problemas/recomendaciones/veredicto, o None si falla.
    """
    sys = prompts.review_system_prompt(domain_label)
    usr = prompts.review_user_prompt(json.dumps(draft_dict, ensure_ascii=False))
    try:
        raw = models.invoke_text(
            models.TASK_REVIEW, sys, usr, force_json=True, temperature=0.1, model=model
        )
    except Exception as exc:  # pragma: no cover - depende del entorno
        return {"error": f"revisión no disponible: {exc}", "veredicto": "revisar"}
    block = schema.extract_json_block(raw)
    if not block:
        return {"error": "revisión sin JSON parseable", "veredicto": "revisar"}
    try:
        data = json.loads(block)
    except Exception:
        return {"error": "revisión con JSON inválido", "veredicto": "revisar"}
    # Limpieza defensiva de las listas de la revisión.
    out: Dict[str, Any] = {}
    for k in ("problemas_detectados", "campos_inconsistentes", "terminos_dudosos", "recomendaciones"):
        out[k] = schema._clean_list(data.get(k))
    ver = str(data.get("veredicto", "") or "").strip().lower()
    out["veredicto"] = ver if ver in {"aprobado", "revisar", "rechazar"} else "revisar"
    out["review_model"] = model or models.get_model_name(models.TASK_REVIEW)
    return out


def run(
    *,
    lesson_title: str,
    section_name: str,
    transcript_segments: List[Dict[str, Any]],
    blocks: List[Dict[str, Any]],
    quality: str = "balanced",
    domain_label: str = "",
    extra_context: str = "",
    review_model: Optional[str] = None,
) -> Dict[str, Any]:
    """Orquesta todo el pipeline. Devuelve el resultado listo para persistir."""
    started = time.time()
    prep = prepare_transcript_text(transcript_segments, domain_label)
    if not prep["text"].strip():
        return {
            "ok": False,
            "error": "La lección no tiene transcripción utilizable. Transcribe o edita la transcripción antes de preparar el tutor.",
            "elapsed_seconds": round(time.time() - started, 2),
        }

    gen = generate_draft(
        lesson_title=lesson_title,
        section_name=section_name,
        blocks=blocks,
        transcript_text=prep["text"],
        domain_label=domain_label,
        extra_context=extra_context,
        duration_seconds=prep.get("duration_seconds", 0),
    )
    if not gen["ok"]:
        return {
            "ok": False,
            "error": "El modelo no devolvió un JSON válido tras la reparación.",
            "errors": gen["errors"],
            "elapsed_seconds": round(time.time() - started, 2),
        }

    draft = gen["draft"]
    review = None
    if quality == "max":
        review = review_draft(draft, domain_label, model=review_model)

    return {
        "ok": True,
        "draft": draft,
        "review": review,
        "repaired": gen["repaired"],
        "transcript_info": prep,
        "models": models.describe_selection(quality),
        "elapsed_seconds": round(time.time() - started, 2),
    }
