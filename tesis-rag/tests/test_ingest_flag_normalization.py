"""Regresión: normalización robusta de flags booleanos en la política de ingesta.

El frontmatter markdown se parsea a STRINGS ('false', '0', 'no'), por eso la
compuerta antes comparaba `allowed_for_indexing is False` y dejaba pasar prompts
de evaluación / QA / manifiestos / recursos externos cuando el flag venía como
string. Aquí se fija el contrato:
  - `_as_bool` interpreta true/false, "true"/"false", "1"/"0", 1/0, yes/no, on/off, null.
  - `es_documento_aprobado_para_indexar` RECHAZA `allowed_for_indexing` falsy aunque
    llegue como string, incluso para archivos con nombre operativo/evaluación.
"""

import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ingest
from ingest import _as_bool, es_documento_aprobado_para_indexar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_as_bool_representaciones_verdaderas():
    for v in (True, "true", "True", "TRUE", " true ", "1", 1, 1.0, "yes", "si", "sí", "on", "y", "t"):
        assert _as_bool(v) is True, repr(v)


def test_as_bool_representaciones_falsas():
    for v in (False, "false", "False", "FALSE", " false ", "0", 0, 0.0, "no", "off", "null", "none", "nil", "", "n", "f"):
        assert _as_bool(v) is False, repr(v)


def test_as_bool_none_usa_default():
    assert _as_bool(None) is False
    assert _as_bool(None, default=True) is True


def test_as_bool_desconocido_cae_al_default():
    assert _as_bool("quizas", default=True) is True
    assert _as_bool("quizas", default=False) is False


@pytest.fixture
def canonical_course(monkeypatch):
    """Registra un curso canónico temporal (nombre limpio bajo tesis-rag/ para que
    el relpath no dispare patrones prohibidos tmp/temp/log)."""
    root = os.path.join(BASE_DIR, "gatefixtures_run")
    shutil.rmtree(root, ignore_errors=True)
    course_dir = os.path.join(root, "curso_2")
    os.makedirs(course_dir)
    monkeypatch.setattr(ingest, "CANONICAL_COURSE_DIRS", tuple(ingest.CANONICAL_COURSE_DIRS) + (course_dir,))
    monkeypatch.setattr(ingest, "ALLOWED_PUBLIC_DIRS", tuple(ingest.ALLOWED_PUBLIC_DIRS) + (course_dir,))
    try:
        yield course_dir
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _write(course_dir, name, allowed_literal):
    p = os.path.join(course_dir, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(
            '---\n'
            'course_id: "2"\n'
            'moodle_section_id: "2"\n'
            'section_number: "1"\n'
            'visible_to_student: "true"\n'
            f'allowed_for_indexing: {allowed_literal}\n'
            '---\n\n'
            '# Contenido de prueba\n\nTexto academico limpio para el test.\n'
        )
    return p


@pytest.mark.parametrize("allowed_literal", ['"false"', 'false', '"False"', '"0"', '"no"', '"off"', '"null"'])
def test_gate_rechaza_allowed_string_falsy(canonical_course, allowed_literal):
    path = _write(canonical_course, "01_contenido_canonico.md", allowed_literal)
    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)
    assert not aprobado, (allowed_literal, razones)
    assert any("allowed_for_indexing" in r for r in razones), razones


@pytest.mark.parametrize("allowed_literal", ['"true"', 'true', '"1"', '"yes"'])
def test_gate_aprueba_allowed_string_truthy(canonical_course, allowed_literal):
    path = _write(canonical_course, "01_contenido_canonico.md", allowed_literal)
    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)
    assert aprobado, razones


@pytest.mark.parametrize("name", [
    "10_prompt_evaluacion.md",
    "00_QA_CORPUS_SECCION_0.md",
    "00_manifest_indexacion_seccion.md",
    "00_recursos_externos_sugeridos.md",
])
def test_gate_operativos_y_evaluacion_no_indexan_aunque_string(canonical_course, name):
    # Simula el flag como STRING 'false' (tal cual lo entrega el frontmatter md).
    path = _write(canonical_course, name, '"false"')
    aprobado, razones, _ = es_documento_aprobado_para_indexar(path, explicar=True)
    assert not aprobado, (name, razones)
    assert any("allowed_for_indexing" in r for r in razones), razones


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
