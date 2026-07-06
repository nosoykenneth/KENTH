"""Pruebas de learning_signals: manifest, mapeo resultados->conceptos, niveles,
señales por estudiante, resumen, inyección al tutor y NO indexación en Chroma."""
import json
from pathlib import Path

import pytest

from services import db_service, learning_signals as ls

MANIFEST = Path(__file__).resolve().parent.parent / "data" / "learning_signals" / "course_2_interactions.json"


# ---------------- Manifest ----------------
def test_manifest_valido_7_lecciones_timestamps_dentro_de_duracion():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["course_id"] == "2"
    lessons = m["lessons"]
    assert len(lessons) == 7
    total = 0
    for L in lessons:
        dur = L["duration_seconds"]
        assert L["lesson_id"].startswith("SEC2-R")
        assert 3 <= len(L["interactions"]) <= 5
        for it in L["interactions"]:
            total += 1
            assert 0 <= it["at"] < dur, f"{it['interaction_id']} fuera de duración"
            rr = it["recommended_review"]
            assert 0 <= rr["timestamp_seconds"] < dur
            assert rr["resource"], "cada remediación referencia un recurso real"
            if it["type"] == "multiple_choice":
                assert sum(1 for o in it["options"] if o["correct"]) == 1
    assert total == 29


def test_manifest_recursos_asociados_existen_en_labels():
    for L in json.loads(MANIFEST.read_text(encoding="utf-8"))["lessons"]:
        labels = L["concept_labels"]
        for it in L["interactions"]:
            assert it["concept"] in labels or it["concept"] == "aplicacion"


# ---------------- Utilidades de mapeo ----------------
def test_cmid_desde_lesson_id():
    assert ls._cmid_from_lesson_id("SEC2-R55") == 55
    assert ls._cmid_from_lesson_id("SEC2-R61") == 61
    assert ls._cmid_from_lesson_id("bad") is None


def test_norm_quita_html_y_acentos():
    assert ls._norm("<p>¿Qué és ÉSTO?</p>") == "que es esto"


def test_match_interaction_por_enunciado():
    plan = ls.lesson_plan("2", "SEC2-R55")
    ints = plan["interactions"]
    m = ls._match_interaction(ls._norm("<p>Un diagnóstico útil de un problema de mezcla describe…</p>"), ints)
    assert m is not None and m["concept"] == "diagnostico"


def test_level_umbrales():
    assert ls._level(40) == ls.LEVEL_NEEDS
    assert ls._level(60) == ls.LEVEL_PARTIAL
    assert ls._level(79) == ls.LEVEL_PARTIAL
    assert ls._level(80) == ls.LEVEL_READY


# ---------------- Señales por estudiante (DB mockeada) ----------------
def _mock_db(monkeypatch, children_scores, grade=6.0):
    """children_scores: dict interaction_id->raw (max=1). Simula un intento real."""
    plan = ls.lesson_plan("2", "SEC2-R55")
    rows = [{"id": 100, "parent_id": None, "interaction_type": "compound",
             "description": "IV", "raw_score": sum(children_scores.values()),
             "max_score": len(children_scores)}]
    for i, it in enumerate(plan["interactions"], start=1):
        rid = it["interaction_id"]
        rows.append({"id": 100 + i, "parent_id": 100, "interaction_type": "choice",
                     "description": it["question"], "raw_score": children_scores.get(rid, 1), "max_score": 1})
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: 21)
    monkeypatch.setattr(db_service, "get_hvp_xapi_results", lambda c, u: rows)
    monkeypatch.setattr(db_service, "get_hvp_grade", lambda c, u, course=None: {"finalgrade": grade, "grademax": 10.0})


def test_signals_score_bajo_weak_concepts_y_remediacion(monkeypatch):
    # falla diagnostico + verificacion_ab -> 60% partial, 2 conceptos débiles
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    assert s["status"] == "available"
    assert s["percentage"] == 60
    assert s["level"] == ls.LEVEL_PARTIAL
    weak = {w["concept"] for w in s["weak_concepts"]}
    assert weak == {"diagnostico", "verificacion_ab"}
    concepts_rev = {r["concept"] for r in s["recommended_review"]}
    assert concepts_rev == {"diagnostico", "verificacion_ab"}
    for r in s["recommended_review"]:
        assert r["timestamp"] and r["resource"] and r["micro_practice"]


def test_signals_score_alto_ready_sin_debiles(monkeypatch):
    _mock_db(monkeypatch, {})  # todo correcto
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    assert s["percentage"] == 100 and s["level"] == ls.LEVEL_READY
    assert s["weak_concepts"] == [] and s["recommended_review"] == []


def test_signals_no_intento(monkeypatch):
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: 21)
    monkeypatch.setattr(db_service, "get_hvp_xapi_results", lambda c, u: [])
    monkeypatch.setattr(db_service, "get_hvp_grade", lambda c, u, course=None: None)
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    assert s["status"] == "not_attempted"


def test_signals_lesson_sin_plan_es_empty(monkeypatch):
    s = ls.get_lesson_signals("40", "SEC2-R99", "2")
    assert s["status"] == "empty" and s["h5p_configured"] is False


# ---------------- Render / inyección al tutor ----------------
def test_render_block_no_punitivo_con_timestamp_y_recurso(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    block = ls.render_signals_block(s)
    assert "NO ES EVIDENCIA RAG" in block
    assert "conviene reforzar" in block.lower()
    assert "minuto 2:30" in block
    assert "Bitácora de decisiones de mezcla" in block
    for punitivo in ["vas mal", "nivel bajo", "eres malo"]:
        # el texto puede citar la PROHIBICIÓN, pero no usar la etiqueta como juicio
        assert f"{punitivo}." not in block.lower()


def test_render_block_not_attempted_invita_sin_inventar(monkeypatch):
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: 21)
    monkeypatch.setattr(db_service, "get_hvp_xapi_results", lambda c, u: [])
    monkeypatch.setattr(db_service, "get_hvp_grade", lambda c, u, course=None: None)
    block = ls.render_signals_block(ls.get_lesson_signals("40", "SEC2-R55", "2"))
    assert "NO ha realizado" in block
    assert "No inventes" in block


def test_signals_block_for_defensivo_no_lanza(monkeypatch):
    # si la lectura de BD explota, no debe romper el chat
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: (_ for _ in ()).throw(RuntimeError("db down")))
    assert ls.signals_block_for("40", "SEC2-R55", "2") == ""


# ---------------- Resumen profesor ----------------
def test_lesson_summary_agrega_y_ranking(monkeypatch):
    plan = ls.lesson_plan("2", "SEC2-R55")
    parents = [{"user_id": 40, "raw_score": 3, "max_score": 5},
               {"user_id": 41, "raw_score": 5, "max_score": 5}]
    children = []
    for uid, wrong in [(40, {"SEC2-R55-I03", "SEC2-R55-I04"}), (41, set())]:
        for it in plan["interactions"]:
            children.append({"user_id": uid, "description": it["question"],
                             "raw_score": 0 if it["interaction_id"] in wrong else 1, "max_score": 1})
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: 21)
    monkeypatch.setattr(db_service, "get_hvp_xapi_parents_all", lambda c: parents)
    monkeypatch.setattr(db_service, "get_hvp_xapi_children_all", lambda c: children)
    out = ls.get_lesson_summary("2", "SEC2-R55")
    assert out["status"] == "available"
    assert out["students_with_results"] == 2
    assert out["average_percentage"] == 80
    assert out["level_distribution"]["ready"] == 1
    top = {c["concept"] for c in out["most_failed_concepts"]}
    assert {"diagnostico", "verificacion_ab"} <= top


def test_sync_idempotente(monkeypatch):
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: 21)
    monkeypatch.setattr(db_service, "get_hvp_xapi_parents_all", lambda c: [])
    monkeypatch.setattr(db_service, "get_hvp_xapi_children_all", lambda c: [])
    a = ls.sync_lesson("2", "SEC2-R55")
    b = ls.sync_lesson("2", "SEC2-R55")
    assert a == b
    assert a["status"] == "no_results"
