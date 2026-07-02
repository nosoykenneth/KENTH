"""FASE 6 — el CONTEXTO inyectado al tutor no expone identificadores técnicos.

Fija que `render_context_block`:
  - NO emite block_id ni lesson_id (códigos tipo S0-L01-B4) como texto que el LLM lea.
  - SÍ conserva la sección como grounding (moodle_section_id) — contrato de retrieval,
    y el tutor no la verbaliza gracias a la instrucción anti-fuga.
  - SÍ usa lenguaje humano: título de la lección, título del momento, minutos (m:ss).
  - Inyecta el "Resumen de la leccion" desde metadata.pedagogy.lesson_summary
    (antes era un campo muerto — auditoría #1).
  - Incluye la instrucción anti-fuga de identificadores internos.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.context_service import render_context_block, _fmt_mmss, _fmt_rango
from models.context import TutorContextEnvelope, ActivityContext


def _env():
    return TutorContextEnvelope(
        question="¿Qué es el headroom?",
        activity_context=ActivityContext(current_lesson_id="S0-L01", current_timestamp=65),
        active_lesson={
            "lesson_id": "S0-L01",
            "lesson_title": "Gain staging",
            "moodle_section_id": "10",
            "section_name": "Sección 2: Integridad de la señal",
            "learning_goal": "Comprender el flujo de ganancia",
            "metadata": {"pedagogy": {"lesson_summary": "La clase explica el flujo de ganancia y el headroom."}},
        },
        active_block={
            "block_id": "S0-L01-B4",
            "block_title": "Práctica de gain staging",
            "start_time": 60,
            "end_time": 90,
            "summary": "Se ajusta la ganancia de entrada",
            "interaction_mode": "practica",
            "concepts": ["headroom"],
            "preguntas_probables": ["¿Cuánto headroom dejar?"],
        },
    )


def test_no_expone_block_id_ni_lesson_id():
    out = render_context_block(_env())
    assert "S0-L01-B4" not in out          # block_id (código que el tutor podría repetir)
    assert "S0-L01" not in out             # lesson_id (ni siquiera como prefijo)


def test_conserva_seccion_como_grounding():
    # La sección se mantiene (contrato de retrieval / "no romper moodle_section_id");
    # el tutor no la verbaliza gracias a la instrucción anti-fuga.
    out = render_context_block(_env())
    assert "Sección 2: Integridad de la señal" in out


def test_usa_lenguaje_humano():
    out = render_context_block(_env())
    # Encabezado técnico interno se conserva (contrato de otros tests), pero los
    # VALORES del bloque/lección son títulos + minutos humanos, no ids.
    assert "Gain staging" in out                  # título de lección
    assert "Práctica de gain staging" in out      # título del momento
    assert "1:00" in out                          # rango humanizado 1:00–1:30
    assert "1:05" in out                          # timestamp del alumno (65s)


def test_inyecta_resumen_de_leccion():
    out = render_context_block(_env())
    assert "Resumen de la leccion" in out
    assert "La clase explica el flujo de ganancia y el headroom." in out


def test_incluye_instruccion_antifuga():
    out = render_context_block(_env())
    assert "identificadores internos" in out


def test_helpers_de_tiempo():
    assert _fmt_mmss(0) == "0:00"
    assert _fmt_mmss(65) == "1:05"
    assert _fmt_mmss(None) == ""
    assert _fmt_rango(60, 90) == "1:00–1:30"
