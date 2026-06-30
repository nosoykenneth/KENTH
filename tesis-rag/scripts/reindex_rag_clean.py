"""Reindex limpio de ChromaDB (arquitectura secciones/lecciones/bloques).

Pasos:
  1. Purga la colección Chroma y reconstruye el corpus canónico por sección
     (documentos/oficial/curso_<id>/seccion_NN/...) -> rebuild_all_documents().
  2. Re-indexa el conocimiento DB-driven de cada curso: descripciones de recursos
     binarios y transcripciones de lección (con su moodle_section_id).
  3. Ejecuta scripts/validate_rag_index.py y aborta con código != 0 si el índice
     viola la arquitectura (axis_id presente, chunk seccional sin sección, etc.).

DESTRUCTIVO: borra y reconstruye el vector store. Correr dentro de tic-fastapi
para que CHROMA_DIR y las credenciales Moodle estén disponibles.

Uso:
    python scripts/reindex_rag_clean.py                 # todos los cursos detectados
    python scripts/reindex_rag_clean.py --course 2      # solo un curso
    python scripts/reindex_rag_clean.py --skip-validate
"""
import argparse
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ingest import rebuild_all_documents, reindex_course_documents, _canonical_course_dirs  # noqa: E402


def _discover_courses():
    """Cursos con corpus canónico (documentos/oficial/curso_<id>/) + el default."""
    ids = set()
    for d in _canonical_course_dirs():
        name = os.path.basename(d)
        if name.startswith("curso_"):
            ids.add(name[len("curso_"):])
    ids.add(os.getenv("KENTH_DEFAULT_COURSE_ID", "2"))
    return sorted(i for i in ids if i)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", action="append", help="course_id (repetible). Por defecto: autodetectados.")
    ap.add_argument("--skip-validate", action="store_true")
    args = ap.parse_args()

    # Inicializa la conexión a Moodle/MariaDB ANTES del rebuild para que la
    # resolución de secciones (section_number/title/slug) funcione desde el
    # primer chunk (si no, using_moodle_db() arranca en False y no resuelve).
    try:
        from services import db_service
        db_service.init_db()
        print(f"[REINDEX] DB lista: using_moodle_db={db_service.using_moodle_db()}")
    except Exception as e:
        print(f"[REINDEX] aviso init_db: {e}")

    print("[REINDEX] (1/3) Rebuild limpio del corpus canónico (ChromaDB)...")
    result = rebuild_all_documents()
    print(f"[REINDEX] corpus: {result}")

    courses = args.course or _discover_courses()
    print(f"[REINDEX] (2/3) Re-indexando recursos + transcripciones DB-driven de: {courses}")
    for cid in courses:
        try:
            r = reindex_course_documents(cid)
            print(f"[REINDEX] curso {cid}: docs={r.get('processed')} recursos={r.get('resources_indexed')} "
                  f"transcripciones={r.get('transcripts_indexed')} skipped={r.get('skipped')}")
        except Exception as e:
            print(f"[REINDEX] curso {cid}: ERROR {e}")

    if args.skip_validate:
        print("[REINDEX] Validación omitida (--skip-validate).")
        return 0

    print("[REINDEX] (3/3) Validando índice...")
    validate_script = os.path.join(BASE_DIR, "scripts", "validate_rag_index.py")
    completed = subprocess.run([sys.executable, validate_script], cwd=BASE_DIR)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
