"""Purga la estructura de lecciones del tutor (borrón y cuenta nueva).

Borra, para un curso (o para todos), las filas de:
  - lessons          (+ lesson_blocks, lesson_prompts, transcript_segments
                       y resource_lesson_links en cascada vía delete_lesson)
  - resource_lesson_links huérfanos (vínculos sin lección)

NO toca el contenido Moodle (videos H5P, secciones) ni el corpus RAG. Es solo
para limpiar lecciones/vínculos de prueba acumulados durante el desarrollo.

Uso:
    python scripts/purge_lessons.py --course 2     # solo el curso 2
    python scripts/purge_lessons.py --all          # TODOS los cursos
    python scripts/purge_lessons.py --course 2 --dry-run   # solo mostrar
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services import db_service  # noqa: E402


def _purge(course_id, dry_run: bool) -> None:
    lessons = db_service.list_lessons(course_id=course_id)
    links = db_service.list_resource_links(course_id)

    scope = f"curso {course_id}" if course_id else "TODOS los cursos"
    print(f"[{scope}] lecciones: {len(lessons)} | vínculos: {len(links)}")
    for lesson in lessons:
        print(f"  - lección {lesson.get('lesson_id')} · {lesson.get('title') or lesson.get('lesson_title') or ''}")
    for link in links:
        print(f"  - vínculo recurso {link.get('resource_id')} -> {link.get('lesson_id')}")

    if dry_run:
        print("\n(dry-run: no se borró nada)")
        return

    deleted_lessons = 0
    for lesson in lessons:
        lid = lesson.get("lesson_id")
        if lid and db_service.delete_lesson(lid):
            deleted_lessons += 1

    # Vínculos huérfanos cuya lección ya no existía (delete_lesson ya barre los
    # vínculos por lesson_id; esto cubre los que quedaron sin lección asociada).
    deleted_links = 0
    for link in db_service.list_resource_links(course_id):
        rid = link.get("resource_id")
        if rid and db_service.delete_resource_link(rid):
            deleted_links += 1

    print(f"\nPurgado: {deleted_lessons} lecciones, {deleted_links} vínculos huérfanos.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Purga lecciones/vínculos del tutor.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--course", help="course_id (numérico Moodle o firmado)")
    group.add_argument("--all", action="store_true", help="purga todos los cursos")
    parser.add_argument("--dry-run", action="store_true", help="solo listar, no borrar")
    args = parser.parse_args()

    course_id = None if args.all else args.course
    _purge(course_id, args.dry_run)


if __name__ == "__main__":
    main()
