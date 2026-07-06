#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FASE 5 — Supersede el corpus canonical_md de una sección (default Sección 0 del
curso 2) que ha pasado a modo teacher_flow. Retira esos chunks del ÍNDICE Chroma;
NO borra los archivos .md (siguen como semilla/admin en disco).

Antes de borrar captura un MANIFIESTO de lo retirado (source_path, lesson_id, chunks)
para el reporte, y verifica el estado antes/después. Delete acotado por metadata
exacta (course_id + moodle_section_id + source='canonical_md'): no toca transcript,
teacher_context ni resource_file, ni otras secciones.

    docker exec tic-fastapi python /app/scripts/section0_supersede_canonical.py \
        --course 2 --section 2 --report /tmp/section0_report [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, "/app")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ingest  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", default="2")
    ap.add_argument("--section", default="2")
    ap.add_argument("--report", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    c, s = str(args.course), str(args.section)

    coll = ingest.get_vector_store()._collection
    where = {"$and": [{"course_id": c}, {"moodle_section_id": s}, {"source": "canonical_md"}]}
    got = coll.get(where=where, include=["metadatas"])
    metas = got.get("metadatas") or []

    by_source = Counter()
    by_lesson = Counter()
    for m in metas:
        by_source[str((m or {}).get("source_path") or "")] += 1
        by_lesson[str((m or {}).get("lesson_id") or "(section-level)")] += 1

    removed_manifest = [
        {"source_path": sp, "chunks": n, "reason": "superseded_by_teacher_flow"}
        for sp, n in sorted(by_source.items())
    ]

    out = {
        "course_id": c, "moodle_section_id": s, "dry_run": args.dry_run,
        "canonical_chunks_before": len(metas),
        "by_lesson": dict(by_lesson),
        "removed_manifest": removed_manifest,
    }

    if not args.dry_run:
        res = ingest.supersede_section_canonical(c, s)
        out["supersede_result"] = res
        out["canonical_chunks_after"] = ingest.count_section_canonical(c, s)

    if args.report:
        os.makedirs(args.report, exist_ok=True)
        json.dump(out, open(os.path.join(args.report, "FASE5_SUPERSEDE.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    print(json.dumps({k: out[k] for k in out if k not in ("removed_manifest", "by_lesson")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
