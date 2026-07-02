"""Modelo pedagógico CANÓNICO unificado (Profesor / Admin / IA).

Fija que:
- PUT /pedagogy (apply_profile mode="replace") escribe el perfil a nivel lección
  (learning_goal, delegated_to_tutor, attribution_constraints, metadata.pedagogy.*,
  prompts) sin tocar estructura ni momentos, y build_profile lo lee de vuelta.
- context_service consume el MISMO perfil: inyecta key_concepts y probable_questions
  a nivel lección y los errores comunes POR MOMENTO (block.metadata.common_mistakes).
- /pedagogy está protegido por require_teacher.
- requires_reindex se mantiene False (campos inyectados, no indexados).
"""
import inspect
import os
import sqlite3
import sys
from contextlib import contextmanager
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes import authoring
from api import dependencies
from services import db_service, pedagogy_profile
from services.context_service import render_context_block
from models.context import TutorContextEnvelope, ActivityContext


CTX = SimpleNamespace(course_id="2", user_id="teacher-1")


def _reset_sqlite(monkeypatch):
    monkeypatch.setenv("TESISAI_FORCE_SQLITE", "1")
    monkeypatch.setenv("TESISAI_ALLOW_SQLITE_FALLBACK", "1")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    @contextmanager
    def fake_connection():
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    monkeypatch.setattr(db_service, "get_connection", fake_connection)
    db_service._INITIALIZED = False
    db_service._BACKEND = None


def _seed(lesson_id="L1", course_id="2"):
    db_service.upsert_lesson(lesson_id=lesson_id, course_id=course_id, moodle_section_id="10", title="Gain staging")
    db_service.replace_lesson_blocks(lesson_id, [
        {"block_id": f"{lesson_id}-B1", "block_order": 0, "start_time": 0, "end_time": 30,
         "block_title": "Intro", "summary": "s1", "tutor_focus": "f1", "concepts": [], "preguntas_probables": []},
    ])


def test_pedagogy_endpoint_usa_require_teacher():
    dep = inspect.signature(authoring.set_pedagogy).parameters["ctx"].default
    assert getattr(dep, "dependency", None) is dependencies.require_teacher


def test_set_pedagogy_escribe_perfil_canonico(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed()

    payload = authoring.PedagogyProfilePayload(
        learning_goal="Comprender el gain staging",
        lesson_summary="Flujo de ganancia y headroom.",
        tutor_tone="socratico",
        help_level="orientar",
        lesson_rules=["Guiar con preguntas"],
        key_concepts=["gain staging", "headroom"],
        common_mistakes=["Saturar el bus"],
        probable_questions=["¿Qué es headroom?"],
        tutor_focus=["Reforzar el criterio auditivo"],
        tutor_must_not_do=["No dar valores fijos"],
        proactive_message="Bienvenido a la clase",
        suggested_prompts=["¿Por dónde empiezo?"],
    )
    authoring.set_pedagogy("L1", payload, ctx=CTX)

    lesson = db_service.get_lesson("L1", "2")
    # Campos vivos + prompts
    assert lesson["learning_goal"] == "Comprender el gain staging"
    assert lesson["delegated_to_tutor"] == ["Reforzar el criterio auditivo"]
    assert lesson["attribution_constraints"] == ["No dar valores fijos"]
    ped = lesson["metadata"]["pedagogy"]
    assert ped["lesson_summary"] == "Flujo de ganancia y headroom."
    assert ped["tutor_tone"] == "socratico"
    assert ped["key_concepts"] == ["gain staging", "headroom"]
    assert ped["probable_questions"] == ["¿Qué es headroom?"]
    assert lesson["metadata"]["requires_reindex"] is False
    # No tocó estructura ni momentos (sigue habiendo 1 bloque intacto).
    blocks = db_service.list_lesson_blocks("L1")
    assert len(blocks) == 1
    assert float(blocks[0]["start_time"]) == 0 and float(blocks[0]["end_time"]) == 30

    # build_profile lee de vuelta el MISMO modelo (round-trip).
    prof = pedagogy_profile.build_profile(db_service.get_lesson("L1", "2"))
    assert prof["learning_goal"] == "Comprender el gain staging"
    assert prof["tutor_focus"] == ["Reforzar el criterio auditivo"]
    assert prof["tutor_must_not_do"] == ["No dar valores fijos"]
    assert prof["key_concepts"] == ["gain staging", "headroom"]
    assert prof["proactive_message"] == "Bienvenido a la clase"
    assert prof["suggested_prompts"] == ["¿Por dónde empiezo?"]


def test_context_inyecta_conceptos_y_preguntas_de_leccion():
    env = TutorContextEnvelope(
        question="q",
        activity_context=ActivityContext(current_lesson_id="L1", current_section_name="Sección"),
        active_lesson={
            "lesson_id": "L1", "lesson_title": "T",
            "metadata": {"pedagogy": {
                "key_concepts": ["headroom", "gain staging"],
                "probable_questions": ["¿Cuánto headroom dejar?"],
            }},
        },
    )
    out = render_context_block(env)
    assert "Conceptos clave de la leccion: headroom, gain staging" in out
    assert "Preguntas probables del alumno en esta leccion:" in out
    assert "¿Cuánto headroom dejar?" in out


def test_context_inyecta_errores_por_momento():
    env = TutorContextEnvelope(
        question="q",
        activity_context=ActivityContext(current_lesson_id="L1", current_timestamp=10),
        active_lesson={"lesson_id": "L1", "lesson_title": "T"},
        active_block={
            "block_id": "L1-B1", "block_title": "Práctica",
            "start_time": 0, "end_time": 30,
            "metadata": {"common_mistakes": ["Confundir peak con RMS"]},
        },
    )
    out = render_context_block(env)
    assert "Errores comunes en este momento:" in out
    assert "Confundir peak con RMS" in out


def test_apply_profile_merge_no_borra_lo_previo(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed()
    # replace: escribe objetivo
    pedagogy_profile.apply_profile("L1", "2", "u", {"learning_goal": "Objetivo A"}, mode="replace")
    # merge con learning_goal vacío: NO debe borrar el previo
    pedagogy_profile.apply_profile("L1", "2", "u", {"tutor_tone": "directo"}, mode="merge")
    lesson = db_service.get_lesson("L1", "2")
    assert lesson["learning_goal"] == "Objetivo A"
    assert lesson["metadata"]["pedagogy"]["tutor_tone"] == "directo"
