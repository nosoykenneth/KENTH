"""Contrato del RAG por SECCIONES/LECCIONES/BLOQUES (post-migración de ejes).

Pruebas unitarias (sin Chroma/Ollama): metadata obligatoria, scope sin 'axis',
afinidad pedagógica bloque>lección>sección>curso, fallback declarado y
prohibición de axis_id como dependencia funcional.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import db_service
from services.agent import retrieval as R

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(
    BASE_DIR, "documentos", "oficial", "curso_2",
    "seccion_03_integridad_de_la_senal", "contenido_canonico.md",
)

REQUIRED_KEYS = {
    "course_id", "moodle_section_id", "section_id", "section_number",
    "section_title", "section_slug", "lesson_id", "block_id", "resource_id",
    "resource_type", "content_type", "layer", "scope", "source", "source_path",
    "source_hash", "version", "index_status",
}


# --- scope determinista, sin 'axis' ---

def test_doc_scopes_sin_axis():
    assert "axis" not in db_service.DOC_SCOPES
    assert {"block", "lesson", "section", "course", "global"} == set(db_service.DOC_SCOPES)


def test_derive_scope_jerarquia():
    assert db_service.derive_scope("2", "", False, "4") == "section"
    assert db_service.derive_scope("2", "L1", False, "4") == "lesson"
    assert db_service.derive_scope("2", "L1", False, "4", "B1") == "block"
    assert db_service.derive_scope("2", "", False, "") == "course"
    assert db_service.derive_scope("", "", True, "") == "global"


def test_validate_scope_axis_legacy_se_normaliza_a_section():
    sc, ig = db_service.validate_scope(scope="axis", course_id="2", moodle_section_id="4")
    assert sc == "section" and ig is False


# --- metadata del chunk canónico ---

def test_metadata_base_seccional_sin_axis():
    import pytest
    if not os.path.exists(CANON):
        pytest.skip("corpus canonico ausente")
    from ingest import _crear_chunks_markdown
    chunks = _crear_chunks_markdown(CANON)
    assert chunks
    meta = chunks[0].metadata
    # claves obligatorias presentes
    faltan = REQUIRED_KEYS - set(meta.keys())
    assert not faltan, f"faltan claves: {faltan}"
    # anclaje a sección, nunca vacío para contenido seccional
    assert meta["scope"] == "section"
    assert meta["moodle_section_id"] == "4"
    assert meta["section_title"]
    # axis_id PROHIBIDO como campo (solo legacy_axis informativo permitido)
    assert "axis_id" not in meta
    assert "eje" not in meta


# --- afinidad pedagógica por contexto ---

def _meta(**kw):
    base = {"course_id": "2"}
    base.update(kw)
    return base


def test_affinity_jerarquia_block_lesson_section():
    state = {"course_id": "2", "moodle_section_id": "4", "current_lesson_id": "L1",
             "block_id": "B1"}
    a_block = R._scope_affinity(_meta(scope="block", moodle_section_id="4", lesson_id="L1", block_id="B1"), state)
    a_lesson = R._scope_affinity(_meta(scope="lesson", moodle_section_id="4", lesson_id="L1"), state)
    a_section = R._scope_affinity(_meta(scope="section", moodle_section_id="4"), state)
    a_other = R._scope_affinity(_meta(scope="section", moodle_section_id="17"), state)
    assert a_block > a_lesson > a_section > 0
    assert a_block == 1.00 and a_lesson == 0.85 and a_section == 0.60
    assert a_other < 0  # otra sección penaliza


def test_context_relation_other_section():
    state = {"course_id": "2", "moodle_section_id": "4"}
    assert R._context_relation(_meta(scope="section", moodle_section_id="4"), state) == "same_section"
    assert R._context_relation(_meta(scope="section", moodle_section_id="17"), state) == "other_section"
    assert R._context_relation(_meta(scope="global", is_global=True), state) == "global"


def test_curriculum_relation_por_numero_seccion():
    state = {"current_section_order": 4}  # -> sección Moodle 3
    assert R._current_section_number(state) == 3
    assert R._curriculum_relation(state, 3) == "current"
    assert R._curriculum_relation(state, 5) == "future"
    assert R._curriculum_relation(state, 1) == "previous"


if __name__ == "__main__":
    test_doc_scopes_sin_axis()
    test_derive_scope_jerarquia()
    test_validate_scope_axis_legacy_se_normaliza_a_section()
    test_affinity_jerarquia_block_lesson_section()
    test_context_relation_other_section()
    test_curriculum_relation_por_numero_seccion()
    print("OK - rag secciones")
