"""Pruebas del resolver de capabilities (services/moodle_permissions.py).

Cubre la normalización del contrato de la WS, los accesores y el camino de
"WS no configurada" (token vacío) que debe devolver None para que los guards
caigan al fallback por rol.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import moodle_permissions as mp


def test_normalize_coacciona_a_bool_y_rol():
    perms = mp._normalize({
        "puede_ver_curso": 1,
        "es_profesor": True,
        "puede_administrar_curso": 0,
        "puede_revisar": "1",
        "es_tecnico_rag": False,
        "es_invitado": 0,
        "rol_efectivo": "profesor",
    })
    assert perms["puede_ver_curso"] is True
    assert perms["es_profesor"] is True
    assert perms["puede_administrar_curso"] is False
    assert perms["puede_revisar"] is True
    assert perms["es_tecnico_rag"] is False
    assert perms["es_invitado"] is False
    assert perms["rol_efectivo"] == "profesor"


def test_normalize_faltantes_son_false():
    perms = mp._normalize({})
    for k in ("puede_ver_curso", "es_profesor", "puede_administrar_curso",
              "puede_revisar", "es_tecnico_rag", "es_invitado"):
        assert perms[k] is False
    assert perms["rol_efectivo"] == ""


def test_accesores():
    p = {"es_profesor": True, "puede_administrar_curso": False, "es_tecnico_rag": False,
         "puede_ver_curso": True, "puede_revisar": True}
    assert mp.can_edit_pedagogy(p) is True
    assert mp.can_admin_course(p) is False
    assert mp.is_rag_admin(p) is False
    assert mp.can_view_course(p) is True
    assert mp.can_review(p) is True
    # None (WS no disponible) -> todo False, sin excepción.
    assert mp.can_edit_pedagogy(None) is False


def test_resolve_sin_token_devuelve_none(monkeypatch):
    # Sin MOODLE_WS_TOKEN la WS no está configurada -> None (usar fallback).
    monkeypatch.setattr(mp, "MOODLE_WS_TOKEN", "")
    assert mp.resolve_course_permissions("42", "2") is None


def test_resolve_sin_userid_o_curso_devuelve_none(monkeypatch):
    monkeypatch.setattr(mp, "MOODLE_WS_TOKEN", "tok")
    monkeypatch.setattr(mp, "MOODLE_WS_BASE", "http://moodle/webservice/rest/server.php")
    assert mp.resolve_course_permissions("", "2") is None
    assert mp.resolve_course_permissions("42", "") is None
