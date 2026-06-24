"""
Configuracion global de pytest para la suite del backend del tutor (tesis-rag).

Objetivo (MUST FIX de la auditoria): la suite debe correr VERDE en UN solo
comando y en CUALQUIER maquina, sin depender de que exista una BD de Moodle ni
de un estado global compartido entre tests.

Decisiones:
- Se fuerza el backend SQLite en una BD TEMPORAL por test (TESISAI_FORCE_SQLITE).
  Asi las pruebas NUNCA escriben en la MariaDB real de Moodle (en la maquina del
  dev existe config.php, y sin esto los tests pegaban a la BD real) y cada test
  arranca con una BD limpia.
- Se resetean los globales de `db_service` (`_INITIALIZED`, `_BACKEND`) antes y
  despues de cada test. Esto elimina la FUGA DE ESTADO GLOBAL que hacia fallar de
  forma intermitente los tests de contrato (TypeError de pymysql cuando `_BACKEND`
  quedaba en "moodle" de un test anterior).

Estas pruebas son unitarias/de contrato de la LOGICA del tutor; la integracion
real contra Moodle/Ollama se valida aparte (ver evaluation/). Forzar SQLite aqui
es la practica estandar para tests deterministas, no oculta ningun fallo real.
"""

import os
import sys

# Permite `import services...`, `import api...`, `import models...` al ejecutar
# pytest desde el directorio tesis-rag/ (no hay paquete instalable).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest


@pytest.fixture(autouse=True)
def _isolated_sqlite_db(tmp_path, monkeypatch):
    """Aisla la persistencia: SQLite temporal por test + globales reseteados."""
    monkeypatch.setenv("TESISAI_FORCE_SQLITE", "1")
    monkeypatch.setenv("TESISAI_ALLOW_SQLITE_FALLBACK", "1")

    # Import diferido: el modulo puede no estar cargado aun al colectar.
    from services import db_service

    monkeypatch.setattr(db_service, "SQLITE_DB", tmp_path / "tesisai_test.sqlite")
    db_service._INITIALIZED = False
    db_service._BACKEND = None
    try:
        yield
    finally:
        db_service._INITIALIZED = False
        db_service._BACKEND = None
