"""Contrato de separación de roles en la autoría (rediseño por roles).

Fija el Obligatorio #7: el profesor edita 'momentos' (pedagogía) pero NO puede
tocar tiempos ni estructura técnica de los bloques. La barrera es server-side:
- PUT /lessons/{id}/moments (require_teacher) actualiza in-place y preserva
  start_time/end_time/orden; rechaza altas/bajas y ni siquiera admite timestamps.
- PUT /lessons/{id}/blocks (require_course_admin) es el reemplazo técnico completo.

También cubre: persistencia de la personalización pedagógica en metadata.pedagogy,
su inyección aditiva en el prompt del tutor, y los guards require_course_admin /
require_rag_admin.
"""
import os
import sqlite3
import sys
from contextlib import contextmanager
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes import authoring
from api import dependencies
from services import db_service
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


def _seed_lesson_with_blocks(lesson_id="L1", course_id="2"):
    db_service.upsert_lesson(
        lesson_id=lesson_id, course_id=course_id, moodle_section_id="10", title="Leccion",
    )
    db_service.replace_lesson_blocks(lesson_id, [
        {"block_id": f"{lesson_id}-B1", "block_order": 0, "start_time": 0, "end_time": 10,
         "block_title": "Momento 1", "summary": "s1", "tutor_focus": "f1",
         "concepts": [], "preguntas_probables": []},
        {"block_id": f"{lesson_id}-B2", "block_order": 1, "start_time": 10, "end_time": 25,
         "block_title": "Momento 2", "summary": "s2", "tutor_focus": "f2",
         "concepts": [], "preguntas_probables": []},
    ])


# ---------------------------------------------------------------------------
# /moments: edición pedagógica in-place, preservando estructura
# ---------------------------------------------------------------------------

def test_moments_actualiza_pedagogia_y_preserva_tiempos(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_lesson_with_blocks()

    payload = authoring.MomentsPayload(moments=[
        authoring.MomentPayload(block_id="L1-B1", block_title="Momento 1 EDIT", summary="nuevo1", tutor_focus="ff1"),
        authoring.MomentPayload(block_id="L1-B2", block_title="Momento 2 EDIT", summary="nuevo2"),
    ])
    res = authoring.update_moments("L1", payload, ctx=CTX)
    assert res["moments"] == 2

    blocks = {b["block_id"]: b for b in db_service.list_lesson_blocks("L1")}
    assert blocks["L1-B1"]["block_title"] == "Momento 1 EDIT"
    assert blocks["L1-B1"]["summary"] == "nuevo1"
    assert blocks["L1-B1"]["tutor_focus"] == "ff1"
    # Tiempos y orden preservados: el profesor no los edita por este endpoint.
    assert float(blocks["L1-B1"]["start_time"]) == 0
    assert float(blocks["L1-B1"]["end_time"]) == 10
    assert float(blocks["L1-B2"]["start_time"]) == 10
    assert float(blocks["L1-B2"]["end_time"]) == 25


def test_moments_rechaza_alta_de_bloque(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_lesson_with_blocks()
    payload = authoring.MomentsPayload(moments=[
        authoring.MomentPayload(block_id="L1-B1"),
        authoring.MomentPayload(block_id="L1-B2"),
        authoring.MomentPayload(block_id="L1-B3"),  # id nuevo -> alta encubierta
    ])
    with pytest.raises(HTTPException) as exc:
        authoring.update_moments("L1", payload, ctx=CTX)
    assert exc.value.status_code == 403


def test_moments_rechaza_baja_de_bloque(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_lesson_with_blocks()
    payload = authoring.MomentsPayload(moments=[
        authoring.MomentPayload(block_id="L1-B1"),  # falta B2 -> baja encubierta
    ])
    with pytest.raises(HTTPException) as exc:
        authoring.update_moments("L1", payload, ctx=CTX)
    assert exc.value.status_code == 403


def test_moment_payload_prohibe_campos_tecnicos():
    # extra="forbid": el profesor no puede ni EXPRESAR cambios de tiempo/estructura.
    for kwargs in ({"start_time": 5}, {"end_time": 99}, {"block_order": 3}):
        with pytest.raises(Exception):
            authoring.MomentPayload(block_id="L1-B1", **kwargs)


# ---------------------------------------------------------------------------
# Personalización pedagógica: persistencia en metadata + inyección aditiva
# ---------------------------------------------------------------------------

def test_upsert_lesson_persiste_pedagogia_en_metadata(monkeypatch):
    _reset_sqlite(monkeypatch)
    db_service.upsert_lesson(lesson_id="L1", course_id="2", moodle_section_id="10", title="T")

    payload = authoring.LessonPayload(
        lesson_id="L1", moodle_section_id="10", title="T",
        pedagogy=authoring.PedagogyPayload(
            tutor_tone="socratico", help_level="orientar",
            lesson_rules="No des la respuesta directa.",
            common_mistakes=["confundir X con Y"],
        ),
    )
    authoring.upsert_lesson("L1", payload, ctx=CTX)

    row = db_service.get_lesson("L1", "2")
    ped = (row.get("metadata") or {}).get("pedagogy") or {}
    assert ped["tutor_tone"] == "socratico"
    assert ped["help_level"] == "orientar"
    assert ped["common_mistakes"] == ["confundir X con Y"]
    assert row["metadata"].get("edited_by") == "teacher-1"  # merge no pisa lo previo


def test_render_inyecta_pedagogia_aditiva():
    env = TutorContextEnvelope(
        question="q",
        activity_context=ActivityContext(current_lesson_id="L1", current_section_name="Seccion"),
        active_lesson={
            "lesson_id": "L1", "lesson_title": "T",
            "metadata": {"pedagogy": {
                "tutor_tone": "socratico", "help_level": "orientar",
                "lesson_rules": "No des la respuesta directa.",
                "common_mistakes": ["confundir X con Y"],
            }},
        },
    )
    out = render_context_block(env)
    assert "socratico" in out
    assert "Nivel de ayuda esperado" in out
    assert "No des la respuesta directa." in out
    assert "confundir X con Y" in out


def test_render_sin_pedagogia_no_inyecta():
    env = TutorContextEnvelope(
        question="q",
        activity_context=ActivityContext(current_lesson_id="L1", current_section_name="Seccion"),
        active_lesson={"lesson_id": "L1", "lesson_title": "T"},
    )
    out = render_context_block(env)
    assert "Tono del tutor solicitado" not in out
    assert "Nivel de ayuda esperado" not in out


# ---------------------------------------------------------------------------
# Guards de rol (deterministas, con Moodle DB simulada)
# ---------------------------------------------------------------------------

def _force_moodle(monkeypatch, user_id="u1"):
    monkeypatch.setattr(dependencies, "get_current_user_id", lambda *a, **k: user_id)
    monkeypatch.setattr(dependencies, "using_moodle_db", lambda: True)
    monkeypatch.setattr(dependencies, "resolve_course_numeric", lambda cid: "2")


def test_require_course_admin_bloquea_no_admin(monkeypatch):
    _force_moodle(monkeypatch)
    monkeypatch.setattr(dependencies, "is_course_admin", lambda uid, cid: False)
    with pytest.raises(HTTPException) as exc:
        dependencies.require_course_admin(authorization="Bearer x", x_course_id="2", x_dev_user_id=None)
    assert exc.value.status_code == 403


def test_require_course_admin_permite_admin(monkeypatch):
    _force_moodle(monkeypatch)
    monkeypatch.setattr(dependencies, "is_course_admin", lambda uid, cid: True)
    ctx = dependencies.require_course_admin(authorization="Bearer x", x_course_id="2", x_dev_user_id=None)
    assert ctx.course_id == "2"
    assert ctx.user_id == "u1"


def test_require_rag_admin_bloquea_no_siteadmin(monkeypatch):
    _force_moodle(monkeypatch)
    monkeypatch.setattr(dependencies, "is_site_admin", lambda uid: False)
    with pytest.raises(HTTPException) as exc:
        dependencies.require_rag_admin(authorization="Bearer x", x_dev_user_id=None)
    assert exc.value.status_code == 403


def test_require_rag_admin_permite_siteadmin(monkeypatch):
    _force_moodle(monkeypatch)
    monkeypatch.setattr(dependencies, "is_site_admin", lambda uid: True)
    uid = dependencies.require_rag_admin(authorization="Bearer x", x_dev_user_id=None)
    assert uid == "u1"
