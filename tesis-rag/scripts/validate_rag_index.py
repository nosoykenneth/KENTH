"""Validación del índice RAG (arquitectura secciones/lecciones/bloques).

Lee ChromaDB directamente (no requiere Ollama) e informa:
  - total de chunks
  - chunks por sección (moodle_section_id + título)
  - chunks por lección
  - chunks globales
  - chunks sin course_id
  - chunks seccionales sin section_id (VIOLACIÓN)
  - presencia de axis_id legacy en el índice (VIOLACIÓN)
  - duplicados por source_hash
  - distribución de scopes
  - ejemplos de metadata

Emite un reporte JSON y Markdown en scripts/_out/ y devuelve exit code != 0 si
hay violaciones duras (axis_id presente, chunk seccional sin sección, chunk sin
course_id que no sea global, o scope 'axis').

Uso (desde tesis-rag/, idealmente dentro del contenedor tic-fastapi):
    python scripts/validate_rag_index.py
    python scripts/validate_rag_index.py --json-only
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

CHROMA_DIR = os.getenv("CHROMA_DIR") or os.path.join(BASE_DIR, "bd_vectorial")
OUT_DIR = os.path.join(BASE_DIR, "scripts", "_out")

SECTIONAL_SCOPES = {"section", "lesson", "block"}


def _bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    return str(v).strip().lower() in {"1", "true", "yes", "si", "sí"}


def _load_metadatas():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    cols = client.list_collections()
    if not cols:
        return "", []
    name = cols[0].name
    coll = client.get_collection(name)
    n = coll.count()
    got = coll.get(limit=n, include=["metadatas"]) if n else {"metadatas": []}
    return name, (got.get("metadatas") or [])


def validate():
    collection, metas = _load_metadatas()
    total = len(metas)

    by_section = collections.Counter()
    by_lesson = collections.Counter()
    by_scope = collections.Counter()
    by_source = collections.Counter()
    by_layer = collections.Counter()
    # source_hash -> set de source_path distintos (duplicado REAL = mismo contenido
    # en >1 archivo; los múltiples chunks de un mismo doc comparten hash y NO cuentan).
    hash_to_paths = collections.defaultdict(set)

    violations = {
        "with_axis_id": [],
        "scope_axis": [],
        "sectional_without_section": [],
        "non_global_without_course": [],
    }

    globales = 0
    for i, m in enumerate(metas):
        m = m or {}
        scope = str(m.get("scope") or "").strip().lower()
        course_id = str(m.get("course_id") or "").strip()
        section_id = str(m.get("moodle_section_id") or m.get("section_id") or "").strip()
        lesson_id = str(m.get("lesson_id") or "").strip()
        is_global = _bool(m.get("is_global")) or scope == "global"

        by_scope[scope or "(vacío)"] += 1
        by_source[str(m.get("source") or "(vacío)")] += 1
        by_layer[str(m.get("layer") or "(vacío)")] += 1
        sh = str(m.get("source_hash") or "")
        if sh:
            hash_to_paths[sh].add(str(m.get("source_path") or ""))

        if is_global:
            globales += 1
        else:
            label = f"{section_id} · {m.get('section_title') or ''}".strip(" ·") or "(sin sección)"
            by_section[label] += 1
            if lesson_id:
                by_lesson[lesson_id] += 1

        # --- violaciones ---
        if str(m.get("axis_id") or "").strip():
            violations["with_axis_id"].append(i)
        if scope == "axis":
            violations["scope_axis"].append(i)
        if scope in SECTIONAL_SCOPES and not section_id and not lesson_id:
            violations["sectional_without_section"].append(i)
        if not is_global and not course_id:
            violations["non_global_without_course"].append(i)

    # Duplicado real: un mismo source_hash presente en >1 source_path distinto.
    duplicados = {h: sorted(paths) for h, paths in hash_to_paths.items() if len(paths) > 1}

    ejemplos = []
    for m in metas[:3]:
        ejemplos.append({k: m.get(k) for k in (
            "course_id", "moodle_section_id", "section_number", "section_title",
            "section_slug", "lesson_id", "block_id", "scope", "layer", "source",
            "resource_type", "content_type", "source_hash",
        )})

    hard_fail = (
        len(violations["with_axis_id"])
        + len(violations["scope_axis"])
        + len(violations["sectional_without_section"])
        + len(violations["non_global_without_course"])
    )

    return {
        "ok": hard_fail == 0,
        "collection": collection,
        "total_chunks": total,
        "globales": globales,
        "chunks_por_seccion": dict(by_section),
        "chunks_por_leccion": dict(by_lesson),
        "distribucion_scopes": dict(by_scope),
        "distribucion_source": dict(by_source),
        "distribucion_layer": dict(by_layer),
        "duplicados_source_hash": {"grupos": len(duplicados), "detalle": dict(list(duplicados.items())[:20])},
        "violaciones": {k: len(v) for k, v in violations.items()},
        "violaciones_indices": {k: v[:20] for k, v in violations.items()},
        "ejemplos_metadata": ejemplos,
    }


def _to_markdown(rep: dict) -> str:
    L = ["# Validación del índice RAG", ""]
    L.append(f"- **Estado**: {'✅ OK' if rep['ok'] else '❌ VIOLACIONES'}")
    L.append(f"- **Colección**: `{rep['collection']}`")
    L.append(f"- **Total chunks**: {rep['total_chunks']}")
    L.append(f"- **Globales**: {rep['globales']}")
    L.append("")
    L.append("## Chunks por sección")
    for k, v in sorted(rep["chunks_por_seccion"].items()):
        L.append(f"- {k}: {v}")
    L.append("")
    L.append("## Chunks por lección")
    for k, v in sorted(rep["chunks_por_leccion"].items()):
        L.append(f"- {k}: {v}")
    L.append("")
    L.append("## Distribución de scopes")
    for k, v in sorted(rep["distribucion_scopes"].items()):
        L.append(f"- {k}: {v}")
    L.append("")
    L.append("## Violaciones (deben ser 0)")
    for k, v in rep["violaciones"].items():
        L.append(f"- {k}: {v}")
    L.append("")
    L.append(f"## Duplicados por source_hash: {rep['duplicados_source_hash']['grupos']} grupos")
    L.append("")
    L.append("## Ejemplos de metadata")
    L.append("```json")
    L.append(json.dumps(rep["ejemplos_metadata"], ensure_ascii=False, indent=2))
    L.append("```")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args()

    rep = validate()
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "rag_index_report.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    md = _to_markdown(rep)
    with open(os.path.join(OUT_DIR, "rag_index_report.md"), "w", encoding="utf-8") as f:
        f.write(md)

    if args.json_only:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(md)
        print(f"\n[VALIDATE] Reporte: {os.path.relpath(OUT_DIR, BASE_DIR)}/rag_index_report.(json|md)")

    if not rep["ok"]:
        print("\n[VALIDATE] ❌ Índice con violaciones de arquitectura (ver 'violaciones').")
        return 1
    print("\n[VALIDATE] ✅ Índice coherente con la arquitectura por secciones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
