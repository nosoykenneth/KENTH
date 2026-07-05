"""Contexto aprobado de la lección (flujo docente). Fases 4, 5 y 6.

Materializa una FUENTE TEXTUAL INDEXABLE a partir del perfil pedagógico CANÓNICO
que el profesor aceptó en el editor "Preparar tutor con IA". Es la pieza que hace
defendible el flujo: el profesor no escribe Markdown/YAML; alimenta al tutor desde
la interfaz y el sistema genera la evidencia.

Separación inject-vs-index (Fase 4). El perfil canónico tiene dos naturalezas:

  COMPORTAMIENTO (se INYECTA en el prompt, NUNCA se indexa como evidencia):
    - tutor_tone, help_level
    - lesson_rules            (directrices internas de la lección)
    - tutor_must_not_do       (restricciones privadas / attribution_constraints)
    - proactive_message, suggested_prompts (mensajes al alumno, no evidencia)

  CONOCIMIENTO (se MATERIALIZA como texto indexable = teacher_approved_context):
    - learning_goal, lesson_summary
    - key_concepts, common_mistakes, probable_questions
    - moments.title / summary / pedagogical_intent
    - recursos textuales aprobados / descripciones de recursos aprobados

La transcripción aprobada es su PROPIA fuente (source="transcript"); aquí NO se
duplica. Los recursos binarios se referencian por su descripción aprobada, nunca su
binario.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services import db_service, pedagogy_profile
from services.lesson_service import load_lesson


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _bullets(items: List[str]) -> List[str]:
    out: List[str] = []
    for it in items or []:
        s = _clean(it)
        if s:
            out.append(f"- {s}")
    return out


def _approved_text_resources(course_id: str, lesson_id: str) -> List[Dict[str, str]]:
    """Recursos APROBADOS relacionados con la lección, como {title, description}.

    Respeta el contrato inject-vs-index: solo entran recursos con
    allowed_for_indexing=true; para binarios (audio/plantilla/imagen) se usa su
    DESCRIPCIÓN aprobada, nunca el archivo. No inventa recursos: si no hay, [].
    """
    try:
        docs = db_service.list_documents(course_id=course_id, lesson_id=lesson_id)
    except Exception:
        return []
    out: List[Dict[str, str]] = []
    for d in docs or []:
        if not d.get("allowed_for_indexing"):
            continue
        meta = d.get("metadata") or {}
        title = _clean(d.get("title"))
        desc = _clean(meta.get("description") or d.get("notes"))
        if not (title or desc):
            continue
        out.append({"title": title, "description": desc,
                    "media_type": _clean(d.get("media_type") or meta.get("media_type"))})
    return out


def _section_meta(course_id: str, moodle_section_id: str) -> Dict[str, Any]:
    sid = _clean(moodle_section_id)
    if not sid:
        return {}
    try:
        from services import section_service
        for sec in section_service._list_sections_from_db(str(course_id or "")):
            if str(sec.get("moodle_section_id") or "") == sid:
                return {
                    "section_number": sec.get("section_number"),
                    "section_title": sec.get("section_name") or sec.get("current_section_name") or "",
                }
    except Exception:
        pass
    return {}


def build_teacher_approved_context_document(
    lesson_id: str,
    course_id: Optional[str] = None,
    *,
    lesson_title_override: str = "",
) -> Optional[Dict[str, Any]]:
    """Construye el documento 'Contexto aprobado de la lección' desde el perfil canónico.

    Devuelve {text, chunks, metadata, has_content} o None si la lección no existe.
    `has_content` es False cuando no hay nada pedagógico aprobado que materializar
    (solo entonces el caller decide no indexar / limpiar).

    NO incluye tono, nivel de ayuda, reglas internas, tutor_must_not_do, prompts
    internos, QA, evaluación, manifests, reportes, ni IDs técnicos (block_id).
    """
    lesson = load_lesson(lesson_id, course_id)
    if not lesson:
        return None

    profile = pedagogy_profile.build_profile(lesson)
    human_title = _clean(lesson_title_override) or _clean(lesson.get("lesson_title")) or _clean(lesson_id)
    sec_id = _clean(lesson.get("moodle_section_id"))
    sec_meta = _section_meta(course_id or lesson.get("course_id") or "", sec_id)
    resources = _approved_text_resources(course_id or lesson.get("course_id") or "", lesson_id)

    # --- Secciones del documento (cada una será un chunk autocontenido) ---
    # Cada chunk arranca con el título humano para que el retrieval lo ancle a la
    # lección correcta y las fuentes muestren una etiqueta humana (nunca el id).
    header = f"Lección: {human_title}"
    sections: List[Dict[str, str]] = []

    def add(title: str, body_lines: List[str]) -> None:
        body = [ln for ln in body_lines if _clean(ln)]
        if body:
            sections.append({"heading": title, "body": "\n".join(body)})

    if _clean(profile.get("learning_goal")):
        add("Objetivo de aprendizaje", [_clean(profile["learning_goal"])])
    if _clean(profile.get("lesson_summary")):
        add("Resumen de la clase", [_clean(profile["lesson_summary"])])
    add("Conceptos clave", _bullets(profile.get("key_concepts")))
    add("Errores comunes", _bullets(profile.get("common_mistakes")))
    add("Preguntas probables", _bullets(profile.get("probable_questions")))

    momentos: List[str] = []
    for m in profile.get("moments") or []:
        titulo = _clean(m.get("title"))
        resumen = _clean(m.get("summary"))
        intent = _clean(m.get("pedagogical_intent"))
        if not (titulo or resumen or intent):
            continue
        linea = f"- {titulo}" if titulo else "-"
        detalles = " ".join(p for p in (resumen, intent) if p)
        if detalles:
            linea = f"{linea}: {detalles}" if titulo else f"- {detalles}"
        momentos.append(linea)
    add("Momentos de la clase", momentos)

    recursos_lineas: List[str] = []
    for r in resources:
        t = _clean(r.get("title"))
        desc = _clean(r.get("description"))
        if t and desc:
            recursos_lineas.append(f"- {t}: {desc}")
        elif t:
            recursos_lineas.append(f"- {t}")
        elif desc:
            recursos_lineas.append(f"- {desc}")
    add("Recursos aprobados relacionados", recursos_lineas)

    has_content = bool(sections)

    # Texto completo (para diagnóstico/preview) + chunks (para indexar).
    doc_lines = ["# Contexto aprobado de la lección", "", header, ""]
    chunks: List[str] = []
    for sec in sections:
        doc_lines.append(f"## {sec['heading']}")
        doc_lines.append(sec["body"])
        doc_lines.append("")
        chunks.append(f"{header}\n\n{sec['heading']}\n{sec['body']}")
    text = "\n".join(doc_lines).strip()
    source_hash = hashlib.md5(text.encode("utf-8")).hexdigest()

    metadata = {
        "course_id": str(course_id or lesson.get("course_id") or ""),
        "moodle_section_id": sec_id,
        "section_number": str(sec_meta.get("section_number") or ""),
        "section_title": _clean(sec_meta.get("section_title")),
        "lesson_id": _clean(lesson_id),
        "lesson_title": human_title,
        "source_type": "teacher_approved_context",
        "source": "authoring_profile",
        "visible_to_student": True,
        "allowed_for_indexing": True,
        "internal_context": False,
        "generated_from": "ai_prepare_acceptance",
        "status": "teacher_approved",
        "updated_at": _now_iso(),
        "source_hash": source_hash,
        "corpus_version": "teacher_flow_v1",
    }
    return {"text": text, "chunks": chunks, "metadata": metadata, "has_content": has_content}


def publish_lesson_teacher_context(
    lesson_id: str,
    course_id: Optional[str] = None,
    user_id: str = "",
    *,
    lesson_title_override: str = "",
) -> Dict[str, Any]:
    """Publica ("Publicar cambios del tutor"): construye el contexto aprobado y lo
    INDEXA de forma incremental (delete-then-add por lección), sin rebuild global.

    Devuelve el contrato de estado que consume el frontend:
      { ok, tutor_updated, transcript_status, index_status, indexed_at,
        chunks, requires_reindex, source_type, message }
    """
    doc = build_teacher_approved_context_document(
        lesson_id, course_id, lesson_title_override=lesson_title_override
    )
    if doc is None:
        return {"ok": False, "error": "Lección no encontrada.", "index_status": "error"}

    lesson = load_lesson(lesson_id, course_id) or {}
    meta = lesson.get("metadata") or {}
    transcript_status = _clean(meta.get("transcript_status"))
    md = doc["metadata"]

    result = {"success": False, "chunks": 0}
    index_status = "pending"
    try:
        import ingest
        if doc["has_content"]:
            result = ingest.index_teacher_approved_context(
                md["course_id"], lesson_id, doc["chunks"],
                lesson_title=md["lesson_title"],
                moodle_section_id=md["moodle_section_id"],
                updated_at=md["updated_at"],
                source_hash=md["source_hash"],
            )
        else:
            # Sin contenido pedagógico aprobado: se limpia cualquier chunk previo.
            ingest.delete_teacher_approved_context(lesson_id)
            result = {"success": True, "chunks": 0, "message": "sin contenido aprobado"}
        index_status = "indexed" if result.get("success") else "error"
    except Exception as exc:  # pragma: no cover - depende del entorno (embeddings)
        print(f"[teacher-context] fallo indexando {lesson_id}: {exc}")
        index_status = "error"

    indexed_at = _now_iso() if index_status == "indexed" else ""
    requires_reindex = index_status != "indexed"

    # Persistir estado en la lección (best-effort).
    try:
        db_service.merge_lesson_metadata(lesson_id, course_id, {
            "teacher_context_index_status": index_status,
            "teacher_context_indexed_at": indexed_at,
            "teacher_context_chunks": int(result.get("chunks") or 0),
            "teacher_context_hash": md["source_hash"],
            "teacher_context_published_by": user_id,
        })
    except Exception as exc:  # pragma: no cover
        print(f"[teacher-context] no se pudo marcar estado en {lesson_id}: {exc}")

    return {
        "ok": index_status == "indexed",
        "tutor_updated": index_status == "indexed",
        "transcript_status": transcript_status,
        "index_status": index_status,
        "indexed_at": indexed_at,
        "chunks": int(result.get("chunks") or 0),
        "requires_reindex": requires_reindex,
        "source_type": "teacher_approved_context",
        "message": result.get("message", ""),
    }
