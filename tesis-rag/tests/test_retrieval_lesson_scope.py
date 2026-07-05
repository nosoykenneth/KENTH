import os
import sys
from types import SimpleNamespace

from langchain_core.documents import Document

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes.chat import _fuentes_visibles_al_alumno
from services.agent import retrieval as R


def _item(lesson_id, score=1.0, source="canonical_md", visible=True):
    return {
        "document": Document(
            page_content=f"contenido {lesson_id or 'section'} {source}",
            metadata={
                "course_id": "2",
                "moodle_section_id": "2",
                "lesson_id": lesson_id,
                "source": source,
                "doc_type": "markdown" if source == "canonical_md" else "video_transcript",
                "allowed_for_indexing": True,
                "visible_to_student": visible,
            },
        ),
        "score": score,
        "final_score": score,
        "context_relation": "same_lesson" if lesson_id else "same_section",
    }


def _mixed_evidence(current_lesson):
    return [
        _item(current_lesson, 1.30, "transcript"),
        _item(current_lesson, 1.20, "canonical_md"),
        _item(current_lesson, 1.10, "canonical_md"),
        _item("SEC2-R58", 1.00, "canonical_md", visible=False),
        _item("SEC2-R58", 0.98, "transcript"),
        _item("SEC2-R58", 0.96, "authoring_profile"),
        _item("", 0.90, "canonical_md"),
    ]


def _state(lesson_id):
    return {"course_id": "2", "moodle_section_id": "2", "current_lesson_id": lesson_id, "retrieval_scope": "lesson"}


def _lesson_ids(items):
    return [item["document"].metadata.get("lesson_id") or "" for item in items[:5]]


def test_sec2_r59_general_filtra_vecinos_si_hay_evidencia_suficiente():
    out = R._ordenar_para_respuesta_directa(
        _mixed_evidence("SEC2-R59"),
        "De que trata esta leccion?",
        _state("SEC2-R59"),
    )

    assert "SEC2-R58" not in _lesson_ids(out)
    assert _lesson_ids(out).count("SEC2-R59") >= 3


def test_sec2_r60_general_filtra_sec2_r58():
    out = R._ordenar_para_respuesta_directa(
        _mixed_evidence("SEC2-R60"),
        "Resumeme esta clase",
        _state("SEC2-R60"),
    )

    assert "SEC2-R58" not in _lesson_ids(out)
    assert _lesson_ids(out).count("SEC2-R60") >= 3


def test_sec2_r61_general_filtra_sec2_r58():
    out = R._ordenar_para_respuesta_directa(
        _mixed_evidence("SEC2-R61"),
        "Cual es el objetivo de esta leccion?",
        _state("SEC2-R61"),
    )

    assert "SEC2-R58" not in _lesson_ids(out)
    assert _lesson_ids(out).count("SEC2-R61") >= 3


def test_pregunta_transversal_explicita_puede_traer_otra_leccion():
    out = R._ordenar_para_respuesta_directa(
        _mixed_evidence("SEC2-R59"),
        "Como se relaciona gain staging con ruteo?",
        _state("SEC2-R59"),
    )

    assert "SEC2-R58" in _lesson_ids(out)


def test_visible_to_student_false_no_aparece_en_fuentes_publicas(monkeypatch):
    monkeypatch.setitem(sys.modules, "ingest", SimpleNamespace(
        _as_bool=lambda value, default=True: default if value is None else str(value).strip().lower() in {"1", "true", "yes", "si", "sí"}
    ))
    fuentes = [        {"source": "canonical_md", "lesson_id": "SEC2-R59", "visible_to_student": True},
        {"source": "canonical_md", "lesson_id": "SEC2-R59", "visible_to_student": False},
        {"source": "transcript", "lesson_id": "SEC2-R59", "visible_to_student": "false"},
    ]

    visibles = _fuentes_visibles_al_alumno(fuentes)

    assert visibles == [{"source": "canonical_md", "lesson_id": "SEC2-R59", "visible_to_student": True}]
