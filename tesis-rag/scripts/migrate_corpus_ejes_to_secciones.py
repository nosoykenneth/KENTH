"""Migración del corpus canónico: taxonomía por EJES -> SECCIONES de Moodle.

Convierte el corpus viejo (documentos/oficial/ejes/contenido_canonico/
KENTH_EjeN_Contenido_Canonico.md, sin metadata y tageado mentalmente por "eje")
en la estructura canónica por sección que exige la arquitectura nueva:

    documentos/oficial/curso_<course_id>/seccion_<NN>_<slug>/contenido_canonico.md

Cada archivo migrado recibe frontmatter explícito con la sección Moodle real
(moodle_section_id, section_number, section_slug, section_title), de modo que el
ingest NO tenga que inferir nada por posición ni por nombre de eje: la sección
viaja en el documento. Esto elimina la dependencia conceptual de "eje".

El mapa Eje -> Sección se tomó del estado REAL de Moodle (curso 2) el
2026-06-30, consultando mdl_course_sections:

    section  sectionid  name
    0        1          BIENVENIDA                          (sin contenido canónico)
    1        2          SECCIÓN 0: El sistema de decisión    <- Eje 0
    2        3          SECCIÓN 1: Leer la señal             <- Eje 1
    3        4          SECCIÓN 2: Integridad de la señal    <- Eje 2
    4        5          SECCIÓN 3: Identidad espectral       <- Eje 3
    5        20         SECCIÓN 4: Energía y movimiento      <- Eje 4
    6        19         SECCIÓN 5: Dimensión espacial        <- Eje 5
    7        18         SECCIÓN 6: Integración global        <- Eje 6
    8        17         SECCIÓN 7: Traducción y entrega      <- Eje 7

NOTA de decisión: existían DOS fuentes canónicas por eje 3/5/6/7
(KENTH_EjeN_Contenido_Canonico.md y eje_N_*/01_contenido_canonico.md) con el
mismo contenido -> doble indexado. Se conserva SOLO el KENTH_* como única fuente
canónica por sección. El resto del árbol viejo (paquetes_limpios, 02_paquete_limpio,
JSON vacíos, manifests) ya estaba excluido del índice y se purga aparte.

Uso (desde tesis-rag/):
    python scripts/migrate_corpus_ejes_to_secciones.py            # ejecuta
    python scripts/migrate_corpus_ejes_to_secciones.py --dry-run  # solo reporta
"""
from __future__ import annotations

import argparse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFICIAL = os.path.join(BASE_DIR, "documentos", "oficial")
SRC_CANONICO = os.path.join(OFICIAL, "ejes", "contenido_canonico")

COURSE_ID = "2"
DEST_ROOT = os.path.join(OFICIAL, f"curso_{COURSE_ID}")

# eje_number -> sección Moodle real (ver docstring). Fuente de verdad: MariaDB.
SECTION_MAP = {
    0: {"moodle_section_id": "2",  "section_number": 1, "section_title": "SECCIÓN 0: El sistema de decisión", "section_slug": "el_sistema_de_decision"},
    1: {"moodle_section_id": "3",  "section_number": 2, "section_title": "SECCIÓN 1: Leer la señal",          "section_slug": "leer_la_senal"},
    2: {"moodle_section_id": "4",  "section_number": 3, "section_title": "SECCIÓN 2: Integridad de la señal",  "section_slug": "integridad_de_la_senal"},
    3: {"moodle_section_id": "5",  "section_number": 4, "section_title": "SECCIÓN 3: Identidad espectral",     "section_slug": "identidad_espectral"},
    4: {"moodle_section_id": "20", "section_number": 5, "section_title": "SECCIÓN 4: Energía y movimiento",    "section_slug": "energia_y_movimiento"},
    5: {"moodle_section_id": "19", "section_number": 6, "section_title": "SECCIÓN 5: Dimensión espacial",      "section_slug": "dimension_espacial"},
    6: {"moodle_section_id": "18", "section_number": 7, "section_title": "SECCIÓN 6: Integración global",      "section_slug": "integracion_global"},
    7: {"moodle_section_id": "17", "section_number": 8, "section_title": "SECCIÓN 7: Traducción y entrega",    "section_slug": "traduccion_y_entrega"},
}


def _frontmatter(sec: dict, eje_number: int) -> str:
    return (
        "---\n"
        f'course_id: "{COURSE_ID}"\n'
        f'moodle_section_id: "{sec["moodle_section_id"]}"\n'
        f'section_id: "{sec["moodle_section_id"]}"\n'
        f'section_number: "{sec["section_number"]}"\n'
        f'section_slug: "{sec["section_slug"]}"\n'
        f'section_title: "{sec["section_title"]}"\n'
        'resource_type: "lesson_content"\n'
        'content_type: "markdown"\n'
        'layer: "canonical"\n'
        'scope: "section"\n'
        'source: "canonical_md"\n'
        'source_origin: "course"\n'
        'status: "ready_for_indexing"\n'
        'visible_to_student: "true"\n'
        'allowed_for_indexing: "true"\n'
        'version: "v1"\n'
        f'legacy_axis: "Eje {eje_number}"  # solo trazabilidad de migración; NO usar como fuente\n'
        "---\n\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    report = {"course_id": COURSE_ID, "dest_root": os.path.relpath(DEST_ROOT, BASE_DIR), "migrated": [], "missing": []}

    if not args.dry_run:
        os.makedirs(DEST_ROOT, exist_ok=True)

    for eje in range(8):
        sec = SECTION_MAP[eje]
        src = os.path.join(SRC_CANONICO, f"KENTH_Eje{eje}_Contenido_Canonico.md")
        if not os.path.exists(src):
            report["missing"].append(os.path.relpath(src, BASE_DIR))
            print(f"[WARN] no existe fuente: {src}")
            continue
        with open(src, "r", encoding="utf-8") as f:
            body = f.read()
        # quitar frontmatter previo si lo hubiera (no lo tienen, defensivo)
        if body.startswith("---"):
            parts = body.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].lstrip("\n")

        dest_dir = os.path.join(DEST_ROOT, f"seccion_{sec['section_number']:02d}_{sec['section_slug']}")
        dest = os.path.join(dest_dir, "contenido_canonico.md")
        content = _frontmatter(sec, eje) + body

        entry = {
            "eje": f"Eje {eje}",
            "src": os.path.relpath(src, BASE_DIR),
            "dest": os.path.relpath(dest, BASE_DIR),
            "moodle_section_id": sec["moodle_section_id"],
            "section_number": sec["section_number"],
            "section_title": sec["section_title"],
            "bytes": len(body),
        }
        report["migrated"].append(entry)
        print(f"[MIGRATE] Eje {eje} -> seccion {sec['section_number']:02d} (moodle_section_id={sec['moodle_section_id']}) :: {entry['dest']}")

        if not args.dry_run:
            os.makedirs(dest_dir, exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)

    if not args.dry_run:
        with open(os.path.join(DEST_ROOT, "_seccion_map.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] {len(report['migrated'])} secciones migradas a {report['dest_root']}")
        print(f"[OK] log de decisión: {os.path.relpath(os.path.join(DEST_ROOT, '_seccion_map.json'), BASE_DIR)}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
