"""
Pruebas de politica de fuentes del tutor contextual.

Cubren la regla A/B/C:
- A: chunks indexables conservan eje y capa desde frontmatter.
- B: el bloque piloto entra como contexto runtime, no como evidencia RAG.
- C: la politica curricular detecta anticipos de ejes posteriores.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingest import _crear_chunks_markdown
from services.context_service import build_envelope, render_context_block
from services.agent.retrieval import _current_section_number, _curriculum_relation


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_markdown_chunks_anclan_seccion_sin_axis():
    # Corpus canonico por seccion (arquitectura nueva). Eje quedo deprecado.
    path = os.path.join(
        BASE_DIR, "documentos", "oficial", "curso_2",
        "seccion_03_integridad_de_la_senal", "contenido_canonico.md",
    )
    if not os.path.exists(path):
        import pytest
        pytest.skip(f"corpus canonico ausente en este checkout: {path}")

    chunks = _crear_chunks_markdown(path)
    assert chunks, "No se generaron chunks del contenido canonico"

    meta = chunks[0].metadata
    # Contrato vigente: el chunk se ancla a la SECCION Moodle, no al eje.
    assert meta["moodle_section_id"] == "4", meta
    assert meta["section_id"] == "4", meta
    assert meta["section_title"] == "SECCIÓN 2: Integridad de la señal", meta
    assert meta["scope"] == "section", meta
    assert meta["layer"] == "canonical", meta
    assert meta["source"] == "canonical_md", meta
    # axis_id PROHIBIDO en el indice nuevo (solo traza legacy informativa permitida).
    assert "axis_id" not in meta, meta
    assert not str(meta.get("axis") or ""), meta


def test_bloque_piloto_es_runtime_y_no_evidencia():
    envelope = build_envelope(
        question="El HPF se decide en solo o en mezcla?",
        raw_activity_context={
            "current_lesson_id": "E2-L01",
            "current_timestamp": 250,
        },
        session_id="source-policy-test",
        has_image=False,
    )
    rendered = render_context_block(envelope)

    assert "BLOQUE ACTIVO DEL VIDEO (PUNTO DE PARTIDA)" in rendered
    assert "NO ES EVIDENCIA RAG" in rendered
    assert "preguntas probables son pistas runtime" in rendered
    assert envelope.active_block["block_id"] == "E2-L01-B4"


def test_politica_ubica_alumno_por_numero_de_seccion():
    envelope = build_envelope(
        question="Que hace realmente el threshold?",
        raw_activity_context={
            "current_lesson_id": "E2-L01",
            "current_timestamp": 250,
            # El numero de seccion Moodle del alumno se deriva del ORDEN de la
            # seccion (order-1): order=4 -> seccion Moodle 3 (order 1 = Bienvenida).
            "current_section_order": 4,
        },
        session_id="curricular-test",
        has_image=False,
    )
    state = {"tutor_envelope": envelope}

    assert _current_section_number(state) == 3
    # Un chunk de la MISMA seccion (3) es 'current'; uno posterior (5) es 'future'.
    assert _curriculum_relation(state, 3) == "current"
    assert _curriculum_relation(state, 5) == "future"
    assert _curriculum_relation(state, 1) == "previous"


if __name__ == "__main__":
    test_markdown_chunks_preservan_eje_y_capa()
    test_bloque_piloto_es_runtime_y_no_evidencia()
    test_politica_detecta_eje_posterior_desde_contexto_actual()
    print("OK - source policy")
