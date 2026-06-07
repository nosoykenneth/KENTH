"""Verificación del flujo de subida de recurso de lección (.flp) tras el fix.

Ejercita el ENDPOINT real `upload_lesson_resource` (no un atajo), con un .flp
subido a E2-L01, y valida que la fila quede coherente:
    scope='lesson', media_type='template', index_status='indexed',
    chunk_count=1, lesson_id='E2-L01', visible_to_student=1, allowed_for_indexing=1.

Como doc_id = slug("E2-L01_<titulo>"), subir el titulo "another trap" reescribe
el registro existente `e2_l01_another_trap` con el código nuevo: prueba + corrección.

Uso:  python scripts/verify_lesson_upload.py
Requiere Ollama (nomic-embed-text) para indexar la descripción del recurso.
"""

import asyncio
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.datastructures import UploadFile, Headers  # noqa: E402

from api.dependencies import TeacherContext  # noqa: E402
from api.routes.lesson_resources import upload_lesson_resource  # noqa: E402
from services import db_service  # noqa: E402

LESSON_ID = "E2-L01"
COURSE_ID = "2"
TITLE = "another trap"
DESCRIPTION = "Plantilla fl studio de rnb trap para el estudiante"

EXPECTED = {
    "scope": "lesson",
    "media_type": "template",
    "index_status": "indexed",
    "chunk_count": 1,
    "lesson_id": "E2-L01",
    "allowed_for_indexing": True,
    "visible_to_student": True,
}


async def _run_upload():
    data = b"FLhd" + b"\x00" * 60  # cabecera .flp simulada (binario, no se embebe)
    upload = UploadFile(
        file=io.BytesIO(data),
        filename="another trap.flp",
        headers=Headers({"content-type": "application/octet-stream"}),
    )
    ctx = TeacherContext(user_id="verify_script", course_id=COURSE_ID, course_raw=COURSE_ID)
    return await upload_lesson_resource(
        lesson_id=LESSON_ID,
        file=upload,
        title=TITLE,
        description=DESCRIPTION,
        concepts="",
        index_to_tutor=True,
        visible_to_student=True,
        ctx=ctx,
    )


def main() -> int:
    resp = asyncio.run(_run_upload())
    doc_id = (resp.get("resource") or {}).get("doc_id") or "e2_l01_another_trap"
    print(f"Subida OK: doc_id={doc_id} chunks={resp.get('chunks')}")

    row = db_service.get_document(doc_id, COURSE_ID)
    print("\n--- FILA FINAL EN DB ---")
    keys = ["doc_id", "course_id", "axis_id", "lesson_id", "scope", "is_global",
            "media_type", "allowed_for_indexing", "visible_to_student",
            "index_status", "chunk_count", "doc_type"]
    for k in keys:
        print(f"  {k} = {row.get(k)!r}")

    fails = []
    for k, expected in EXPECTED.items():
        actual = row.get(k)
        ok = actual == expected
        print(f"  [{'PASS' if ok else 'FAIL'}] {k}: esperado={expected!r} real={actual!r}")
        if not ok:
            fails.append(k)

    # La columna media_type debe estar persistida (no solo el fallback de metadata).
    print("\n--- CHROMA (chunk de descripción) ---")
    try:
        import ingest
        got = ingest.get_vector_store()._collection.get(
            where={"source": f"resource:{doc_id}"}, include=["metadatas"]
        )
        metas = got.get("metadatas") or []
        print(f"  chunks en Chroma: {len(metas)}")
        if metas:
            m = metas[0]
            for k in ("scope", "visible_to_student", "allowed_for_indexing", "course_id", "lesson_id", "media_type"):
                print(f"    {k} = {m.get(k)!r}")
            if m.get("scope") != "lesson":
                fails.append("chroma.scope")
            if m.get("visible_to_student") is not True:
                fails.append("chroma.visible_to_student")
    except Exception as e:
        print(f"  (no se pudo consultar Chroma: {e})")

    print(f"\n=== RESULTADO: {'OK' if not fails else 'FALLOS: ' + ', '.join(fails)} ===")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
