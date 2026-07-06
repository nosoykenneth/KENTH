"""Sección 0 teacher-driven RAG — política de fuente activa (Fase 4), regeneración
limpia de momentos (Fase 6) e integridad del manifest de recursos (Fase 3).

No requiere Chroma/Ollama/BD: prueba las piezas deterministas del contrato.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from services import pedagogy_profile


# ---------------------------------------------------------------------------
# Fase 4 — política de fuente activa canonical_md por (curso, sección)
# ---------------------------------------------------------------------------

def test_teacher_flow_desactiva_canonical_solo_en_seccion0(monkeypatch):
    monkeypatch.setattr(config, "RAG_SECTION0_SOURCE_MODE", "teacher_flow")
    monkeypatch.setattr(config, "TEACHER_FLOW_COURSE_ID", "2")
    monkeypatch.setattr(config, "TEACHER_FLOW_SECTION_ID", "2")
    # Sección 0 del curso piloto: canonical_md NO es fuente activa.
    assert config.canonical_md_is_active_source("2", "2") is False
    # Otras secciones del mismo curso NO se tocan.
    assert config.canonical_md_is_active_source("2", "5") is True
    # Otros cursos NO se tocan.
    assert config.canonical_md_is_active_source("3", "2") is True


def test_hybrid_y_canonical_only_mantienen_canonical_activo(monkeypatch):
    monkeypatch.setattr(config, "TEACHER_FLOW_COURSE_ID", "2")
    monkeypatch.setattr(config, "TEACHER_FLOW_SECTION_ID", "2")
    monkeypatch.setattr(config, "RAG_SECTION0_SOURCE_MODE", "hybrid")
    assert config.canonical_md_is_active_source("2", "2") is True
    monkeypatch.setattr(config, "RAG_SECTION0_SOURCE_MODE", "canonical_only")
    assert config.canonical_md_is_active_source("2", "2") is True


def test_ints_y_strings_se_normalizan(monkeypatch):
    monkeypatch.setattr(config, "RAG_SECTION0_SOURCE_MODE", "teacher_flow")
    monkeypatch.setattr(config, "TEACHER_FLOW_COURSE_ID", "2")
    monkeypatch.setattr(config, "TEACHER_FLOW_SECTION_ID", "2")
    assert config.canonical_md_is_active_source(2, 2) is False


# ---------------------------------------------------------------------------
# Fase 6 — fuse_moments: replace_blocks descarta bloques de otra grabación
# ---------------------------------------------------------------------------

_STALE = [
    {"block_id": "L-B1", "block_order": 0, "start_time": 0.0, "end_time": 60.0,
     "block_title": "Panorama Frecuencial (tema viejo)", "summary": "EQ", "concepts": []},
    {"block_id": "L-B2", "block_order": 1, "start_time": 60.0, "end_time": 120.0,
     "block_title": "Ajuste en Batería (tema viejo)", "summary": "EQ2", "concepts": []},
]
_FRESH = [
    {"title": "El oído se adapta", "summary": "igual sonoridad", "start_time": 0.0, "end_time": 40.0},
    {"title": "Nivel de escucha de referencia", "summary": "monitoreo", "start_time": 40.0, "end_time": 90.0},
]


def test_fuse_default_conserva_bloques_viejos():
    """Comportamiento previo (regresión): sin replace_blocks los bloques viejos
    sobreviven junto a los nuevos (la causa raíz del bug de momentos)."""
    merged = pedagogy_profile.fuse_moments(_STALE, _FRESH, lesson_id="SEC2-R56")
    titles = [b["block_title"] for b in merged]
    assert any("tema viejo" in t for t in titles)  # los viejos siguen ahí
    assert "El oído se adapta" in titles


def test_fuse_replace_blocks_descarta_lo_viejo():
    """replace_blocks=True: la línea de tiempo se arma SOLO desde los momentos
    entrantes; ningún título del tema viejo sobrevive."""
    merged = pedagogy_profile.fuse_moments(_STALE, _FRESH, lesson_id="SEC2-R56", replace_blocks=True)
    titles = [b["block_title"] for b in merged]
    assert titles == ["El oído se adapta", "Nivel de escucha de referencia"]
    assert not any("tema viejo" in t for t in titles)
    assert all(str(b["block_id"]).startswith("SEC2-R56-B") for b in merged)


def test_fuse_replace_blocks_ignora_existing_block_id_entrante():
    """Aunque el momento traiga existing_block_id de un bloque viejo, replace_blocks
    lo ignora y crea un bloque fresco (no reancla al tema viejo)."""
    moments = [{"existing_block_id": "L-B1", "title": "Nuevo", "start_time": 0.0, "end_time": 30.0}]
    merged = pedagogy_profile.fuse_moments(_STALE, moments, lesson_id="SEC2-R56", replace_blocks=True)
    assert len(merged) == 1
    assert merged[0]["block_title"] == "Nuevo"
    assert merged[0]["block_id"] != "L-B1"


def test_fuse_replace_blocks_sin_tiempos_no_crea_nada():
    """Sin tiempos válidos no se inventan bloques; apply_profile no borra a ciegas."""
    moments = [{"title": "sin tiempo"}]
    merged = pedagogy_profile.fuse_moments(_STALE, moments, lesson_id="SEC2-R56", replace_blocks=True)
    assert merged == []


# ---------------------------------------------------------------------------
# Fase 3 — integridad del manifest de recursos de la Sección 0
# ---------------------------------------------------------------------------

def test_manifest_cubre_las_7_lecciones_y_es_coherente():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "scripts", "section0_resources_manifest.json")
    data = json.load(open(path, encoding="utf-8"))
    assert data["course_id"] == "2" and data["moodle_section_id"] == "2"
    res = data["resources"]
    lessons = {f"SEC2-R{n}" for n in range(55, 62)}
    by_lesson = {}
    for r in res:
        assert r["lesson_id"] in lessons, r["lesson_id"]
        assert r["kind"] in ("upload", "description")
        assert r["title"].strip() and r["description"].strip()
        if r["kind"] == "upload":
            assert r["file"], r["title"]      # upload necesita binario
        else:
            assert r["file"] is None          # description-only no lleva binario
        by_lesson.setdefault(r["lesson_id"], []).append(r)
    # Las 7 lecciones tienen recursos y todas incluyen sus "Apuntes del profesor".
    assert set(by_lesson) == lessons
    for lid, items in by_lesson.items():
        assert any("Apuntes del profesor" in i["title"] for i in items), lid
