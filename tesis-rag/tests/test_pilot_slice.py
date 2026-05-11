"""
Pruebas minimas de la vertical slice piloto.

Cubre:
- Carga de manifiestos piloto.
- Resolucion de bloque por timestamp (dentro y fuera de rango).
- Construccion de envelope con pilot_block adjunto.
- Render del bloque activo en el contexto inyectado al prompt.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pilot_service import (
    list_pilot_lessons,
    load_pilot_lesson,
    find_block_at_timestamp,
    resolve_pilot_block,
)
from services.context_service import build_envelope, render_context_block


PILOTOS = ["E2-L01", "E3-L03", "E4-L01"]


def test_listado_y_carga():
    items = list_pilot_lessons()
    ids = {it["lesson_id"] for it in items}
    assert ids == set(PILOTOS), f"Lecciones piloto en manifest: {ids}"

    for lid in PILOTOS:
        lesson = load_pilot_lesson(lid)
        assert lesson, f"No se cargo {lid}"
        assert lesson.get("blocks"), f"{lid} sin bloques"
        for b in lesson["blocks"]:
            for k in ["block_id", "start_time", "end_time", "block_title", "summary",
                      "interaction_mode", "concepts", "preguntas_probables", "tutor_focus"]:
                assert k in b, f"{lid} bloque {b.get('block_id')} sin {k}"


def test_resolucion_dentro_de_rango():
    lesson = load_pilot_lesson("E2-L01")
    block = find_block_at_timestamp(lesson, 100)  # cae en B3 (80-200)
    assert block["block_id"] == "E2-L01-B3", block


def test_resolucion_borde_inferior():
    lesson = load_pilot_lesson("E2-L01")
    block = find_block_at_timestamp(lesson, 0)
    assert block["block_id"] == "E2-L01-B1"


def test_resolucion_fuera_de_rango_cae_al_mas_cercano():
    lesson = load_pilot_lesson("E2-L01")
    block = find_block_at_timestamp(lesson, 9999)
    assert block["block_id"].endswith("B8"), block["block_id"]


def test_envelope_inyecta_bloque_piloto():
    envelope = build_envelope(
        question="que diferencia hay entre EQ correctivo y EQ estetico?",
        raw_activity_context={
            "current_lesson_id": "E3-L03",
            "current_timestamp": 60,  # bloque B2 (35-80)
        },
        session_id="test-session",
        has_image=False,
    )
    assert envelope.pilot_lesson is not None
    assert envelope.pilot_block is not None
    assert envelope.pilot_block["block_id"] == "E3-L03-B2"

    rendered = render_context_block(envelope)
    assert "BLOQUE ACTIVO DEL VIDEO" in rendered
    assert "PUNTO DE PARTIDA" in rendered
    assert "E3-L03-B2" in rendered


def test_envelope_sin_timestamp_no_resuelve_bloque():
    envelope = build_envelope(
        question="hola",
        raw_activity_context={"current_lesson_id": "E3-L03"},
        session_id="test-session",
        has_image=False,
    )
    # leccion piloto detectada, pero sin timestamp no resolvemos bloque
    assert envelope.pilot_lesson is not None
    assert envelope.pilot_block is None


def test_resolve_pilot_block_con_leccion_no_piloto():
    resolved = resolve_pilot_block("lesson_eje2_intro", 30)
    assert resolved == {"lesson": None, "block": None}


if __name__ == "__main__":
    test_listado_y_carga()
    test_resolucion_dentro_de_rango()
    test_resolucion_borde_inferior()
    test_resolucion_fuera_de_rango_cae_al_mas_cercano()
    test_envelope_inyecta_bloque_piloto()
    test_envelope_sin_timestamp_no_resuelve_bloque()
    test_resolve_pilot_block_con_leccion_no_piloto()
    print("OK - todos los tests piloto pasan")
