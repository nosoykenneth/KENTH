#!/usr/bin/env python3
"""Promoción de un corpus de AUTORÍA a la ubicación canónica INGEST-READY.

Transforma un árbol de autoría con frontmatter "humano"
    corpus/seccion_<slug>/**            (section_number pedagógico, recommended_scope, sin moodle_section_id)
al árbol canónico que lee el pipeline RAG, con frontmatter de SISTEMA
    tesis-rag/documentos/oficial/curso_<id>/seccion_<slug>/**   (moodle_section_id, scope, source, lesson_id)

Es el driver versionado (antes vivía sólo en el servidor como ingest_seccion0.py) que
aplica la política de flags declarada en INGEST_MANIFEST_SECCION_<N>.json. Sólo reescribe
METADATA/estructura: el CUERPO del markdown se copia verbatim (nunca se toca el contenido).

NO indexa nada, NO toca Chroma ni la BD. La ingesta real la hace el flujo de
docs/tic/PLAN_INGESTA_CORPUS.md (add_single_document / reindex acotado).

Política por `action` del manifest:
  - INDEX_lesson  -> allowed_for_indexing:true,  scope:lesson  (lesson_id = lesson_id_real)
  - INDEX_section -> allowed_for_indexing:true,  scope:section
  - EXCLUDE_never_index -> allowed_for_indexing:false (eval/QA/manifest/recursos_externos)
  - HOLD_pending_lesson_mapping -> allowed_for_indexing:false + retention_status:pending_lesson_mapping
      (lección sin lección real; retenida hasta que exista. Re-correr el script cuando el
       manifest tenga lesson_id_real la promueve automáticamente a indexable.)

Uso:
    python scripts/promote_seccion_corpus.py --manifest <ruta_json> [--dry-run|--commit]
    (por defecto: --dry-run)
"""
import argparse
import json
import os
import re
import shutil
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tesis-rag/


def slugify(text: str) -> str:
    """Slug ASCII estable desde un título (misma lógica que ingest._slugify)."""
    text = str(text or "").strip()
    text = re.sub(r"^\s*(secci[oó]n|tema)\s*\d+\s*[:.\-]\s*", "", text, flags=re.IGNORECASE)
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "_", norm).strip("_").lower()


def strip_frontmatter(text: str) -> str:
    """Devuelve el cuerpo del markdown sin el bloque frontmatter (--- ... ---)."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text.strip()


def _yaml_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    s = str(v)
    if '"' in s:  # los títulos del corpus no traen comillas dobles; si aparecieran, abortar limpio
        raise ValueError(f"valor con comilla doble no soportado por el frontmatter simple: {s!r}")
    return f'"{s}"'


def build_frontmatter(entry: dict, ctx: dict) -> str:
    """Construye el frontmatter de sistema para un archivo del manifest."""
    action = entry.get("action", "")
    lesson_id = (entry.get("lesson_id_real") or "").strip()
    has_lesson = bool(lesson_id)

    retention = None
    if action == "INDEX_lesson":
        allowed, scope = True, "lesson"
    elif action == "INDEX_section":
        allowed, scope = True, "section"
    elif action == "EXCLUDE_never_index":
        allowed = False
        scope = "lesson" if entry.get("recommended_scope") == "lesson" else "section"
    elif action == "HOLD_pending_lesson_mapping":
        allowed, scope, retention = False, "section", "pending_lesson_mapping"
    else:  # fallback defensivo: nunca indexar algo que no reconocemos
        allowed, scope, retention = False, "section", "unknown_action"

    fields = [
        ("course_id", ctx["course_id"]),
        ("moodle_section_id", ctx["moodle_section_id"]),
        ("section_id", ctx["moodle_section_id"]),
        ("section_number", ctx["section_number"]),
        ("section_slug", ctx["section_slug"]),
        ("section_title", ctx["section_title"]),
        ("lesson_id", lesson_id),
        ("lesson_number", entry.get("lesson_number", "")),
        ("lesson_title", entry.get("lesson_title", "")),
        ("source_type", entry.get("source_type", "")),
        ("scope", scope),
        ("source", "canonical_md"),
        ("content_type", "markdown"),
        ("visible_to_student", bool(entry.get("visible_to_student"))),
        ("allowed_for_indexing", bool(allowed)),
    ]
    if entry.get("internal_context"):
        fields.append(("internal_context", True))
    fields.append(("status", entry.get("status", "")))
    if retention:
        fields.append(("retention_status", retention))
    fields += [
        ("source_origin", "course"),
        ("corpus_version", ctx["corpus_version"]),
        ("ingestion_batch_id", ctx["batch_id"]),
        ("original_relative_path", entry["relative_path"]),
    ]
    lines = ["---"] + [f"{k}: {_yaml_value(v)}" for k, v in fields] + ["---"]
    return "\n".join(lines), allowed, scope, retention


# Companions operativos (no listados en el array `files`): se copian GATEADOS.
def _promote_plan(src, dest, ctx, do_write):
    with open(src, "r", encoding="utf-8") as f:
        body = f.read()
    fm = "\n".join([
        "---",
        f'course_id: "{ctx["course_id"]}"',
        f'moodle_section_id: "{ctx["moodle_section_id"]}"',
        f'section_number: "{ctx["section_number"]}"',
        f'section_title: "{ctx["section_title"]}"',
        'source_type: "operational_plan"',
        'scope: "section"',
        'visible_to_student: false',
        'allowed_for_indexing: false',
        'status: "excluded_operational"',
        'source_origin: "course"',
        "---",
    ])
    out = fm + "\n\n" + strip_frontmatter(body) + "\n" if body.lstrip().startswith("---") else fm + "\n\n" + body.strip() + "\n"
    if do_write:
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
    return "EXCLUDE(plan)"


def _promote_manifest_json(src, dest, do_write):
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):  # defensa en profundidad: gatear también por flag/status
        data["allowed_for_indexing"] = False
        data["visible_to_student"] = False
        data["status"] = "excluded_operational"
    if do_write:
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return "EXCLUDE(manifest.json)"


def _copy_verbatim(src, dest, do_write):
    # Guard: re-correr in-place (src_dir == dest_dir) haría copyfile(src, src) -> SameFileError.
    if do_write and os.path.abspath(src) != os.path.abspath(dest):
        shutil.copyfile(src, dest)
    return "COPY(non-safe-ext)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="ruta a INGEST_MANIFEST_SECCION_<N>.json")
    ap.add_argument("--dest-course", default=None, help="course_id destino (por defecto el del manifest)")
    ap.add_argument("--dest-dirname", default=None, help="nombre de carpeta destino de la sección")
    ap.add_argument("--commit", action="store_true", help="escribe en disco (por defecto dry-run)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    do_write = args.commit and not args.dry_run

    manifest_path = os.path.abspath(args.manifest)
    src_dir = os.path.dirname(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    course_id = args.dest_course or str(manifest["course_id"])
    ctx = {
        "course_id": course_id,
        "moodle_section_id": str(manifest["moodle_section_id"]),
        "section_number": str(manifest["section_number"]),
        "section_title": str(manifest["section_title"]),
        "section_slug": slugify(manifest["section_title"]),
        "corpus_version": str(manifest.get("corpus_version", "")),
        "batch_id": str(manifest.get("batch_id", "")),
    }
    dest_dirname = args.dest_dirname or os.path.basename(src_dir)
    dest_dir = os.path.join(BASE_DIR, "documentos", "oficial", f"curso_{course_id}", dest_dirname)

    print(f"[promote] manifest : {os.path.relpath(manifest_path, BASE_DIR)}")
    print(f"[promote] origen   : {os.path.relpath(src_dir, BASE_DIR)}")
    print(f"[promote] destino  : {os.path.relpath(dest_dir, BASE_DIR)}")
    print(f"[promote] modo     : {'COMMIT (escribe)' if do_write else 'DRY-RUN (no escribe)'}")
    print(f"[promote] sección  : id={ctx['moodle_section_id']} n={ctx['section_number']} slug={ctx['section_slug']}\n")

    counts = {"INDEX_lesson": 0, "INDEX_section": 0, "EXCLUDE_never_index": 0,
              "HOLD_pending_lesson_mapping": 0, "companion": 0, "indexable": 0, "excluded": 0}
    handled = set()

    for entry in manifest["files"]:
        rel = entry["relative_path"]
        src = os.path.join(src_dir, rel)
        dest = os.path.join(dest_dir, rel)
        if not os.path.exists(src):
            print(f"  [MISS] {rel} (no existe en origen)"); continue
        with open(src, "r", encoding="utf-8") as f:
            text = f.read()
        fm, allowed, scope, retention = build_frontmatter(entry, ctx)
        out = fm + "\n\n" + strip_frontmatter(text) + "\n"
        if do_write:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
        counts[entry["action"]] = counts.get(entry["action"], 0) + 1
        counts["indexable" if allowed else "excluded"] += 1
        handled.add(rel)
        tag = "IDX" if allowed else "---"
        rid = entry.get("lesson_id_real") or ""
        print(f"  [{tag}] {rel:<62} scope={scope:<7} lesson_id={rid or '-':<8} {entry['action']}")

    # Companions operativos (no en `files`).
    companions = {
        "PLAN_INGESTA_SECCION_0.md": lambda s, d: _promote_plan(s, d, ctx, do_write),
        "INGEST_MANIFEST_SECCION_0.json": lambda s, d: _promote_manifest_json(s, d, do_write),
        "INGEST_MANIFEST_SECCION_0.csv": lambda s, d: _copy_verbatim(s, d, do_write),
    }
    for name, fn in companions.items():
        src = os.path.join(src_dir, name)
        if not os.path.exists(src):
            continue
        dest = os.path.join(dest_dir, name)
        if do_write:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
        kind = fn(src, dest)
        counts["companion"] += 1
        handled.add(name)
        print(f"  [op-] {name:<62} {kind}")

    # ¿Quedó algún archivo del origen sin promover?
    for root, _dirs, files in os.walk(src_dir):
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), src_dir).replace("\\", "/")
            if rel not in handled:
                print(f"  [WARN] sin promover (no en manifest ni companions): {rel}")

    print("\n[promote] resumen:")
    print(f"  INDEX_lesson={counts['INDEX_lesson']}  INDEX_section={counts['INDEX_section']}  "
          f"EXCLUDE={counts['EXCLUDE_never_index']}  HOLD={counts['HOLD_pending_lesson_mapping']}  "
          f"companions={counts['companion']}")
    print(f"  -> indexables={counts['indexable']}  excluidos/retenidos={counts['excluded'] + counts['companion']}")
    if not do_write:
        print("\n[promote] DRY-RUN: no se escribió nada. Re-ejecuta con --commit para aplicar.")


if __name__ == "__main__":
    main()
