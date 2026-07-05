#!/usr/bin/env python
"""Driver del FLUJO DOCENTE para la Sección 0 (curso 2).

Idempotente. Ejecuta, por lección presente en la BD, la cadena del flujo docente:
  transcripción aprobada -> índice de transcripción -> contexto aprobado del
  editor (teacher_approved_context) -> índice incremental -> auditoría.

NO hace rebuild global. NO borra archivos. NO inventa lecciones: si una lección de
la Sección 0 no existe en la BD (p. ej. sólo vive en el servidor), la reporta y
sigue. Patrón delete-then-add por lección para todo lo que indexa.

Uso (desde tesis-rag/):
  python scripts/teacher_flow_section0.py                 # DRY-RUN (no muta nada)
  python scripts/teacher_flow_section0.py --apply         # aplica (con backup Chroma)
  python scripts/teacher_flow_section0.py --apply --supersede-canonical
                                                          # además borra chunks
                                                          # canonical_md de Sec 0
  python scripts/teacher_flow_section0.py --apply --no-backup
  python scripts/teacher_flow_section0.py --report DIR    # dónde escribir la auditoría

Seguridad: en DRY-RUN sólo lee; con --apply hace primero un backup de bd_vectorial
(salvo --no-backup) y luego muta BD + Chroma acotado al curso 2 / Sección 0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

# Permite ejecutar como `python scripts/teacher_flow_section0.py` desde tesis-rag/.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

COURSE_ID = "2"
SECTION_MOODLE_ID = "2"          # moodle_section_id de "SECCIÓN 0" (section_number=1)
SECTION_HUMAN = "Sección 0 — El sistema de decisión"
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripciones_seccion_00")

# Mapeo canónico de la Sección 0. lesson_id SEC2-R{cmid}; cmid = 54 + número.
# El título humano es la fuente de verdad de presentación (los .txt lo autodeclaran
# en su primera línea, que usamos para verificar que no haya cruces de lección).
SECTION0 = [
    {"num": "0.1", "lesson_id": "SEC2-R55", "cmid": 55,
     "title": "Mezclar es decidir: el ciclo de trabajo",
     "file": "leccion_0_1_transcripcion.txt", "declares": "primera lección"},
    {"num": "0.2", "lesson_id": "SEC2-R56", "cmid": 56,
     "title": "Tu oído miente: percepción y nivel de escucha",
     "file": "leccion_0_2_transcripcion.txt", "declares": "segunda lección"},
    {"num": "0.3", "lesson_id": "SEC2-R57", "cmid": 57,
     "title": "Monitores y auriculares: trabajar con lo que tienes",
     "file": "leccion_0_3_transcripcion.txt", "declares": "tercera lección"},
    {"num": "0.4", "lesson_id": "SEC2-R58", "cmid": 58,
     "title": "Anatomía universal del mixer: ruteo",
     "file": "leccion_0_4_transcripcion.txt", "declares": "cuarta lección"},
    {"num": "0.5", "lesson_id": "SEC2-R59", "cmid": 59,
     "title": "Gain Staging: el cimiento de toda la cadena",
     "file": "leccion_0_5_transcripcion.txt", "declares": "quinta lección"},
    {"num": "0.6", "lesson_id": "SEC2-R60", "cmid": 60,
     "title": "Nativos vs emulaciones analógicas: la matriz de decisión",
     "file": "leccion_0_6_transcripcion.txt", "declares": "sexta lección"},
    {"num": "0.7", "lesson_id": "SEC2-R61", "cmid": 61,
     "title": "Checklist de sesión lista para mezclar",
     "file": "leccion_0_7_transcripcion.txt", "declares": "séptima"},
]

_TS_LINE = re.compile(
    r"^\[(?P<start>\d{1,2}(?::\d{2})*\.\d{1,3})\s*-->\s*(?P<end>\d{1,2}(?::\d{2})*\.\d{1,3})\]\s*(?P<text>.*)$"
)


def _ts_to_seconds(ts: str) -> float:
    """'MM:SS.mmm' o 'HH:MM:SS.mmm' -> segundos (float)."""
    parts = ts.strip().split(":")
    secs = float(parts[-1])
    for i, p in enumerate(reversed(parts[:-1])):
        secs += int(p) * (60 ** (i + 1))
    return round(secs, 3)


def parse_transcript_file(path: str) -> list:
    """Parsea un .txt VTT-like a segmentos [{seq,start_time,end_time,text,speaker}].

    Preserva timestamps (segmentación operativa). Normaliza saltos de línea y
    espacios; NO resume ni inventa. UTF-8.
    """
    segments = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = _TS_LINE.match(line)
            if not m:
                # Línea de continuación sin timestamp: se anexa al segmento previo.
                if segments:
                    segments[-1]["text"] = (segments[-1]["text"] + " " + line).strip()
                continue
            text = re.sub(r"\s+", " ", m.group("text")).strip()
            if not text:
                continue
            segments.append({
                "seq": len(segments),
                "start_time": _ts_to_seconds(m.group("start")),
                "end_time": _ts_to_seconds(m.group("end")),
                "text": text,
                "speaker": "",
            })
    return segments


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _backup_chroma(log: list) -> str:
    import config
    src = config.CHROMA_DIR
    if not os.path.isdir(src):
        log.append(f"[backup] Chroma dir inexistente ({src}); nada que respaldar.")
        return ""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = f"{src}_backup_teacherflow_{stamp}"
    shutil.copytree(src, dst)
    log.append(f"[backup] Chroma respaldado en {dst}")
    return dst


def _chroma_audit(course_id: str, section_id: str) -> dict:
    import ingest
    coll = ingest.get_vector_store()._collection
    res = coll.get(where={"$and": [{"course_id": course_id}, {"moodle_section_id": section_id}]},
                   include=["metadatas"])
    metas = res.get("metadatas") or []
    from collections import Counter
    by_source = Counter((m.get("source") or "") for m in metas)
    by_lesson = Counter((m.get("lesson_id") or "") for m in metas)
    by_type = Counter((m.get("source_type") or "") for m in metas)
    by_doctype = Counter((m.get("doc_type") or "") for m in metas)
    return {
        "total_section_chunks": len(metas),
        "by_source": dict(by_source),
        "by_lesson_id": dict(by_lesson),
        "by_source_type": dict(by_type),
        "by_doc_type": dict(by_doctype),
    }


def run(apply: bool, backup: bool, supersede_canonical: bool, report_dir: str) -> dict:
    from services import db_service, teacher_context
    import ingest

    db_service.init_db()
    log: list = []
    per_lesson: list = []

    log.append(f"apply={apply} backup={backup} supersede_canonical={supersede_canonical}")
    log.append(f"course={COURSE_ID} section_moodle_id={SECTION_MOODLE_ID} ({SECTION_HUMAN})")

    pre_audit = _chroma_audit(COURSE_ID, SECTION_MOODLE_ID)
    log.append(f"[pre] Chroma Sección 0: {pre_audit['total_section_chunks']} chunks "
               f"lessons={pre_audit['by_lesson_id']}")

    if apply and backup:
        _backup_chroma(log)

    for spec in SECTION0:
        lid = spec["lesson_id"]
        entry = {"num": spec["num"], "lesson_id": lid, "cmid": spec["cmid"],
                 "expected_title": spec["title"]}
        lesson = db_service.get_lesson(lid, COURSE_ID)
        if not lesson:
            entry["status"] = "missing_in_db"
            entry["action"] = "SKIP (no existe localmente; poblar en el servidor)"
            per_lesson.append(entry)
            log.append(f"[{spec['num']} {lid}] AUSENTE en BD -> se omite (server-only).")
            continue

        db_title = (lesson.get("title") or lesson.get("lesson_title") or "").strip()
        entry["db_title"] = db_title

        # Verificación de alineación de título (Fase 1): el .txt autodeclara su
        # número de lección; comprobamos que coincide con lo esperado (anti-cruce).
        fpath = os.path.join(TRANSCRIPT_DIR, spec["file"])
        if not os.path.exists(fpath):
            entry["status"] = "transcript_file_missing"
            per_lesson.append(entry)
            log.append(f"[{spec['num']} {lid}] falta archivo {spec['file']}.")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            head = " ".join(f.readline() for _ in range(3)).lower()
        declares_ok = spec["declares"].lower() in head
        entry["declares_ok"] = declares_ok
        if not declares_ok:
            entry["status"] = "title_alignment_warning"
            log.append(f"[{spec['num']} {lid}] AVISO: el archivo no autodeclara "
                       f"'{spec['declares']}'; revisar posible cruce antes de indexar.")

        segments = parse_transcript_file(fpath)
        entry["segments"] = len(segments)
        entry["duration_s"] = segments[-1]["end_time"] if segments else 0

        if not apply:
            entry["status"] = "dry_run_ok"
            per_lesson.append(entry)
            log.append(f"[{spec['num']} {lid}] DRY-RUN: {len(segments)} segs listos "
                       f"(dur ~{entry['duration_s']}s).")
            continue

        # 1) Transcripción aprobada (reemplazo completo).
        db_service.replace_transcript(lid, segments)
        db_service.merge_lesson_metadata(lid, COURSE_ID, {
            "transcript_status": config_approved_state(),
            "transcript_source": "imported_approved",
            "transcript_approved_at": _now_iso(),
            "transcript_segments_count": len(segments),
        })
        # 2) Índice de transcripción (delete-then-add por lección).
        tr = ingest.index_lesson_transcript(
            COURSE_ID, lid, segments,
            moodle_section_id=SECTION_MOODLE_ID,
            lesson_title=(db_title or spec["title"]),
        )
        entry["transcript_chunks"] = tr.get("chunks", 0)
        # 3) Contexto aprobado del editor + índice incremental.
        pub = teacher_context.publish_lesson_teacher_context(
            lid, COURSE_ID, user_id="teacher_flow_driver",
            lesson_title_override=(db_title or spec["title"]),
        )
        entry["teacher_context_chunks"] = pub.get("chunks", 0)
        entry["teacher_context_index_status"] = pub.get("index_status")
        entry["status"] = "applied"
        per_lesson.append(entry)
        log.append(f"[{spec['num']} {lid}] APLICADO: transcript={entry['transcript_chunks']} "
                   f"teacher_context={entry['teacher_context_chunks']} "
                   f"({pub.get('index_status')}).")

    # Fase 7 opcional: superseder el corpus markdown canónico de la Sección 0.
    if apply and supersede_canonical:
        try:
            coll = ingest.get_vector_store()._collection
            before = _chroma_audit(COURSE_ID, SECTION_MOODLE_ID)
            coll.delete(where={"$and": [
                {"course_id": COURSE_ID},
                {"moodle_section_id": SECTION_MOODLE_ID},
                {"source": "canonical_md"},
            ]})
            after = _chroma_audit(COURSE_ID, SECTION_MOODLE_ID)
            removed = before["by_source"].get("canonical_md", 0) - after["by_source"].get("canonical_md", 0)
            log.append(f"[supersede] canonical_md Sección 0 borrados: {removed}")
        except Exception as e:
            log.append(f"[supersede] error: {e}")

    post_audit = _chroma_audit(COURSE_ID, SECTION_MOODLE_ID)
    log.append(f"[post] Chroma Sección 0: {post_audit['total_section_chunks']} chunks "
               f"lessons={post_audit['by_lesson_id']} types={post_audit['by_source_type']}")

    summary = {
        "generated_at": _now_iso(),
        "course_id": COURSE_ID,
        "section_moodle_id": SECTION_MOODLE_ID,
        "section_human": SECTION_HUMAN,
        "apply": apply,
        "lessons": per_lesson,
        "pre_audit": pre_audit,
        "post_audit": post_audit,
        "log": log,
    }

    if report_dir:
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, "teacher_flow_run.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    return summary


def config_approved_state() -> str:
    import config
    return config.TRANSCRIPT_STATUS_APPROVED


def main():
    ap = argparse.ArgumentParser(description="Flujo docente RAG — Sección 0 (curso 2)")
    ap.add_argument("--apply", action="store_true", help="aplica cambios (default: dry-run)")
    ap.add_argument("--no-backup", action="store_true", help="no respaldar Chroma antes de aplicar")
    ap.add_argument("--supersede-canonical", action="store_true",
                    help="borra chunks canonical_md de la Sección 0 (reemplazados por el flujo docente)")
    ap.add_argument("--report", default="", help="directorio donde escribir la auditoría JSON")
    args = ap.parse_args()

    summary = run(apply=args.apply, backup=not args.no_backup,
                  supersede_canonical=args.supersede_canonical, report_dir=args.report)
    print(json.dumps({k: summary[k] for k in ("apply", "pre_audit", "post_audit")},
                     ensure_ascii=False, indent=2))
    for line in summary["log"]:
        print(line)
    print("\nLecciones:")
    for l in summary["lessons"]:
        print(f"  {l['num']} {l['lesson_id']}: {l.get('status')} "
              f"segs={l.get('segments','-')} tr_chunks={l.get('transcript_chunks','-')} "
              f"tc_chunks={l.get('teacher_context_chunks','-')}")


if __name__ == "__main__":
    main()
