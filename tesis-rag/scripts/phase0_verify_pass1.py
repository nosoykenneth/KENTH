"""Fase 0 / Pass 1 — Verifica que la elevacion de literales a constantes en
graph.py y vision.py es FIEL al original (git HEAD).

Extrae por AST todos los literales de string de la version en HEAD y comprueba
que el valor de cada constante nueva existe verbatim en ese conjunto. Un typo en
la copia => no es substring => falla. Asi el baseline capturado tras Pass 1
refleja el comportamiento original real.

Uso: python scripts/phase0_verify_pass1.py
"""

import ast
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent import graph as agent_graph
from services.agent import vision as agent_vision


def _head_source(rel_path: str) -> str:
    out = subprocess.run(
        ["git", "show", f"HEAD:{rel_path}"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        raise RuntimeError(f"git show fallo para {rel_path}: {out.stderr}")
    return out.stdout


def _string_literals(src: str):
    """Devuelve todos los literales de string del modulo, incluidas las partes
    Constant dentro de f-strings (JoinedStr)."""
    tree = ast.parse(src)
    blob_parts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            blob_parts.append(node.value)
    return "".join(blob_parts)


CHECKS = {
    "tesis-rag/services/agent/graph.py": {
        "RAG_SYSTEM_PROMPT": agent_graph.RAG_SYSTEM_PROMPT,
        "VISION_RAG_INTRO": agent_graph.VISION_RAG_INTRO,
        "VISION_RAG_RULES": agent_graph.VISION_RAG_RULES,
        "LOST_INTRO": agent_graph.LOST_INTRO,
        "LOST_RULES": agent_graph.LOST_RULES,
        "WEB_QUERY_SUFFIX": agent_graph.WEB_QUERY_SUFFIX,
        "WEB_INTRO": agent_graph.WEB_INTRO,
        "WEB_RULES": agent_graph.WEB_RULES,
        "GUARD_REPLY": agent_graph.GUARD_REPLY,
        "GREETINGS.thanks": agent_graph.GREETINGS["thanks"],
        "GREETINGS.ok": agent_graph.GREETINGS["ok"],
        "GREETINGS.bye": agent_graph.GREETINGS["bye"],
        "GREETINGS.default": agent_graph.GREETINGS["default"],
    },
    "tesis-rag/services/agent/vision.py": {
        "VISION_CLASSIFY_PROMPT": agent_vision.VISION_CLASSIFY_PROMPT,
        "VISION_CAPTION_PROMPT": agent_vision.VISION_CAPTION_PROMPT,
        # El prompt sin-evidencia incluye un sufijo dinamico f"Pregunta...". La
        # constante guarda solo la parte estatica, asi que comprobamos esa.
        "VISION_NO_EVIDENCE_PROMPT": agent_vision.VISION_NO_EVIDENCE_PROMPT,
    },
}


# Constantes cuyo codigo fuente se anadio en el working tree DESPUES de HEAD
# (cambios sin commitear pre-sesion). No se pueden verificar contra HEAD; su
# fidelidad se apoya en la lectura del working tree pre-Pass-1.
POSTDATES_HEAD = {"VISION_CAPTION_PROMPT"}


def main():
    ok = True
    for rel_path, consts in CHECKS.items():
        blob = _string_literals(_head_source(rel_path))
        for name, value in consts.items():
            if value in blob:
                print(f"[OK  ] {rel_path}::{name} (len={len(value)}) verbatim en HEAD")
            elif name in POSTDATES_HEAD:
                print(f"[SKIP] {rel_path}::{name} (len={len(value)}) postdata HEAD; no verificable por git")
            else:
                ok = False
                print(f"[FAIL] {rel_path}::{name} (len={len(value)}) NO coincide con HEAD")
    print("\nPASS 1 FIDELITY:", "OK" if ok else "FALLO")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
