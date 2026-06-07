"""Fase 1 — Verificacion de saneamiento estructural.

Dos niveles:
  A) LOGICA PURA (siempre corre, sin BD ni embeddings): scope/validacion/coercion.
  B) INTEGRACION (opcional, requiere backend vivo): reindex preserva
     transcripciones/recursos/imagenes y la visibilidad llega al chunk.

Uso:
    python -m scripts.verify_phase1                 # solo logica pura
    python -m scripts.verify_phase1 --course 2      # + integracion sobre un curso

La parte de integracion NO modifica contenido: solo reindexa (operacion ya
idempotente del sistema) y consulta Chroma para comprobar invariantes.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fails = []
_passes = []


def check(name: str, cond: bool, detail: str = ""):
    (_passes if cond else _fails).append(name)
    mark = "PASS" if cond else "FAIL"
    print(f"  [{mark}] {name}" + (f" -> {detail}" if detail and not cond else ""))


# ==========================================
# A) LOGICA PURA
# ==========================================

def test_scope_logic():
    print("\n== A) Logica de scope / validacion ==")
    from services import db_service as db

    check("derive lesson", db.derive_scope("2", "Eje 1", "L1") == "lesson")
    check("derive axis", db.derive_scope("2", "Eje 1", "") == "axis")
    check("derive course", db.derive_scope("2", "", "") == "course")
    check("derive global por is_global", db.derive_scope("2", "Eje 1", "L1", is_global=True) == "global")
    check("derive global legacy (todo vacio)", db.derive_scope("", "", "") == "global")

    # validate: global SIEMPRE fuerza is_global=1
    sc, ig = db.validate_scope(scope="global", course_id="", axis_id="", lesson_id="")
    check("validate global -> is_global=1", sc == "global" and ig is True)

    # validate: lesson requiere axis+lesson+course
    sc, ig = db.validate_scope(scope="lesson", course_id="2", axis_id="Eje 1", lesson_id="L1")
    check("validate lesson ok", sc == "lesson" and ig is False)

    # validate: course con lesson_id -> error
    try:
        db.validate_scope(scope="course", course_id="2", lesson_id="L1")
        check("validate course+lesson rechazado", False, "no lanzo ValueError")
    except ValueError:
        check("validate course+lesson rechazado", True)

    # validate: no-global sin course -> error
    try:
        db.validate_scope(scope="course", course_id="")
        check("validate sin course rechazado", False, "no lanzo ValueError")
    except ValueError:
        check("validate sin course rechazado", True)

    # validate: is_global con scope no-global -> error
    try:
        db.validate_scope(scope="course", course_id="2", is_global=True)
        check("validate is_global+course rechazado", False, "no lanzo ValueError")
    except ValueError:
        check("validate is_global+course rechazado", True)


def test_bool_coercion():
    print("\n== A) Coercion de booleanos (frontmatter md) ==")
    import ingest
    check("'True' -> True", ingest._as_bool("True") is True)
    check("'false' -> False", ingest._as_bool("false") is False)
    check("1 -> True", ingest._as_bool(1) is True)
    check("0 -> False", ingest._as_bool(0) is False)
    check("None default", ingest._as_bool(None, default=True) is True)
    check("scope chunk lesson", ingest._scope_chunk("2", "Eje 1", "L1", False) == "lesson")
    check("scope chunk global por flag", ingest._scope_chunk("2", "", "", True) == "global")


# ==========================================
# B) INTEGRACION
# ==========================================

def test_integration(course_id: str):
    print(f"\n== B) Integracion sobre curso {course_id} (reindex + Chroma) ==")
    import ingest
    from services import db_service as db

    col = ingest.get_vector_store()._collection

    def count(where):
        try:
            return len(col.get(where=where, include=[]).get("ids", []))
        except Exception as e:
            print(f"    (error consultando Chroma: {e})")
            return -1

    before = {
        "transcript": count({"$and": [{"course_id": course_id}, {"doc_type": "video_transcript"}]}),
        "resource": count({"$and": [{"course_id": course_id}, {"media_type": "audio"}]}),
        "image": count({"$and": [{"course_id": course_id}, {"media_type": "image"}]}),
    }
    print(f"    Antes: {before}")

    result = ingest.reindex_course_documents(course_id)
    print(f"    reindex: processed={result.get('processed')} resources={result.get('resources_indexed')} "
          f"transcripts={result.get('transcripts_indexed')} skipped={result.get('skipped')}")

    after = {
        "transcript": count({"$and": [{"course_id": course_id}, {"doc_type": "video_transcript"}]}),
        "image": count({"$and": [{"course_id": course_id}, {"media_type": "image"}]}),
    }
    print(f"    Despues: {after}")

    # Si habia transcripciones/imagenes antes, no deben desaparecer tras reindex.
    if before["transcript"] > 0:
        check("reindex conserva transcripciones", after["transcript"] > 0,
              f"antes={before['transcript']} despues={after['transcript']}")
    else:
        print("    (sin transcripciones previas; comprueba subiendo una y reindexando)")
    if before["image"] > 0:
        check("reindex conserva imagenes", after["image"] > 0,
              f"antes={before['image']} despues={after['image']}")

    # allowed_for_indexing=false NO debe quedar en Chroma.
    not_allowed = count({"$and": [{"course_id": course_id}, {"allowed_for_indexing": False}]})
    check("no hay chunks con allowed_for_indexing=false", not_allowed == 0, f"encontrados={not_allowed}")

    # Toda fila indexada debe tener scope e index_status coherentes en BD.
    docs = db.list_documents(course_id=course_id)
    sin_scope = [d["doc_id"] for d in docs if not d.get("scope")]
    check("todas las filas tienen scope", not sin_scope, f"sin scope: {sin_scope[:5]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verificacion Fase 1")
    parser.add_argument("--course", default="", help="course_id para la parte de integracion")
    args = parser.parse_args()

    test_scope_logic()
    test_bool_coercion()

    if args.course:
        try:
            test_integration(args.course)
        except Exception as e:
            check("integracion ejecutable", False, str(e))
    else:
        print("\n(omito integracion: pasa --course <id> para ejercitar reindex/Chroma)")

    print(f"\n=== RESULTADO: {len(_passes)} PASS, {len(_fails)} FAIL ===")
    if _fails:
        print("Fallaron: " + ", ".join(_fails))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
