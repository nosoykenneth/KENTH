"""Cierre UX de la orientación adaptativa (feat/final-ux-guidance-and-thesis-audit).

Cubre las tres correcciones funcionales del cierre:
- FASE 2: la guía cubre VARIOS conceptos débiles, priorizados (1/2/3+), sin
  saturar, con minuto+recurso+micro-práctica y sin exponer internos.
- FASE 3: tono / nivel de ayuda por lección se traducen a directivas OPERATIVAS
  que se inyectan como comportamiento (nunca como RAG) y no eliminan la
  remediación (minuto/recurso).
- FASE 4: el chat GENERAL (sin lección activa) no inventa learning_signals: la
  pregunta personal de progreso recibe respuesta determinística neutral; el
  chat de lección conserva la inyección de señales reales.

Deterministas y sin red (BD/agente mockeados). Ejecutar desde tesis-rag/:
    python -m pytest tests/test_final_ux_guidance.py
"""
import os
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.dependencies import get_current_user_id
from api.routes import chat as chat_mod
from models.context import ActivityContext, TutorContextEnvelope
from services import db_service, learning_signals as ls, pedagogy_profile
from services.context_service import render_context_block


# ---------------------------------------------------------------------------
# Utilidades: mismo mock de BD que test_learning_signals (intento real en R55)
# ---------------------------------------------------------------------------
def _mock_db(monkeypatch, children_scores, grade=6.0):
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
    # guidance_for consulta el help_level de la lección: por defecto no hay lección
    monkeypatch.setattr(db_service, "get_lesson", lambda lid, cid=None: None)


_INTERNOS = ("xAPI", "Chroma", "JSON", "chunk", "backend")


# ---------------------------------------------------------------------------
# FASE 2 — guía multi-concepto priorizada
# ---------------------------------------------------------------------------
def test_guidance_1_debil_concepto_minuto_recurso_micro(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0})  # 80%... fuerza partial con nota
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    # 4/5 = 80% => ready con 1 débil: sugerencia suave sin alerta
    assert s["level"] == ls.LEVEL_READY
    msg = ls.build_guidance_message(s)
    assert "Buen avance" in msg
    assert "minuto" in msg  # la sugerencia suave conserva el minuto
    assert "Conviene reforzar" not in msg  # ready NO alerta refuerzo

    out = ls.guidance_for("40", "SEC2-R55", "2")
    assert out["should_notify"] is False  # ready nunca notifica badge amarillo


def test_guidance_1_debil_needs_pasos_concretos(monkeypatch):
    # 2 fallos del MISMO concepto no existen en R55; usamos score bajo por nota:
    # fallamos 3 para needs y comprobamos el formato de 3+; para 1 débil real
    # usamos partial con 1 fallo y umbral 60-79 vía 2 fallos -> ver test de 2.
    _mock_db(monkeypatch, {"SEC2-R55-I01": 0, "SEC2-R55-I02": 0, "SEC2-R55-I03": 0})
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    assert s["level"] == ls.LEVEL_NEEDS
    msg = ls.build_guidance_message(s)
    assert "Prioridad 1" in msg and "Prioridad 2" in msg and "Prioridad 3" in msg
    assert "Ruta corta" in msg
    for interno in _INTERNOS:
        assert interno not in msg


def test_guidance_2_debiles_cubre_ambos_y_da_orden(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    out = ls.guidance_for("40", "SEC2-R55", "2")
    assert out["should_notify"] is True
    msg = out["message"]
    assert "Conviene reforzar" in msg
    review = out["recommended_review"]
    assert len(review) == 2
    for r in review:
        assert r["concept_label"] in msg, f"debe cubrir {r['concept_label']}"
        assert r["timestamp"] in msg, "cada concepto lleva su minuto"
        assert r["resource"] in msg, "cada concepto lleva su recurso"
    assert "primero revisa" in msg.lower() or "se conectan" in msg.lower()
    for interno in _INTERNOS:
        assert interno not in msg


def test_guidance_3_mas_debiles_prioriza_max_3_sin_saturar(monkeypatch):
    plan = ls.lesson_plan("2", "SEC2-R55")
    wrong = {it["interaction_id"]: 0 for it in plan["interactions"]}  # falla TODO
    _mock_db(monkeypatch, wrong, grade=0.0)
    out = ls.guidance_for("40", "SEC2-R55", "2")
    s = out["signals"]
    assert len(s["weak_concepts"]) >= 4  # hay más débiles que los que se muestran
    assert len(out["recommended_review"]) == 3  # tope 3: no saturar
    msg = out["message"]
    assert "Prioridad 1" in msg and "Prioridad 2" in msg and "Prioridad 3" in msg
    assert "Prioridad 4" not in msg
    assert "Ruta corta" in msg
    # needs_reinforcement: guiado, sin reto avanzado
    assert "reto" not in msg.lower()


def test_prioriza_conceptos_de_menor_score_primero(monkeypatch):
    # I01 y I03 fallados (ratio 0) vs resto correcto: el orden de prioridad
    # respeta el orden pedagógico del manifest al empatar el score.
    _mock_db(monkeypatch, {"SEC2-R55-I01": 0, "SEC2-R55-I03": 0})
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    weak = [w["concept"] for w in s["weak_concepts"]]
    assert weak == ["mezcla_decision", "diagnostico"]  # orden manifest en empate
    review = [r["concept"] for r in s["recommended_review"]]
    assert review == weak[:3]
    # los débiles exponen su score por concepto (para priorización transparente)
    assert all("score" in w and "max_score" in w for w in s["weak_concepts"])


def test_render_block_multi_concepto_lleva_prioridades(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    s = ls.get_lesson_signals("40", "SEC2-R55", "2")
    block = ls.render_signals_block(s)
    assert "Prioridad 1" in block and "Prioridad 2" in block
    assert "PRIORIZADOS" in block
    assert "minuto" in block


def test_guidance_not_attempted_sin_mensaje(monkeypatch):
    monkeypatch.setattr(db_service, "using_moodle_db", lambda: True)
    monkeypatch.setattr(db_service, "get_hvp_instance_id_by_cmid", lambda c: 21)
    monkeypatch.setattr(db_service, "get_hvp_xapi_results", lambda c, u: [])
    monkeypatch.setattr(db_service, "get_hvp_grade", lambda c, u, course=None: None)
    monkeypatch.setattr(db_service, "get_lesson", lambda lid, cid=None: None)
    out = ls.guidance_for("40", "SEC2-R55", "2")
    assert out["status"] == "not_attempted"
    assert out["should_notify"] is False and out["message"] == ""


# ---------------------------------------------------------------------------
# FASE 3 — tono / nivel de ayuda: directivas operativas
# ---------------------------------------------------------------------------
def test_directivas_cubren_todas_las_opciones_de_la_ui():
    # Las opciones REALES de la UI (TutorPedagogyView TONE_OPTIONS/HELP_OPTIONS)
    for tone in ("directo", "paciente", "exigente", "socratico", "practico"):
        assert pedagogy_profile.tone_directive(tone), f"tono sin directiva: {tone}"
    for hl in ("orientar", "explicar", "corregir", "preguntar", "ejemplo_guiado"):
        assert pedagogy_profile.help_directive(hl), f"nivel sin directiva: {hl}"
    # valores vacíos o desconocidos no inyectan nada (default limpio)
    assert pedagogy_profile.tone_directive("") == ""
    assert pedagogy_profile.tone_directive("motivador") == ""
    assert pedagogy_profile.help_directive(None) == ""


def _env_con_pedagogia(tone, help_level):
    return TutorContextEnvelope(
        question="q",
        activity_context=ActivityContext(current_lesson_id="L1", current_section_name="Seccion"),
        active_lesson={
            "lesson_id": "L1", "lesson_title": "T",
            "metadata": {"pedagogy": {"tutor_tone": tone, "help_level": help_level}},
        },
    )


def test_render_inyecta_directivas_operativas_practico_orientar():
    out = render_context_block(_env_con_pedagogia("practico", "orientar"))
    assert "COMO APLICAR EL TONO" in out
    assert "pasos accionables" in out
    assert "COMO APLICAR EL NIVEL DE AYUDA" in out
    assert "pistas" in out
    # el comportamiento nunca borra la remediación de señales
    assert "no omitas el minuto del video ni el recurso" in out


def test_render_inyecta_directivas_socratico_preguntar():
    out = render_context_block(_env_con_pedagogia("socratico", "preguntar"))
    assert "no des la respuesta completa de inmediato" in out
    assert "razonar" in out


def test_render_inyecta_directivas_exigente_corregir():
    out = render_context_block(_env_con_pedagogia("exigente", "corregir"))
    assert "sin ser punitivo" in out
    assert "identifica explícitamente el error" in out


def test_render_sin_pedagogia_no_inyecta_directivas():
    env = TutorContextEnvelope(
        question="q",
        activity_context=ActivityContext(current_lesson_id="L1", current_section_name="Seccion"),
        active_lesson={"lesson_id": "L1", "lesson_title": "T"},
    )
    out = render_context_block(env)
    assert "COMO APLICAR EL TONO" not in out
    assert "COMO APLICAR EL NIVEL DE AYUDA" not in out


def test_guidance_respeta_help_level_sin_perder_minuto_recurso(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    monkeypatch.setattr(
        db_service, "get_lesson",
        lambda lid, cid=None: {"metadata": {"pedagogy": {"help_level": "preguntar"}}},
    )
    out = ls.guidance_for("40", "SEC2-R55", "2")
    msg = out["message"]
    assert "intenta responder" in msg  # cierre estilo 'preguntar'
    # el nivel de ayuda NUNCA elimina la remediación
    assert "minuto" in msg
    assert out["recommended_review"][0]["resource"] in msg


def test_guidance_help_level_ejemplo_guiado(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    monkeypatch.setattr(
        db_service, "get_lesson",
        lambda lid, cid=None: {"metadata": {"pedagogy": {"help_level": "ejemplo_guiado"}}},
    )
    out = ls.guidance_for("40", "SEC2-R55", "2")
    assert "ejemplo guiado" in out["message"]


def test_guidance_help_level_desconocido_usa_orientar(monkeypatch):
    _mock_db(monkeypatch, {"SEC2-R55-I03": 0, "SEC2-R55-I04": 0})
    monkeypatch.setattr(
        db_service, "get_lesson",
        lambda lid, cid=None: {"metadata": {"pedagogy": {"help_level": "wat"}}},
    )
    out = ls.guidance_for("40", "SEC2-R55", "2")
    assert "repasemos el primer punto" in out["message"]


# ---------------------------------------------------------------------------
# FASE 4 — chat general sin lección: neutral, sin señales inventadas
# ---------------------------------------------------------------------------
def test_detector_progreso_personal_positivos():
    for q in (
        "¿Qué debo reforzar?",
        "que tengo que repasar del curso",
        "¿cómo me fue en la actividad?",
        "cuáles son mis resultados",
        "¿en qué fallé?",
        "qué me recomiendas reforzar",
        "necesito saber mi progreso",
    ):
        assert ls.is_personal_progress_question(q), q


def test_detector_progreso_personal_negativos():
    for q in (
        "¿Qué es el gain staging?",
        "cómo voy a rutear un bus de reverb",   # pregunta de contenido, no personal
        "explícame la diferencia entre clip gain y fader",
        "¿qué recursos tiene la lección?",
        "hola",
        "",
    ):
        assert not ls.is_personal_progress_question(q), q


def _chat_client(monkeypatch, agent_should_run):
    """App mínima con el router de chat: agente y persistencia mockeados."""
    app = FastAPI()
    app.include_router(chat_mod.router)
    app.dependency_overrides[get_current_user_id] = lambda: "40"

    llamadas = {"agente": 0}

    def _fake_invoke(estado):
        llamadas["agente"] += 1
        if not agent_should_run:
            raise AssertionError("el agente NO debía ejecutarse en esta ruta")
        return {
            **estado,
            "respuesta_final": "respuesta del agente",
            "evidencias": [],
            "evidence_level": "high",
        }

    monkeypatch.setattr(chat_mod.super_agente, "invoke", _fake_invoke)
    monkeypatch.setattr(chat_mod, "save_interaction_trace", lambda **kw: None)
    monkeypatch.setattr(chat_mod, "save_trace", lambda **kw: None)
    monkeypatch.setattr(chat_mod, "ensure_chat_exists", lambda **kw: None)
    monkeypatch.setattr(chat_mod, "add_message", lambda *a, **kw: {"id": "m1"})
    monkeypatch.setattr(chat_mod, "resolve_course_numeric", lambda c: c or "2")
    return TestClient(app), llamadas


def test_chat_general_progreso_personal_es_deterministico_y_neutral(monkeypatch):
    client, llamadas = _chat_client(monkeypatch, agent_should_run=False)
    resp = client.post("/chat", json={"pregunta": "¿Qué debo reforzar?", "course_id": "2"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "personal_progress_no_lesson"
    assert data["answer_type"] == "deterministic_orientation"
    assert "lección específica" in data["respuesta"]
    assert "señales de aprendizaje" in data["respuesta"]
    assert "general_chat_no_signals" in data["applied_policies"]
    assert data["runtime_context"].get("has_learning_signals") is None
    assert llamadas["agente"] == 0  # nunca llegó al agente ni pudo inventar señales


def test_chat_general_pregunta_normal_va_al_agente(monkeypatch):
    client, llamadas = _chat_client(monkeypatch, agent_should_run=True)
    resp = client.post("/chat", json={"pregunta": "¿Qué es el gain staging?", "course_id": "2"})
    assert resp.status_code == 200
    assert resp.json()["respuesta"] == "respuesta del agente"
    assert llamadas["agente"] == 1


def test_chat_de_leccion_conserva_senales_y_no_deflecta(monkeypatch):
    # Con lesson_id la MISMA pregunta personal sigue el flujo normal (el agente
    # recibe el bloque de señales reales inyectado en el contexto activo).
    client, llamadas = _chat_client(monkeypatch, agent_should_run=True)
    monkeypatch.setattr(
        chat_mod.learning_signals, "signals_block_for",
        lambda uid, lid, cid: "--- SEÑALES DE APRENDIZAJE DEL ESTUDIANTE (runtime, NO ES EVIDENCIA RAG) ---",
    )
    capturado = {}
    original_invoke = chat_mod.super_agente.invoke

    def _capture(estado):
        capturado["block"] = estado.get("activity_context_block", "")
        return original_invoke(estado)

    monkeypatch.setattr(chat_mod.super_agente, "invoke", _capture)
    resp = client.post("/chat", json={
        "pregunta": "¿Qué debo reforzar?",
        "course_id": "2",
        "lesson_id": "SEC2-R55",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] != "personal_progress_no_lesson"
    assert data["runtime_context"]["has_learning_signals"] is True
    assert "SEÑALES DE APRENDIZAJE" in capturado["block"]
