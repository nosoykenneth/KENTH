#!/usr/bin/env python3
"""Mapea DÓNDE se lee cada campo de metadata pedagógica en el backend del tutor.

Responde la pregunta 1 del contrato de metadata ("¿dónde se LEE cada campo?") y
detecta campos *muertos*: declarados en los modelos/persistencia pero nunca
consumidos por la lógica (routing/retrieval/context/verification/prompts). Es una
heurística de texto: confirma a mano los casos límite, pero acelera mucho la
auditoría.

Agnóstico al curso y al repo: la lista de campos y las rutas son configurables.
No contiene credenciales, rutas personales ni datos sensibles.

Uso:
    python scan_metadata_usage.py --root ../../tesis-rag
    python scan_metadata_usage.py --root /path/al/backend --fields tutor_focus concepts
    python scan_metadata_usage.py --root . --json > usage.json

Clasifica cada archivo .py donde aparece un campo en un "bucket":
    model    -> modelos/esquemas (declaración)            [models/, schemas]
    persist  -> persistencia/carga                         [db_service, *_service load]
    inject   -> render/inyección al prompt                 [context_service, prompts, render]
    logic    -> decisión: routing/retrieval/verification   [agent/, routing, retrieval]
    author   -> autoría/escritura                          [authoring]
    test     -> pruebas/scripts/scratch                    [tests/, scripts/, scratch/]
    other    -> el resto

Un campo que solo aparece en {model, persist, test} y NUNCA en {inject, logic}
es sospechoso de estar MUERTO (poblado pero sin efecto en el comportamiento).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# En consolas Windows cp1252, imprimir acentos/¿ rompe con UnicodeEncodeError.
# Forzamos UTF-8 en stdout/stderr cuando se pueda (Py3.7+).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

# Campos del contrato de metadata pedagógica (ver references/metadata-contract.md).
DEFAULT_FIELDS = [
    "learning_goal",
    "learning_goals",
    "expected_action",
    "prerequisites",
    "delegated_to_tutor",
    "attribution_constraints",
    "proactive_message",
    "suggested_prompts",
    "lesson_blocks",
    "tutor_focus",
    "probable_questions",
    "preguntas_probables",
    "concepts",
    "interaction_mode",
]

DEFAULT_EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    "bd_vectorial", "bd_chat", "bd_vectorial_backup",
}


def classify(path: str) -> str:
    p = path.replace("\\", "/").lower()
    if "/tests/" in p or "/scratch/" in p or "/scripts/" in p or os.path.basename(p).startswith("test_"):
        return "test"
    if "authoring" in p:
        return "author"
    if "/models/" in p or "schemas" in os.path.basename(p):
        return "model"
    if "db_service" in p or "transcription_service" in p or "moodle_ws" in p:
        return "persist"
    if "context_service" in p or "prompts" in os.path.basename(p) or "render" in p:
        return "inject"
    if "/agent/" in p or "routing" in p or "retrieval" in p or "verification" in p or "graph" in p:
        return "logic"
    if "lesson_service" in p or "section_service" in p:
        return "persist"
    return "other"


def iter_py_files(root: str, exclude_dirs: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in exclude_dirs and not d.startswith("bd_vectorial_backup")
        ]
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def scan(root: str, fields: list[str], exclude_dirs: set[str]) -> dict:
    patterns = {f: re.compile(r"\b" + re.escape(f) + r"\b") for f in fields}
    result = {
        f: {"total": 0, "buckets": {}, "files": []}
        for f in fields
    }
    for path in iter_py_files(root, exclude_dirs):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        bucket = classify(path)
        rel = os.path.relpath(path, root)
        for f, pat in patterns.items():
            hits = len(pat.findall(text))
            if hits:
                result[f]["total"] += hits
                result[f]["buckets"][bucket] = result[f]["buckets"].get(bucket, 0) + hits
                result[f]["files"].append({"file": rel, "bucket": bucket, "hits": hits})
    return result


def is_dead(entry: dict) -> bool:
    """Muerto = aparece en algún lado pero NUNCA en inject ni logic."""
    if entry["total"] == 0:
        return False
    effective = entry["buckets"].get("inject", 0) + entry["buckets"].get("logic", 0)
    return effective == 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="Raíz del backend a escanear (p. ej. ../../tesis-rag).")
    ap.add_argument("--fields", nargs="*", default=None, help="Campos a buscar (por defecto, el contrato completo).")
    ap.add_argument("--exclude", nargs="*", default=None, help="Directorios extra a excluir.")
    ap.add_argument("--json", action="store_true", help="Salida JSON cruda.")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"ERROR: no existe el directorio {root}", file=sys.stderr)
        return 2

    fields = args.fields or DEFAULT_FIELDS
    exclude = set(DEFAULT_EXCLUDE_DIRS)
    if args.exclude:
        exclude.update(args.exclude)

    result = scan(root, fields, exclude)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print(f"# Uso de metadata en {root}\n")
    dead = []
    for f in fields:
        e = result[f]
        if e["total"] == 0:
            print(f"  {f:28s}  AUSENTE (0 ocurrencias)")
            continue
        buckets = ", ".join(f"{b}:{n}" for b, n in sorted(e["buckets"].items()))
        flag = "  <-- POSIBLE CAMPO MUERTO (sin inject/logic)" if is_dead(e) else ""
        print(f"  {f:28s}  total={e['total']:3d}  [{buckets}]{flag}")
        if is_dead(e):
            dead.append(f)

    print("\n## Lectura efectiva (inject + logic) por campo")
    for f in fields:
        e = result[f]
        eff = e["buckets"].get("inject", 0) + e["buckets"].get("logic", 0)
        logic = e["buckets"].get("logic", 0)
        note = ""
        if e["total"] and logic == 0 and eff > 0:
            note = "  (solo inyección: ¿gobierna routing/gates? probablemente NO)"
        print(f"  {f:28s}  efectiva={eff:3d}  logic={logic:3d}{note}")

    if dead:
        print("\n## Campos sospechosos de estar MUERTOS:")
        for f in dead:
            print(f"  - {f}")
        print("  (Verifica a mano: pueden leerse vía **kwargs/getattr dinámico.)")
    else:
        print("\n## Sin campos muertos evidentes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
