"""Fase 1 — Backfill de scope/is_global/index_status en local_tesisai_documents.

Uso:
    python -m scripts.phase1_backfill_scopes --dry-run   # solo reporta, no escribe
    python -m scripts.phase1_backfill_scopes             # aplica la migracion

Reglas (compatibles, no destructivas):
  - course_id="" y sin axis/lesson  -> scope='global', is_global=1 (legacy global).
  - course_id + axis_id + lesson_id  -> scope='lesson'.
  - course_id + axis_id (sin lesson) -> scope='axis'.
  - course_id (sin axis/lesson)      -> scope='course'.
Reporta filas ambiguas (lesson sin axis, o axis/lesson sin course y no global).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import db_service  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill de scope para documentos del tutor")
    parser.add_argument("--dry-run", action="store_true", help="No escribe; solo reporta el plan")
    args = parser.parse_args()

    result = db_service.backfill_document_scopes(dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result.get("ambiguous"):
        print(f"\n[ATENCION] {len(result['ambiguous'])} recurso(s) ambiguo(s) — revisar manualmente.")
        return 2
    print("\n[OK] Backfill completado." + (" (dry-run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
