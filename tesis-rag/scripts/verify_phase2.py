"""Fase 2 — Verificación: recurso de eje + resource_type + scope/visibilidad.

Ejercita los ENDPOINTS reales (no atajos) contra el curso 2 / eje "Eje 2" /
lección E2-L01. Crea recursos de prueba con prefijo 'p2test_' y los limpia al final
(excepto el .flp de lección, que reescribe e2_l01_another_trap con datos correctos).

Requiere Ollama (nomic-embed-text). Uso:  python scripts/verify_phase2.py
"""

import asyncio
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.datastructures import UploadFile, Headers  # noqa: E402
from fastapi import HTTPException  # noqa: E402

from api.dependencies import TeacherContext  # noqa: E402
from api.routes import lesson_resources as LR  # noqa: E402
from api.routes import course_documents as CD  # noqa: E402
from services import db_service  # noqa: E402
import ingest  # noqa: E402

COURSE = "2"
AXIS = "Eje 2"
LESSON = "E2-L01"
CTX = TeacherContext(user_id="p2test", course_id=COURSE, course_raw=COURSE)

_passes, _fails = [], []
_created = []  # (kind, doc_id)


def check(name, cond, detail=""):
    (_passes if cond else _fails).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" -> {detail}" if detail and not cond else ""))


def upfile(name, data):
    return UploadFile(file=io.BytesIO(data), filename=name,
                      headers=Headers({"content-type": "application/octet-stream"}))


def chroma_meta(source):
    got = ingest.get_vector_store()._collection.get(where={"source": source}, include=["metadatas"])
    return got.get("metadatas") or []


def chroma_count(where):
    try:
        return len(ingest.get_vector_store()._collection.get(where=where, include=[]).get("ids", []))
    except Exception:
        return -1


async def scenario_axis_document():
    print("\n== A) Recurso de EJE (documento .md) ==")
    md = ("# Apunte general de filtros del eje 2\n\n"
          "Este documento describe filtros pasa-altos y pasa-bajos, frecuencia de corte, "
          "pendiente y factor Q a nivel general del eje. " * 12).encode("utf-8")
    resp = await LR.upload_axis_resource(
        axis_id=AXIS, file=upfile("apunte general de filtros.md", md),
        title="Apunte general de filtros", description="Apunte de filtros del eje",
        concepts="filtros, eq", index_to_tutor=True, visible_to_student=None,
        resource_type="", ctx=CTX,
    )
    doc_id = resp["resource"]["doc_id"]
    _created.append(("axis", doc_id))
    row = db_service.get_document(doc_id, COURSE)
    check("axis doc scope='axis'", row.get("scope") == "axis", f"scope={row.get('scope')}")
    check("axis doc lesson_id vacío", not row.get("lesson_id"), f"lesson_id={row.get('lesson_id')!r}")
    check("axis doc axis_id correcto", row.get("axis_id") == AXIS, f"axis_id={row.get('axis_id')!r}")
    check("axis doc index_status='indexed'", row.get("index_status") == "indexed", f"{row.get('index_status')}")
    check("axis doc chunk_count>0", (row.get("chunk_count") or 0) > 0, f"{row.get('chunk_count')}")
    check("axis doc resource_type='theory'", row.get("resource_type") == "theory", f"{row.get('resource_type')}")


async def scenario_axis_template():
    print("\n== B) Recurso de EJE (plantilla .flp) ==")
    # B1: sin descripción + indexar => 400.
    raised = False
    try:
        await LR.upload_axis_resource(
            axis_id=AXIS, file=upfile("plantilla base.flp", b"FLhd" + b"\x00" * 40),
            title="plantilla base", description="", concepts="",
            index_to_tutor=True, visible_to_student=None, resource_type="", ctx=CTX,
        )
    except HTTPException:
        raised = True
    check("axis template sin descripción => 400", raised)

    # B2: con descripción => indexa solo descripción (1 chunk).
    resp = await LR.upload_axis_resource(
        axis_id=AXIS, file=upfile("plantilla base.flp", b"FLhd" + b"\x00" * 40),
        title="plantilla base", description="Plantilla base de mezcla del eje 2",
        concepts="mezcla", index_to_tutor=True, visible_to_student=True, resource_type="", ctx=CTX,
    )
    doc_id = resp["resource"]["doc_id"]
    _created.append(("axis", doc_id))
    row = db_service.get_document(doc_id, COURSE)
    check("axis tpl scope='axis'", row.get("scope") == "axis", f"{row.get('scope')}")
    check("axis tpl media_type='template'", row.get("media_type") == "template", f"{row.get('media_type')}")
    check("axis tpl resource_type='daw_template'", row.get("resource_type") == "daw_template", f"{row.get('resource_type')}")
    check("axis tpl chunk_count=1", row.get("chunk_count") == 1, f"{row.get('chunk_count')}")
    check("axis tpl index_status='indexed'", row.get("index_status") == "indexed", f"{row.get('index_status')}")


async def scenario_lesson_flp():
    print("\n== C) Recurso de LECCIÓN (.flp) + agrupación estructurada ==")
    resp = await LR.upload_lesson_resource(
        lesson_id=LESSON, file=upfile("another trap.flp", b"FLhd" + b"\x00" * 40),
        title="another trap", description="Plantilla fl studio de rnb trap para el estudiante",
        concepts="", index_to_tutor=True, visible_to_student=True, resource_type="", ctx=CTX,
    )
    doc_id = resp["resource"]["doc_id"]
    row = db_service.get_document(doc_id, COURSE)
    check("lesson flp scope='lesson'", row.get("scope") == "lesson", f"{row.get('scope')}")
    check("lesson flp lesson_id correcto", row.get("lesson_id") == LESSON, f"{row.get('lesson_id')}")

    structured = CD.structured_course_documents(ctx=CTX)
    ax = structured["axes"].get(AXIS, {})
    axis_ids = {r["doc_id"] for r in ax.get("axis_resources", [])}
    lesson_ids = {r["doc_id"] for r in ax.get("lessons", {}).get(LESSON, [])}
    check("lesson flp NO está en recursos del eje", doc_id not in axis_ids)
    check("lesson flp SÍ bajo lessons['E2-L01']", doc_id in lesson_ids)


async def scenario_global():
    print("\n== D) Recurso GLOBAL ==")
    md = ("# Glosario universal de audio\n\n"
          "Definiciones generales de dB, headroom, true peak y LUFS válidas para todos los cursos. " * 12).encode("utf-8")
    resp = await CD.upload_course_document(
        file=upfile("glosario universal audio.md", md), title="Glosario universal de audio",
        axis_id="", doc_layer="canonico", attribution_required=False, ownership="kenth_academy",
        notes="", scope="global", description="Glosario universal", concepts="db, lufs",
        resource_type="", ctx=CTX,
    )
    doc_id = resp["document"]["doc_id"]
    _created.append(("global", doc_id))
    row = db_service.get_document(doc_id, "")
    check("global is_global=1", bool(row.get("is_global")))
    check("global scope='global'", row.get("scope") == "global", f"{row.get('scope')}")
    check("global course_id vacío", not row.get("course_id"), f"{row.get('course_id')!r}")
    return doc_id


async def scenario_not_indexed():
    print("\n== F) allowed_for_indexing=false => pending, sin chunk ==")
    resp = await LR.upload_lesson_resource(
        lesson_id=LESSON, file=upfile("solo descarga.flp", b"FLhd" + b"\x00" * 40),
        title="p2test solo descarga", description="archivo solo de descarga",
        concepts="", index_to_tutor=False, visible_to_student=True, resource_type="", ctx=CTX,
    )
    doc_id = resp["resource"]["doc_id"]
    _created.append(("lesson", doc_id))
    row = db_service.get_document(doc_id, COURSE)
    check("no-index index_status='pending'", row.get("index_status") == "pending", f"{row.get('index_status')}")
    check("no-index sin chunks en Chroma", len(chroma_meta(f"resource:{doc_id}")) == 0)
    return doc_id


def scenario_reindex_and_meta(global_doc_id):
    print("\n== E) Reindex curso conserva scopes + G) metadata Chroma ==")
    before_axis = chroma_count({"$and": [{"course_id": COURSE}, {"scope": "axis"}]})
    before_lesson = chroma_count({"$and": [{"course_id": COURSE}, {"scope": "lesson"}]})
    before_tr = chroma_count({"$and": [{"course_id": COURSE}, {"doc_type": "video_transcript"}]})
    global_before = chroma_count({"is_global": True})

    res = ingest.reindex_course_documents(COURSE)
    print(f"    reindex: processed={res.get('processed')} resources={res.get('resources_indexed')} "
          f"transcripts={res.get('transcripts_indexed')}")

    after_axis = chroma_count({"$and": [{"course_id": COURSE}, {"scope": "axis"}]})
    after_lesson = chroma_count({"$and": [{"course_id": COURSE}, {"scope": "lesson"}]})
    after_tr = chroma_count({"$and": [{"course_id": COURSE}, {"doc_type": "video_transcript"}]})
    global_after = chroma_count({"is_global": True})

    check("reindex conserva chunks scope='axis'", after_axis >= before_axis and after_axis > 0,
          f"{before_axis}->{after_axis}")
    check("reindex conserva chunks scope='lesson'", after_lesson >= 1, f"{before_lesson}->{after_lesson}")
    check("reindex conserva transcripciones", after_tr >= before_tr and after_tr > 0, f"{before_tr}->{after_tr}")
    check("reindex NO toca globales", global_after >= global_before and global_after > 0,
          f"{global_before}->{global_after}")
    check("sin chunks allowed_for_indexing=false",
          chroma_count({"$and": [{"course_id": COURSE}, {"allowed_for_indexing": False}]}) == 0)

    # G) metadata de un chunk de recurso de eje (template).
    tpl = [c for c in _created if c[0] == "axis"]
    if tpl:
        metas = chroma_meta(f"resource:{tpl[-1][1]}")
        if metas:
            m = metas[0]
            for field in ("scope", "resource_type", "media_type", "visible_to_student",
                          "allowed_for_indexing", "course_id", "axis_id"):
                check(f"chroma chunk tiene {field}", field in m, f"falta {field}")
            check("chroma chunk scope='axis'", m.get("scope") == "axis", f"{m.get('scope')}")
            check("chroma chunk resource_type='daw_template'", m.get("resource_type") == "daw_template",
                  f"{m.get('resource_type')}")

    # D-cont) el doc global sigue existiendo tras reindex del curso.
    check("global sobrevive reindex(curso)", db_service.get_document(global_doc_id, "") is not None)


def scenario_visibility():
    print("\n== H) Visibilidad (resource_type solution => oculto; descarga 403) ==")
    # H1: subir solución sin fijar visibilidad => default oculto.
    async def _up():
        return await LR.upload_lesson_resource(
            lesson_id=LESSON, file=upfile("solucion ejercicio.md", b"# Solucion\nrespuesta correcta " * 20),
            title="p2test solucion", description="solucion del ejercicio",
            concepts="", index_to_tutor=True, visible_to_student=None, resource_type="solution", ctx=CTX,
        )
    resp = asyncio.run(_up())
    doc_id = resp["resource"]["doc_id"]
    _created.append(("lesson", doc_id))
    row = db_service.get_document(doc_id, COURSE)
    check("solution default visible_to_student=false", row.get("visible_to_student") is False,
          f"{row.get('visible_to_student')}")

    # H2: descarga pública de recurso no visible => 403.
    raised403 = False
    try:
        LR.download_resource_file(doc_id=doc_id, course_id=COURSE)
    except HTTPException as e:
        raised403 = (e.status_code == 403)
    check("descarga pública de no-visible => 403", raised403)

    # H3: el panel del alumno NO lista el recurso no visible.
    visibles = LR.student_lesson_resources(lesson_id=LESSON, course_id=COURSE)["resources"]
    check("alumno no ve recurso oculto", doc_id not in {r["doc_id"] for r in visibles})


def cleanup():
    print("\n== Limpieza de recursos de prueba ==")
    for kind, doc_id in _created:
        try:
            doc = db_service.get_document(doc_id, "" if kind == "global" else COURSE)
            if doc and doc.get("relpath"):
                fp = os.path.join(ingest.BASE_DIR, doc["relpath"])
                ingest.remove_single_document(fp)
                for p in (fp, os.path.splitext(fp)[0] + ".json"):
                    if os.path.exists(p):
                        os.remove(p)
            ingest.delete_resource_index(doc_id)
            db_service.delete_document(doc_id, "" if kind == "global" else COURSE)
        except Exception as e:
            print(f"    (no se pudo limpiar {doc_id}: {e})")
    print(f"    limpiados: {len(_created)}")


def main():
    asyncio.run(scenario_axis_document())
    asyncio.run(scenario_axis_template())
    asyncio.run(scenario_lesson_flp())
    gid = asyncio.run(scenario_global())
    asyncio.run(scenario_not_indexed())
    scenario_reindex_and_meta(gid)
    scenario_visibility()
    cleanup()
    print(f"\n=== RESULTADO FASE 2: {len(_passes)} PASS, {len(_fails)} FAIL ===")
    if _fails:
        print("Fallaron: " + ", ".join(_fails))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
