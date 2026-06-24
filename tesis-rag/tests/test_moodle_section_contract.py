import os
import sqlite3
import sys
from contextlib import contextmanager
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes import authoring, sections
from services import db_service, section_service
from services.context_service import build_envelope, render_context_block
from services.agent.retrieval import _context_relation, _scope_affinity


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


def test_upsert_lesson_guarda_moodle_section_id(monkeypatch):
    _reset_sqlite(monkeypatch)

    db_service.upsert_lesson(
        lesson_id="S15-L01",
        course_id="2",
        axis_id="Eje 2",
        moodle_section_id="15",
        title="Leccion con seccion Moodle",
    )

    row = db_service.get_lesson("S15-L01", "2")
    assert row["axis_id"] == ""
    assert row["moodle_section_id"] == "15"


def test_upsert_resource_link_guarda_moodle_section_id(monkeypatch):
    _reset_sqlite(monkeypatch)

    link = db_service.upsert_resource_link(
        resource_id="987",
        lesson_id="S15-L01",
        course_id="2",
        axis_id="Eje 2",
        moodle_section_id="15",
        resource_type="web_page",
        resource_subtype="h5p_video",
    )

    assert link["axis_id"] == ""
    assert link["moodle_section_id"] == "15"
    assert db_service.get_resource_link("987")["moodle_section_id"] == "15"


def test_authoring_upsert_lesson_endpoint_acepta_moodle_section_id(monkeypatch):
    captured = {}

    def fake_upsert_lesson(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(authoring.db_service, "upsert_lesson", fake_upsert_lesson)
    monkeypatch.setattr(
        authoring,
        "load_lesson",
        lambda lesson_id, course_id=None: {
            "lesson_id": lesson_id,
            "axis_id": captured.get("axis_id"),
            "moodle_section_id": captured.get("moodle_section_id"),
        },
    )

    payload = authoring.LessonPayload(
        lesson_id="S15-L02",
        axis_id="Eje 2",
        moodle_section_id="15",
        title="Nueva",
    )
    ctx = SimpleNamespace(course_id="2", user_id="teacher-1")
    response = authoring.upsert_lesson("S15-L02", payload, ctx=ctx)

    assert captured["axis_id"] == ""
    assert captured["moodle_section_id"] == "15"
    assert response["moodle_section_id"] == "15"


def test_sections_link_endpoint_acepta_moodle_section_id(monkeypatch):
    captured = {}

    monkeypatch.setattr(
        sections.section_service,
        "load_lesson",
        lambda lesson_id, course_id=None: {
            "lesson_id": lesson_id,
            "axis_id": "",
            "moodle_section_id": "15",
        },
    )
    async def fake_get_section(course_id, section_id, client=None):
        return {"moodle_section_id": section_id, "section_name": "Tema filtros", "section_order": 3}
    monkeypatch.setattr(sections.section_service, "get_moodle_section", fake_get_section)

    def fake_upsert_resource_link(**kwargs):
        captured.update(kwargs)
        return kwargs

    monkeypatch.setattr(sections.db_service, "upsert_resource_link", fake_upsert_resource_link)

    payload = sections.ResourceLinkPayload(
        lesson_id="S15-L02",
        course_id="2",
        moodle_section_id="15",
        resource_type="web_page",
        resource_subtype="h5p_video",
    )
    import asyncio
    response = asyncio.run(sections.put_link("987", payload, client=object()))

    assert captured["axis_id"] == ""
    assert captured["moodle_section_id"] == "15"
    assert response["moodle_section_id"] == "15"


def test_activity_context_hidrata_y_renderiza_moodle_section(monkeypatch):
    _reset_sqlite(monkeypatch)
    db_service.upsert_lesson(
        lesson_id="S15-L03",
        course_id="2",
        axis_id="Eje 2",
        moodle_section_id="15",
        title="Contexto",
    )

    envelope = build_envelope(
        question="Que estoy viendo?",
        raw_activity_context={
            "current_lesson_id": "S15-L03",
            "current_section_name": "Tema filtros",
            "current_section_order": 3,
        },
        session_id="moodle-section-context",
        has_image=False,
    )
    rendered = render_context_block(envelope)

    assert envelope.activity_context.moodle_section_id == "15"
    assert envelope.activity_context.current_section_name == "Tema filtros"
    assert envelope.activity_context.current_section_order == 3
    # El render etiqueta la seccion Moodle como "Moodle_section_id de la leccion
    # activa: 15" (id) y "Seccion actual: Tema filtros" (nombre). Verificamos el
    # CONTRATO real (que el id y el nombre de seccion lleguen al contexto del
    # tutor), tolerante a la etiqueta exacta para no romper ante cambios de copy.
    assert "moodle_section_id" in rendered.lower() and "15" in rendered
    assert "Tema filtros" in rendered


def test_retrieval_prioriza_moodle_section_id():
    state = {"course_id": "2", "moodle_section_id": "15", "current_lesson_id": "S15-L03"}
    section_meta = {"course_id": "2", "scope": "section", "moodle_section_id": "15", "allowed_for_indexing": True}
    other_meta = {"course_id": "2", "scope": "section", "moodle_section_id": "99", "allowed_for_indexing": True}

    assert _scope_affinity(section_meta, state) == 0.45
    assert _context_relation(section_meta, state) == "same_section"
    assert _context_relation(other_meta, state) == "other_section"


def test_sections_list_fallback_db_sin_moodle_ws(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE mdl_course_sections (
            id INTEGER PRIMARY KEY,
            course INTEGER,
            section INTEGER,
            name TEXT,
            summary TEXT,
            visible INTEGER
        )
        """
    )
    conn.execute(
        "INSERT INTO mdl_course_sections (id, course, section, name, summary, visible) VALUES (?, ?, ?, ?, ?, ?)",
        (15, 2, 1, "Integridad de la informacion", "", 1),
    )
    conn.commit()

    @contextmanager
    def fake_connection():
        yield conn

    monkeypatch.setattr(section_service.db_service, "resolve_course_numeric", lambda course_id: "2")
    monkeypatch.setattr(section_service.db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(section_service.db_service, "_q", lambda: "?")
    monkeypatch.setattr(section_service.db_service, "_moodle_table", lambda name: f"mdl_{name}")
    monkeypatch.setattr(section_service.db_service, "get_connection", fake_connection)

    import asyncio
    sections_list = asyncio.run(
        section_service.list_moodle_sections(
            "Mi42YjU4ZDdhMDdkMjE=",
            client=SimpleNamespace(configured=False),
        )
    )

    assert sections_list[0]["moodle_section_id"] == "15"
    assert sections_list[0]["current_section_name"] == "Integridad de la informacion"
