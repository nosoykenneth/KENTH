"""
API de autoría del profesor (escritura del "cerebro" del tutor).

Todo está protegido por `require_teacher`: el usuario debe tener rol docente/gestor
en el curso indicado en la cabecera `X-Course-Id` (se valida contra los roles reales
de Moodle). Las escrituras se hacen scoped al curso canónico (id numérico Moodle).

Reusa la capa de persistencia de `services.db_service` (DB Moodle, fallback SQLite)
y la resolución DB-first de `services.lesson_service`.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from api.dependencies import require_teacher, require_course_admin, TeacherContext
from services import db_service, transcription_service
from services.lesson_service import load_lesson


router = APIRouter(prefix="/authoring", tags=["authoring"])


def _index_transcript_safe(course_id: str, lesson_id: str, segments) -> None:
    """Indexa la transcripción en RAG sin romper la respuesta si algo falla."""
    try:
        import ingest  # import perezoso (carga embeddings)
        lesson = db_service.get_lesson(lesson_id, course_id) or {}
        ingest.index_lesson_transcript(
            course_id,
            lesson_id,
            segments,
            moodle_section_id=lesson.get("moodle_section_id", ""),
        )
    except Exception as exc:  # pragma: no cover
        print(f"[transcript-index] fallo indexando {lesson_id}: {exc}")


# ==========================================
# MODELOS
# ==========================================

class PedagogyPayload(BaseModel):
    """Personalización pedagógica que edita el PROFESOR desde la Vista Profesor.

    Se persiste dentro de `metadata.pedagogy` de la lección (sin migración de
    esquema) y se inyecta de forma aditiva en el prompt del tutor
    (`render_context_block`). No re-cablea dominio: tono/nivel son datos.
    """
    model_config = ConfigDict(extra="ignore")
    tutor_tone: str = ""            # directo | paciente | exigente | socratico | practico
    help_level: str = ""           # orientar | explicar | corregir | preguntar | ejemplo_guiado
    lesson_rules: str = ""         # reglas de la lección (texto libre)
    common_mistakes: List[str] = []  # errores comunes a vigilar


class LessonPayload(BaseModel):
    lesson_id: str
    axis_id: str = ""
    moodle_section_id: Optional[str] = None
    title: str = ""
    order: int = 0
    learning_goal: str = ""
    expected_action: str = ""
    learning_goals: List[str] = []
    resources: List[str] = []
    prerequisites: List[str] = []
    delegated_to_tutor: List[str] = []
    attribution_constraints: List[str] = []
    notes: str = ""
    # Personalización pedagógica del profesor (opcional). Si viene, se mergea en
    # metadata.pedagogy preservando el resto de la metadata.
    pedagogy: Optional[PedagogyPayload] = None


class MomentPayload(BaseModel):
    """Edición PEDAGÓGICA de un 'momento' (bloque) por el profesor.

    `extra="forbid"`: el payload NO admite start_time/end_time ni ningún campo
    técnico. Es la barrera server-side (Obligatorio #7): el profesor no puede
    tocar tiempos ni estructura, sin depender de que el front no los envíe.
    """
    model_config = ConfigDict(extra="forbid")
    block_id: str  # referencia obligatoria a un bloque EXISTENTE
    block_title: str = ""
    summary: str = ""
    interaction_mode: str = ""
    tutor_focus: str = ""
    concepts: List[str] = []
    preguntas_probables: List[str] = []


class MomentsPayload(BaseModel):
    moments: List[MomentPayload] = []


class BlockPayload(BaseModel):
    block_id: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    block_title: str = ""
    summary: str = ""
    interaction_mode: str = ""
    tutor_focus: str = ""
    concepts: List[str] = []
    preguntas_probables: List[str] = []


class BlocksPayload(BaseModel):
    blocks: List[BlockPayload] = []


class PromptsPayload(BaseModel):
    proactive_message: str = ""
    suggested_prompts: List[str] = []


class TranscriptSegmentPayload(BaseModel):
    seq: Optional[int] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    text: str = ""
    speaker: str = ""


class TranscriptPayload(BaseModel):
    segments: List[TranscriptSegmentPayload] = []


class AutoTranscribePayload(BaseModel):
    resource_id: int  # cmid del recurso H5P en Moodle
    language: str = "es"


class LessonImportPayload(BaseModel):
    """Esquema de importación de una lección (mismo formato que las semillas
    course_runtime/axes/eje_N/lessons/*.json). Todos los campos son tolerantes;
    la validación dura ocurre en el endpoint."""
    lesson_id: str = ""
    axis_id: str = ""
    moodle_section_id: Optional[str] = None
    lesson_title: str = ""
    title: str = ""
    order: int = 0
    learning_goal: str = ""
    expected_action: str = ""
    learning_goals: List[str] = []
    resources: List[str] = []
    prerequisites: List[str] = []
    delegated_to_tutor: List[str] = []
    attribution_constraints: List[str] = []
    proactive_message: str = ""
    suggested_prompts: List[str] = []
    notes: str = ""
    blocks: List[BlockPayload] = []
    transcript: List[TranscriptSegmentPayload] = []  # opcional


class ResourcePayload(BaseModel):
    resource_id: str
    axis_id: str = ""
    moodle_section_id: Optional[str] = None
    lesson_id: str = ""
    type: str = "lesson_note"
    title: str = ""
    source_uri: str = ""
    duration_seconds: Optional[int] = None
    page_count: Optional[int] = None
    language: str = "es"
    tags: List[str] = []


class ReorderPayload(BaseModel):
    # lista de {id, order} para reordenar ejes o lecciones
    items: List[dict] = []


# ==========================================
# LECCIONES
# ==========================================

@router.put("/lessons/{lesson_id}")
def upsert_lesson(lesson_id: str, payload: LessonPayload, ctx: TeacherContext = Depends(require_teacher)):
    existing = db_service.get_lesson(payload.lesson_id or lesson_id, ctx.course_id) or {}
    section_id = str(payload.moodle_section_id or "").strip()
    if not section_id:
        section_id = str(existing.get("moodle_section_id") or "").strip()
    if not section_id:
        raise HTTPException(status_code=400, detail="moodle_section_id es requerido para guardar lecciones.")
    # metadata se preserva (merge), nunca se pisa: solo se actualiza edited_by.
    metadata = {**(existing.get("metadata") or {}), "edited_by": ctx.user_id}
    # Personalización pedagógica del profesor -> metadata.pedagogy (sin migración).
    # Merge campo a campo para no borrar lo previo si llega parcial.
    if payload.pedagogy is not None:
        prev_ped = dict(metadata.get("pedagogy") or {})
        prev_ped.update(payload.pedagogy.model_dump())
        metadata["pedagogy"] = prev_ped
    db_service.upsert_lesson(
        lesson_id=payload.lesson_id or lesson_id,
        course_id=ctx.course_id,
        axis_id="",
        moodle_section_id=section_id,
        title=payload.title,
        order=payload.order,
        learning_goal=payload.learning_goal,
        expected_action=payload.expected_action,
        learning_goals=payload.learning_goals,
        resources=payload.resources,
        prerequisites=payload.prerequisites,
        delegated_to_tutor=payload.delegated_to_tutor,
        attribution_constraints=payload.attribution_constraints,
        notes=payload.notes,
        metadata=metadata,
    )
    return load_lesson(payload.lesson_id or lesson_id, ctx.course_id)


@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: str, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="LecciÃ³n no encontrada.")
    deleted = db_service.delete_lesson(lesson_id)
    return {"deleted": deleted, "lesson_id": lesson_id}


@router.put("/lessons/{lesson_id}/blocks")
def replace_blocks(lesson_id: str, payload: BlocksPayload, ctx: TeacherContext = Depends(require_course_admin)):
    """Reemplazo TÉCNICO/estructural de bloques (timestamps, alta/baja, reorden).

    Reservado al ADMIN DEL CURSO / técnico (editor avanzado). El profesor NO edita
    aquí: usa `PUT /lessons/{id}/moments` (pedagogía). Barrera server-side, no UI.
    """
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    blocks = []
    for idx, b in enumerate(payload.blocks):
        blocks.append({
            "block_id": b.block_id or f"{lesson_id}-B{idx + 1}",
            "block_order": idx,
            "start_time": b.start_time,
            "end_time": b.end_time,
            "block_title": b.block_title,
            "summary": b.summary,
            "interaction_mode": b.interaction_mode,
            "tutor_focus": b.tutor_focus,
            "concepts": b.concepts,
            "preguntas_probables": b.preguntas_probables,
        })
    count = db_service.replace_lesson_blocks(lesson_id, blocks)
    return {"lesson_id": lesson_id, "blocks": count}


@router.put("/lessons/{lesson_id}/moments")
def update_moments(lesson_id: str, payload: MomentsPayload, ctx: TeacherContext = Depends(require_teacher)):
    """Edición PEDAGÓGICA de 'momentos' (bloques) por el profesor.

    Barrera real en backend (Obligatorio #7): actualiza SOLO campos pedagógicos
    (título/resumen/intención/tutor_focus/concepts/preguntas) EN SU SITIO,
    preservando start_time/end_time/block_order. Rechaza toda alta, baja o cambio
    del conjunto de block_id; los timestamps ni siquiera se aceptan en el payload
    (`extra="forbid"`). El orden técnico existente se conserva (no se reordena).
    """
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")

    existing = db_service.list_lesson_blocks(lesson_id)
    existing_by_id = {str(b.get("block_id")): b for b in existing}
    incoming_by_id: Dict[str, MomentPayload] = {}
    for m in payload.moments:
        bid = str(m.block_id or "").strip()
        if not bid:
            raise HTTPException(status_code=400, detail="Cada momento debe referenciar un block_id existente.")
        if bid in incoming_by_id:
            raise HTTPException(status_code=400, detail=f"block_id duplicado en la petición: {bid}")
        incoming_by_id[bid] = m

    # El conjunto de block_id debe coincidir EXACTAMENTE con el existente:
    # cualquier alta (id nuevo) o baja (id faltante) encubierta se rechaza.
    if set(incoming_by_id.keys()) != set(existing_by_id.keys()):
        raise HTTPException(
            status_code=403,
            detail="No se permite crear, borrar ni cambiar el conjunto de bloques desde la edición de momentos.",
        )

    # Itera en el ORDEN TÉCNICO ya guardado (el profesor no reordena) y actualiza
    # solo lo pedagógico, preservando tiempos y orden.
    merged: List[Dict[str, Any]] = []
    for b in existing:
        bid = str(b.get("block_id"))
        m = incoming_by_id[bid]
        merged.append({
            "block_id": bid,
            "block_order": b.get("block_order"),
            "start_time": b.get("start_time"),   # preservado (no editable por profesor)
            "end_time": b.get("end_time"),       # preservado (no editable por profesor)
            "block_title": m.block_title,
            "summary": m.summary,
            "interaction_mode": m.interaction_mode or b.get("interaction_mode", ""),
            "tutor_focus": m.tutor_focus,
            "concepts": m.concepts,
            "preguntas_probables": m.preguntas_probables,
            "metadata": b.get("metadata", {}),
        })
    count = db_service.replace_lesson_blocks(lesson_id, merged)
    return {"lesson_id": lesson_id, "moments": count}


@router.put("/lessons/{lesson_id}/prompts")
def set_prompts(lesson_id: str, payload: PromptsPayload, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    db_service.set_lesson_prompts(
        lesson_id,
        proactive_message=payload.proactive_message,
        suggested_prompts=payload.suggested_prompts,
    )
    return load_lesson(lesson_id, ctx.course_id)


@router.post("/lessons/import")
def import_lesson(
    payload: LessonImportPayload,
    target_lesson_id: Optional[str] = None,
    ctx: TeacherContext = Depends(require_teacher),
):
    """Importa una lección desde un JSON (crear nueva o rellenar una existente).

    - Si `target_lesson_id` viene (actualizar una lección ya vinculada), se usa esa
      lección y se IGNORA el `lesson_id`/`axis_id` del archivo (el vínculo no se toca).
    - Si no, se crea/actualiza la lección con el `lesson_id`/`axis_id` del archivo.
    Sobreescribe metadatos, bloques, prompts y (si viene) transcripción.
    """
    if target_lesson_id:
        existing = db_service.get_lesson(target_lesson_id, ctx.course_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Lección destino no encontrada.")
        lesson_id = target_lesson_id
        moodle_section_id = existing.get("moodle_section_id") or payload.moodle_section_id or ""
    else:
        if not (payload.lesson_id or "").strip():
            raise HTTPException(status_code=422, detail="El JSON no trae 'lesson_id'.")
        lesson_id = payload.lesson_id.strip()
        moodle_section_id = payload.moodle_section_id or ""
    if not str(moodle_section_id or "").strip():
        raise HTTPException(status_code=422, detail="La lección importada requiere 'moodle_section_id'.")

    title = (payload.lesson_title or payload.title or "").strip()
    if not title:
        raise HTTPException(status_code=422, detail="El JSON no trae 'lesson_title'/'title'.")

    # Validar bloques.
    blocks = []
    for idx, b in enumerate(payload.blocks):
        if b.start_time is None or b.end_time is None:
            raise HTTPException(status_code=422, detail=f"Bloque {idx + 1}: falta start_time o end_time.")
        if float(b.end_time) <= float(b.start_time):
            raise HTTPException(status_code=422, detail=f"Bloque {idx + 1}: end_time debe ser mayor que start_time.")
        blocks.append({
            "block_id": b.block_id or f"{lesson_id}-B{idx + 1}",
            "block_order": idx,
            "start_time": b.start_time,
            "end_time": b.end_time,
            "block_title": b.block_title,
            "summary": b.summary,
            "interaction_mode": b.interaction_mode,
            "tutor_focus": b.tutor_focus,
            "concepts": b.concepts,
            "preguntas_probables": b.preguntas_probables,
        })

    existing_meta = {}
    if target_lesson_id:
        existing_meta = (db_service.get_lesson(target_lesson_id, ctx.course_id) or {}).get("metadata") or {}
    db_service.upsert_lesson(
        lesson_id=lesson_id,
        course_id=ctx.course_id,
        axis_id="",
        moodle_section_id=moodle_section_id,
        title=title,
        order=payload.order,
        learning_goal=payload.learning_goal,
        expected_action=payload.expected_action,
        learning_goals=payload.learning_goals,
        resources=payload.resources,
        prerequisites=payload.prerequisites,
        delegated_to_tutor=payload.delegated_to_tutor,
        attribution_constraints=payload.attribution_constraints,
        notes=payload.notes,
        metadata={**existing_meta, "edited_by": ctx.user_id, "imported": True},
    )
    db_service.replace_lesson_blocks(lesson_id, blocks)
    db_service.set_lesson_prompts(
        lesson_id,
        proactive_message=payload.proactive_message,
        suggested_prompts=payload.suggested_prompts,
    )
    if payload.transcript:
        segs = [{
            "seq": i,
            "start_time": s.start_time,
            "end_time": s.end_time,
            "text": s.text,
            "speaker": s.speaker,
        } for i, s in enumerate(payload.transcript)]
        db_service.replace_transcript(lesson_id, segs)
        _index_transcript_safe(ctx.course_id, lesson_id, segs)

    return load_lesson(lesson_id, ctx.course_id)


@router.get("/lessons/{lesson_id}/transcript")
def get_transcript(lesson_id: str, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    segments = db_service.list_transcript(lesson_id)
    status = transcription_service.get_status(lesson_id)
    return {"lesson_id": lesson_id, "segments": segments, "job": status}


@router.put("/lessons/{lesson_id}/transcript")
def set_transcript(lesson_id: str, payload: TranscriptPayload, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    segments = []
    for idx, s in enumerate(payload.segments):
        segments.append({
            "seq": s.seq if s.seq is not None else idx,
            "start_time": s.start_time,
            "end_time": s.end_time,
            "text": s.text,
            "speaker": s.speaker,
        })
    count = db_service.replace_transcript(lesson_id, segments)
    _index_transcript_safe(ctx.course_id, lesson_id, segments)
    return {"lesson_id": lesson_id, "segments": count}


@router.post("/lessons/{lesson_id}/transcript/auto")
def auto_transcribe(lesson_id: str, payload: AutoTranscribePayload, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    video = db_service.find_hvp_video_path(payload.resource_id)
    if not video:
        raise HTTPException(
            status_code=422,
            detail="No se encontró un archivo de video subido en este H5P. "
                   "La transcripción automática solo funciona con videos alojados en Moodle.",
        )
    lesson = db_service.get_lesson(lesson_id, ctx.course_id) or {}
    job = transcription_service.start_transcription(
        lesson_id, video["path"], payload.language,
        course_id=ctx.course_id, moodle_section_id=lesson.get("moodle_section_id", ""),
    )
    return {"lesson_id": lesson_id, "job": job, "video": {"filename": video.get("filename")}}


@router.get("/lessons/{lesson_id}/transcript/status")
def transcript_status(lesson_id: str, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    status = transcription_service.get_status(lesson_id)
    return {"lesson_id": lesson_id, "job": status}


@router.put("/lessons-reorder")
def reorder_lessons(payload: ReorderPayload, ctx: TeacherContext = Depends(require_course_admin)):
    # Reordenar es estructura técnica -> admin del curso, no el profesor.
    updated = 0
    for item in payload.items:
        lesson_id = item.get("id") or item.get("lesson_id")
        order = item.get("order")
        if not lesson_id or order is None:
            continue
        row = db_service.get_lesson(lesson_id, ctx.course_id)
        if not row:
            continue
        db_service.upsert_lesson(
            lesson_id=lesson_id,
            course_id=row.get("course_id") or ctx.course_id,
            axis_id="",
            moodle_section_id=row.get("moodle_section_id", ""),
            title=row.get("title", ""),
            order=int(order),
            learning_goal=row.get("learning_goal", ""),
            expected_action=row.get("expected_action", ""),
            learning_goals=row.get("learning_goals", []),
            resources=row.get("resources", []),
            prerequisites=row.get("prerequisites", []),
            delegated_to_tutor=row.get("delegated_to_tutor", []),
            attribution_constraints=row.get("attribution_constraints", []),
            notes=row.get("notes", ""),
            metadata=row.get("metadata", {}),
        )
        updated += 1
    return {"updated": updated}


# ==========================================
# RECURSOS
# ==========================================

@router.put("/resources/{resource_id}")
def upsert_resource(resource_id: str, payload: ResourcePayload, ctx: TeacherContext = Depends(require_teacher)):
    db_service.upsert_resource(
        resource_id=payload.resource_id or resource_id,
        course_id=ctx.course_id,
        axis_id="",
        moodle_section_id=payload.moodle_section_id or "",
        lesson_id=payload.lesson_id,
        resource_type=payload.type,
        title=payload.title,
        source_uri=payload.source_uri,
        duration_seconds=payload.duration_seconds,
        page_count=payload.page_count,
        language=payload.language,
        tags=payload.tags,
        metadata={"edited_by": ctx.user_id},
    )
    return db_service.get_resource(payload.resource_id or resource_id)


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: str, ctx: TeacherContext = Depends(require_teacher)):
    deleted = db_service.delete_resource(resource_id)
    return {"deleted": deleted, "resource_id": resource_id}
