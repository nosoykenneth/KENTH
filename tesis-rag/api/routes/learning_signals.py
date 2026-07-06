"""Endpoints de learning_signals — desempeño del estudiante en las actividades
H5P, expuesto como señales pedagógicas.

Ruta externa (vía gateway `/api/ai/*`):
  GET  /api/ai/learning-signals/lesson/{lesson_id}/me       (estudiante: sus señales)
  GET  /api/ai/learning-signals/lesson/{lesson_id}/summary  (profesor/admin: resumen)
  POST /api/ai/learning-signals/sync/lesson/{lesson_id}     (usuario del curso: recalcula su snapshot)

Permisos:
  - /me         -> token del alumno (get_current_user_id); solo devuelve SUS señales.
  - /summary    -> require_teacher (rol docente/gestor del curso).
  - /sync       -> require_course_view; idempotente, devuelve solo snapshot del usuario.
  - /guidance   -> require_course_view; mensaje listo para UI sin modelo ni Chroma.
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Header, Query

from api.dependencies import get_current_user_id, require_teacher, require_course_view, TeacherContext
from services import learning_signals
from services.db_service import resolve_course_numeric

router = APIRouter(prefix="/learning-signals", tags=["learning-signals"])


def _resolve_course(course_id: Optional[str], x_course_id: Optional[str]) -> str:
    raw = (x_course_id or course_id or "2").strip()
    return resolve_course_numeric(raw) or raw


@router.get("/lesson/{lesson_id}/me")
def lesson_signals_me(
    lesson_id: str,
    user_id: str = Depends(get_current_user_id),
    course_id: Optional[str] = Query(default=None),
    x_course_id: Optional[str] = Header(default=None, alias="X-Course-Id"),
):
    """Señales del estudiante autenticado para una lección. El user_id proviene
    del token validado; el payload nunca puede pedir señales de otro alumno."""
    resolved = _resolve_course(course_id, x_course_id)
    return learning_signals.get_lesson_signals(user_id, lesson_id, resolved)


@router.get("/lesson/{lesson_id}/summary")
def lesson_signals_summary(
    lesson_id: str,
    ctx: TeacherContext = Depends(require_teacher),
):
    """Resumen agregado para profesor/admin del curso: distribución de niveles,
    promedio, conceptos más fallados, cantidad de intentos/completion."""
    return learning_signals.get_lesson_summary(ctx.course_id, lesson_id)


@router.post("/sync/lesson/{lesson_id}")
def lesson_signals_sync(
    lesson_id: str,
    ctx: TeacherContext = Depends(require_course_view),
):
    """Recalcula señales desde Moodle/H5P para el usuario autenticado.

    Los resultados ya viven en Moodle; esta operación no escribe en Chroma ni
    expone agregados de otros estudiantes.
    """
    return learning_signals.sync_lesson_for_user(ctx.user_id, ctx.course_id, lesson_id)


@router.post("/lesson/{lesson_id}/guidance")
def lesson_signals_guidance(
    lesson_id: str,
    ctx: TeacherContext = Depends(require_course_view),
):
    """Devuelve orientación determinística basada en learning_signals del usuario."""
    return learning_signals.guidance_for(ctx.user_id, lesson_id, ctx.course_id)
