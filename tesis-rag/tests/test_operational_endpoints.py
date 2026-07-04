"""Endpoints operativos de cierre TIC: /health, /moodle/me y el contrato de
tolerancia de course_id en las lecturas.

Cubre los bugs de la auditoría TIC (AUDITORIA_TIC_READYNESS.md §11):
- B1: `/moodle/me` -> 500 por KeyError de logging (clave `message` en `extra`
      colisiona con LogRecord). Regresión fijada aquí: un error WS se convierte en
      MoodleWSError manejable, no en KeyError.
- B2: no existía `/health`.
- B3: `/sections/lessons/all` -> 422 opaco por falta de course_id.

Todas las pruebas son deterministas y sin red (se mockean cliente WS, Chroma,
Ollama y BD). Ejecutar desde tesis-rag/:  python -m pytest tests/test_operational_endpoints.py
"""
import asyncio
import json
import logging
import os
import sys

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import dependencies
from api.dependencies import get_current_user_id
from api.routes import health as health_mod
from api.routes import moodle as moodle_mod
from services import moodle_ws_client as mwc
from services.moodle_ws_client import MoodleWSError, get_moodle_ws_client


# ---------------------------------------------------------------------------
# B1 — el logging del error WS NO puede lanzar KeyError (regresión /moodle/me 500)
# ---------------------------------------------------------------------------

class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _FakeHttpxClient:
    def __init__(self, payload):
        self._payload = payload
        self.is_closed = False

    async def post(self, url, data=None):
        return _FakeResp(self._payload)

    async def aclose(self):
        self.is_closed = True


def test_moodle_ws_exception_payload_lanza_moodleerror_no_keyerror(monkeypatch):
    """El caso exacto del bug: la WS responde 200 con `exception`+`message`.

    Antes del fix, `logger.error(..., extra={"message": ...})` lanzaba
    KeyError("Attempt to overwrite 'message'") y el error subía como 500.
    Ahora debe subir como MoodleWSError (que el endpoint traduce a error controlado).
    """
    # Asegura que el nivel ERROR está habilitado, para que makeRecord se ejecute
    # (es ahí donde el bug original lanzaba KeyError).
    logging.getLogger("services.moodle_ws_client").setLevel(logging.ERROR)

    client = mwc.MoodleWSClient(base_url="http://moodle/webservice/rest/server.php", token="tok")
    fake = _FakeHttpxClient({
        "exception": "webservice_access_exception",
        "errorcode": "accessexception",
        "message": "Control de acceso: no autorizado para ver este usuario.",
    })

    async def _fake_get_client():
        return fake

    monkeypatch.setattr(client, "_get_client", _fake_get_client)

    with pytest.raises(MoodleWSError):
        asyncio.run(client.call("core_user_get_users_by_field", field="id", values=["42"]))


def test_moodle_ws_ok_payload_devuelve_datos(monkeypatch):
    client = mwc.MoodleWSClient(base_url="http://moodle/ws", token="tok")
    fake = _FakeHttpxClient([{"id": 42, "fullname": "Ada"}])

    async def _fake_get_client():
        return fake

    monkeypatch.setattr(client, "_get_client", _fake_get_client)
    out = asyncio.run(client.get_user_by_id(42))
    assert out == {"id": 42, "fullname": "Ada"}


# ---------------------------------------------------------------------------
# B2 — /health: forma correcta, cálculo de estado y SIN secretos
# ---------------------------------------------------------------------------

def _health_app():
    app = FastAPI()
    app.include_router(health_mod.router)
    return app


def _patch_health(monkeypatch, db="ok", chroma=("ok", 24), ollama=("ok", {"chat": True, "embedding": True}), ws="ok"):
    monkeypatch.setattr(health_mod, "_check_moodle_db", lambda: db)
    monkeypatch.setattr(health_mod, "_check_chroma", lambda: chroma)
    monkeypatch.setattr(health_mod, "_check_ollama", lambda: ollama)

    async def _ws():
        return ws

    monkeypatch.setattr(health_mod, "_check_moodle_ws", _ws)


def test_health_ok(monkeypatch):
    _patch_health(monkeypatch)
    r = TestClient(_health_app()).get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    for key in ("fastapi", "moodle_db", "moodle_ws", "chroma", "ollama", "models"):
        assert key in body
    assert body["models"] == {"chat": health_mod.TEXT_MODEL, "embedding": health_mod.EMBED_MODEL}


def test_health_degraded_por_ws_o_sqlite(monkeypatch):
    _patch_health(monkeypatch, db="sqlite", ws="unavailable")
    body = TestClient(_health_app()).get("/health").json()
    assert body["status"] == "degraded"


def test_health_error_si_falla_critico(monkeypatch):
    _patch_health(monkeypatch, chroma=("error", None))
    body = TestClient(_health_app()).get("/health").json()
    assert body["status"] == "error"


def test_health_no_expone_secretos(monkeypatch):
    # Planta secretos en el entorno; el body de /health NUNCA debe contenerlos.
    monkeypatch.setenv("MOODLE_WS_TOKEN", "SECRET-WS-TOKEN-XYZ")
    monkeypatch.setenv("MOODLE_DBPASS", "SECRET-DB-PASS-XYZ")
    _patch_health(monkeypatch)
    raw = TestClient(_health_app()).get("/health").text
    assert "SECRET-WS-TOKEN-XYZ" not in raw
    assert "SECRET-DB-PASS-XYZ" not in raw
    lower = raw.lower()
    for forbidden in ("wstoken", "password", "dbpass", "authorization", "bearer"):
        assert forbidden not in lower


# ---------------------------------------------------------------------------
# B1 (extremo endpoint) — /moodle/me responde 200 degradado, nunca 500
# ---------------------------------------------------------------------------

class _FakeWSClient:
    configured = True

    def __init__(self, raise_err=False, profile=None):
        self._raise = raise_err
        self._profile = profile

    async def get_user_by_id(self, uid):
        if self._raise:
            raise MoodleWSError("acceso denegado")
        return self._profile


def _me_app(fake_client, perms):
    app = FastAPI()
    app.include_router(moodle_mod.router)
    app.dependency_overrides[get_current_user_id] = lambda: "42"
    app.dependency_overrides[get_moodle_ws_client] = lambda: fake_client
    return app


def test_me_degrada_cuando_ws_falla(monkeypatch):
    monkeypatch.setattr(moodle_mod, "resolve_course_permissions", lambda uid, cid: None)
    app = _me_app(_FakeWSClient(raise_err=True), None)
    r = TestClient(app).get("/moodle/me")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "42"
    assert body["profile"] is None
    assert body["moodle_ws"] == "error"


def test_me_ok_con_perfil_y_capabilities(monkeypatch):
    perms = {"puede_ver_curso": True, "es_profesor": True, "rol_efectivo": "profesor"}
    monkeypatch.setattr(moodle_mod, "resolve_course_permissions", lambda uid, cid: perms)
    profile = {"id": 42, "fullname": "Ada Lovelace", "email": "ada@x.io", "secretfield": "nope"}
    app = _me_app(_FakeWSClient(profile=profile), perms)
    r = TestClient(app).get("/moodle/me")
    assert r.status_code == 200
    body = r.json()
    assert body["moodle_ws"] == "ok"
    assert body["profile"]["fullname"] == "Ada Lovelace"
    # Lista blanca: campos no reconocidos NO se filtran.
    assert "secretfield" not in body["profile"]
    assert body["capabilities"]["es_profesor"] is True


# ---------------------------------------------------------------------------
# B3 y seguridad — course_id por query como fallback NO debilita autorización
# ---------------------------------------------------------------------------

def _force_moodle(monkeypatch, user_id="u1", perms=None):
    monkeypatch.setattr(dependencies, "get_current_user_id", lambda *a, **k: user_id)
    monkeypatch.setattr(dependencies, "using_moodle_db", lambda: True)
    monkeypatch.setattr(dependencies, "resolve_course_numeric", lambda cid: "2")
    monkeypatch.setattr(dependencies, "resolve_course_permissions", lambda uid, cid: perms)


def test_course_view_query_fallback_sigue_validando_capability(monkeypatch):
    # Curso llega SOLO por query (no header) y el usuario NO puede ver -> 403.
    _force_moodle(monkeypatch, perms={"puede_ver_curso": False})
    with pytest.raises(HTTPException) as exc:
        dependencies.require_course_view(authorization="Bearer x", x_course_id=None, course_id="2", x_dev_user_id=None)
    assert exc.value.status_code == 403


def test_course_view_query_fallback_permite_si_tiene_acceso(monkeypatch):
    _force_moodle(monkeypatch, perms={"puede_ver_curso": True})
    ctx = dependencies.require_course_view(authorization="Bearer x", x_course_id=None, course_id="2", x_dev_user_id=None)
    assert ctx.course_id == "2"


def test_course_view_sin_curso_devuelve_400_claro(monkeypatch):
    _force_moodle(monkeypatch, perms={"puede_ver_curso": True})
    with pytest.raises(HTTPException) as exc:
        dependencies.require_course_view(authorization="Bearer x", x_course_id=None, course_id=None, x_dev_user_id=None)
    assert exc.value.status_code == 400
    assert "course" in exc.value.detail.lower()


def test_me_exige_token_cuando_moodle_activo(monkeypatch):
    # Seguridad no debilitada: con Moodle activo, X-User-Id NO sustituye al token.
    monkeypatch.setattr(dependencies, "using_moodle_db", lambda: True)
    monkeypatch.setattr(dependencies, "get_user_id_from_token", lambda t: None)
    with pytest.raises(HTTPException) as exc:
        dependencies.get_current_user_id(authorization=None, x_dev_user_id="99")
    assert exc.value.status_code == 401
