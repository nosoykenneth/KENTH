"""
API de autoría del profesor (escritura del "cerebro" del tutor).

Todo está protegido por `require_teacher`: el usuario debe tener rol docente/gestor
en el curso indicado en la cabecera `X-Course-Id` (se valida contra los roles reales
de Moodle). Las escrituras se hacen scoped al curso canónico (id numérico Moodle).

Reusa la capa de persistencia de `services.db_service` (DB Moodle, fallback SQLite)
y la resolución DB-first de `services.axis_service`.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.dependencies import require_teacher, TeacherContext
from services import db_service, transcription_service
from services.axis_service import _canonical_axis_id, load_axis_manifest, load_lesson


router = APIRouter(prefix="/authoring", tags=["authoring"])


def _index_transcript_safe(course_id: str, lesson_id: str, segments) -> None:
    """Indexa la transcripción en RAG sin romper la respuesta si algo falla."""
    try:
        import ingest  # import perezoso (carga embeddings)
        lesson = db_service.get_lesson(lesson_id, course_id) or {}
        ingest.index_lesson_transcript(
            course_id, lesson_id, segments, axis_id=lesson.get("axis_id", ""),
        )
    except Exception as exc:  # pragma: no cover
        print(f"[transcript-index] fallo indexando {lesson_id}: {exc}")


# ==========================================
# MODELOS
# ==========================================

class AxisPayload(BaseModel):
    axis_id: str
    axis_number: int = 0
    axis_slug: str = ""
    title: str = ""
    pedagogical_role: str = ""
    doc_root: str = ""
    status: str = ""
    axis_order: int = 0
    primary_resources: List[str] = []
    derived_resources: List[str] = []


class LessonPayload(BaseModel):
    lesson_id: str
    axis_id: str
    title: str = ""
    order: int = 0
    learning_goal: str = ""
    expected_action: str = ""
    learning_goals: List[str] = []
    expected_actions: List[str] = []
    source_script_file: str = ""
    resources: List[str] = []
    prerequisites: List[str] = []
    notes: str = ""


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
    lesson_title: str = ""
    title: str = ""
    order: int = 0
    learning_goal: str = ""
    expected_action: str = ""
    learning_goals: List[str] = []
    expected_actions: List[str] = []
    source_script_file: str = ""
    resources: List[str] = []
    prerequisites: List[str] = []
    proactive_message: str = ""
    suggested_prompts: List[str] = []
    notes: str = ""
    blocks: List[BlockPayload] = []
    transcript: List[TranscriptSegmentPayload] = []  # opcional


class ResourcePayload(BaseModel):
    resource_id: str
    axis_id: str = ""
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
# EJES
# ==========================================

@router.put("/axes/{axis_id}")
def upsert_axis(axis_id: str, payload: AxisPayload, ctx: TeacherContext = Depends(require_teacher)):
    canonical = _canonical_axis_id(payload.axis_id or axis_id)
    db_service.upsert_axis(
        axis_id=canonical,
        course_id=ctx.course_id,
        axis_number=payload.axis_number,
        axis_slug=payload.axis_slug or canonical.lower().replace(" ", "_"),
        title=payload.title,
        pedagogical_role=payload.pedagogical_role,
        doc_root=payload.doc_root,
        status=payload.status,
        axis_order=payload.axis_order or payload.axis_number,
        metadata={
            "primary_resources": payload.primary_resources,
            "derived_resources": payload.derived_resources,
        },
    )
    return load_axis_manifest(canonical, ctx.course_id)


@router.delete("/axes/{axis_id}")
def delete_axis(axis_id: str, ctx: TeacherContext = Depends(require_teacher)):
    canonical = _canonical_axis_id(axis_id)
    lessons = db_service.list_lessons(axis_id=canonical, course_id=ctx.course_id)
    if lessons:
        raise HTTPException(
            status_code=409,
            detail=f"El eje '{canonical}' tiene {len(lessons)} lección(es). Bórralas o muévelas antes de eliminar el eje.",
        )
    deleted = db_service.delete_axis(canonical, ctx.course_id)
    return {"deleted": deleted, "axis_id": canonical}


# ==========================================
# LECCIONES
# ==========================================

@router.put("/lessons/{lesson_id}")
def upsert_lesson(lesson_id: str, payload: LessonPayload, ctx: TeacherContext = Depends(require_teacher)):
    canonical_axis = _canonical_axis_id(payload.axis_id)
    db_service.upsert_lesson(
        lesson_id=payload.lesson_id or lesson_id,
        course_id=ctx.course_id,
        axis_id=canonical_axis,
        title=payload.title,
        order=payload.order,
        learning_goal=payload.learning_goal,
        expected_action=payload.expected_action,
        learning_goals=payload.learning_goals,
        expected_actions=payload.expected_actions,
        source_script_file=payload.source_script_file,
        resources=payload.resources,
        prerequisites=payload.prerequisites,
        notes=payload.notes,
        metadata={"edited_by": ctx.user_id},
    )
    return load_lesson(payload.lesson_id or lesson_id, ctx.course_id)


@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: str, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="LecciÃ³n no encontrada.")
    deleted = db_service.delete_lesson(lesson_id)
    return {"deleted": deleted, "lesson_id": lesson_id}


@router.put("/lessons/{lesson_id}/blocks")
def replace_blocks(lesson_id: str, payload: BlocksPayload, ctx: TeacherContext = Depends(require_teacher)):
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
        axis_id = existing.get("axis_id") or _canonical_axis_id(payload.axis_id)
    else:
        if not (payload.lesson_id or "").strip():
            raise HTTPException(status_code=422, detail="El JSON no trae 'lesson_id'.")
        if not (payload.axis_id or "").strip():
            raise HTTPException(status_code=422, detail="El JSON no trae 'axis_id'.")
        lesson_id = payload.lesson_id.strip()
        axis_id = _canonical_axis_id(payload.axis_id)

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

    db_service.upsert_lesson(
        lesson_id=lesson_id,
        course_id=ctx.course_id,
        axis_id=axis_id,
        title=title,
        order=payload.order,
        learning_goal=payload.learning_goal,
        expected_action=payload.expected_action,
        learning_goals=payload.learning_goals,
        expected_actions=payload.expected_actions,
        source_script_file=payload.source_script_file,
        resources=payload.resources,
        prerequisites=payload.prerequisites,
        notes=payload.notes,
        metadata={"edited_by": ctx.user_id, "imported": True},
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
        course_id=ctx.course_id, axis_id=lesson.get("axis_id", ""),
    )
    return {"lesson_id": lesson_id, "job": job, "video": {"filename": video.get("filename")}}


@router.get("/lessons/{lesson_id}/transcript/status")
def transcript_status(lesson_id: str, ctx: TeacherContext = Depends(require_teacher)):
    if not db_service.get_lesson(lesson_id, ctx.course_id):
        raise HTTPException(status_code=404, detail="Lección no encontrada.")
    status = transcription_service.get_status(lesson_id)
    return {"lesson_id": lesson_id, "job": status}


@router.put("/lessons-reorder")
def reorder_lessons(payload: ReorderPayload, ctx: TeacherContext = Depends(require_teacher)):
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
            axis_id=row.get("axis_id", ""),
            title=row.get("title", ""),
            order=int(order),
            learning_goal=row.get("learning_goal", ""),
            expected_action=row.get("expected_action", ""),
            learning_goals=row.get("learning_goals", []),
            expected_actions=row.get("expected_actions", []),
            source_script_file=row.get("source_script_file", ""),
            resources=row.get("resources", []),
            prerequisites=row.get("prerequisites", []),
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
        axis_id=_canonical_axis_id(payload.axis_id) if payload.axis_id else "",
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
