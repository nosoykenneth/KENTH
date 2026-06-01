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
from services.agent.retrieval import (
    _current_axis_number,
    _is_future_axis_question,
    _question_axis_number,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_markdown_chunks_preservan_eje_y_capa():
    path = os.path.join(
        BASE_DIR,
        "documentos",
        "oficial",
        "ejes",
        "eje_2_integridad_senal",
        "01_contenido_canonico.md",
    )
    chunks = _crear_chunks_markdown(path)
    assert chunks, "No se generaron chunks del contenido canonico"

    meta = chunks[0].metadata
    assert meta["axis"] == "Eje 2", meta
    assert meta["eje"] == "Eje 2", meta
    assert meta["axis_id"] == "Eje 2", meta
    assert meta["layer"] == "canonico", meta
    assert meta["source_origin"] == "course", meta
    assert meta["status"] == "ready_for_indexing", meta


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


def test_politica_detecta_eje_posterior_desde_contexto_actual():
    envelope = build_envelope(
        question="Que hace realmente el threshold?",
        raw_activity_context={
            "current_lesson_id": "E2-L01",
            "current_timestamp": 250,
        },
        session_id="future-axis-test",
        has_image=False,
    )
    state = {"tutor_envelope": envelope}

    assert _current_axis_number(state) == 2
    assert _question_axis_number("Que hace realmente el threshold?") == 4
    assert _is_future_axis_question(state, "Que hace realmente el threshold?")


if __name__ == "__main__":
    test_markdown_chunks_preservan_eje_y_capa()
    test_bloque_piloto_es_runtime_y_no_evidencia()
    test_politica_detecta_eje_posterior_desde_contexto_actual()
    print("OK - source policy")
