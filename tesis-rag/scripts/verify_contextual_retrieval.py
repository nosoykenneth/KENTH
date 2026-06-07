"""Fase 3 - verificacion de ranking contextual de retrieval.

No escribe contenido ni toca Chroma. Usa documentos dummy con metadata equivalente
a los chunks reales para validar filtros, scope_affinity, ranking y truncado.

Uso:
  python scripts/verify_contextual_retrieval.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document  # noqa: E402

from services.agent.retrieval import (  # noqa: E402
    _chunks_desde_evidencias,
    _context_relation,
    _matches_course_scope,
    _preparar_evidencias_contextuales,
    _scope_affinity,
)


COURSE = "2"
AXIS = "Eje 2"
LESSON = "E2-L01"

_passes = []
_fails = []


def check(name, cond, detail=""):
    (_passes if cond else _fails).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" -> {detail}" if detail and not cond else ""))


def meta(scope, *, course=COURSE, axis=AXIS, lesson="", title="", allowed=True, visible=True, extra=None):
    data = {
        "source": f"dummy:{title or scope}",
        "filename": f"{title or scope}.md",
        "title": title or scope,
        "resource_title": title or scope,
        "scope": scope,
        "course_id": course,
        "axis_id": axis,
        "lesson_id": lesson,
        "allowed_for_indexing": allowed,
        "visible_to_student": visible,
        "index_status": "indexed" if allowed else "pending",
        "media_type": "document",
        "resource_type": "theory",
        "is_global": scope == "global",
    }
    if scope == "global":
        data["course_id"] = ""
        data["axis_id"] = ""
        data["lesson_id"] = ""
    if extra:
        data.update(extra)
    return data


def item(scope, text, score, **kwargs):
    m = meta(scope, **kwargs)
    return {"document": Document(page_content=text, metadata=m), "score": score}


def rank(items, question="filtros frecuencia de corte", state=None):
    state = state or {
        "course_id": COURSE,
        "current_axis_id": AXIS,
        "current_lesson_id": LESSON,
    }
    return _preparar_evidencias_contextuales(items, question, state, modo_lookup=False)


def case_a_lesson_wins():
    print("\n== A) Pregunta desde E2-L01 sobre recurso de la leccion ==")
    ranked = rank([
        item("global", "teoria universal de audio", 0.74, title="global"),
        item("course", "teoria general del curso", 0.72, title="course", axis="", lesson=""),
        item("axis", "apunte general de filtros", 0.70, title="axis"),
        item("lesson", "Another trap plantilla de la leccion E2-L01", 0.50, title="another trap", lesson=LESSON),
    ], "para que sirve Another trap")
    top = ranked[0]["document"].metadata
    check("rankea primero lesson E2-L01", top.get("scope") == "lesson" and top.get("lesson_id") == LESSON)
    check("scope_affinity lesson = 0.80", _scope_affinity(top, {"course_id": COURSE, "current_axis_id": AXIS, "current_lesson_id": LESSON}) == 0.80)


def case_b_specific_limits_generic():
    print("\n== B) Filtros en general: lesson/eje antes que generico ==")
    ranked = rank([
        item("global", "filtros universales y teoria global", 0.67, title="global"),
        item("course", "filtros del curso mezcla", 0.66, title="course", axis="", lesson=""),
        item("axis", "filtros pasa altos pasa bajos del Eje 2", 0.68, title="axis"),
        item("lesson", "filtros usados en la leccion E2-L01", 0.62, title="lesson", lesson=LESSON),
    ])
    scopes = [r["document"].metadata.get("scope") for r in ranked]
    generic_count = sum(1 for s in scopes if s in {"course", "global"})
    check("lesson queda primero", scopes[0] == "lesson", str(scopes))
    check("axis queda antes que curso/global", scopes.index("axis") < min([i for i, s in enumerate(scopes) if s in {"course", "global"}], default=99), str(scopes))
    check("limita genericos a maximo 1", generic_count <= 1, str(scopes))


def case_c_course_global_when_no_specific():
    print("\n== C) Sin evidencia lesson/eje suficiente: permite curso/global ==")
    ranked = rank([
        item("global", "teoria universal de headroom", 0.71, title="global"),
        item("course", "teoria general del curso sobre headroom", 0.62, title="course", axis="", lesson=""),
    ], "que es headroom")
    scopes = [r["document"].metadata.get("scope") for r in ranked]
    check("recupera curso/global", set(scopes) == {"course", "global"}, str(scopes))
    check("course gana sobre global por afinidad", scopes[0] == "course", str(scopes))


def case_d_other_axis_marked():
    print("\n== D) Concepto de otro eje: se marca other_axis ==")
    ranked = rank([
        item("axis", "compresion paralela y dinamica avanzada", 0.96, title="axis4", axis="Eje 4"),
    ], "que es compresion paralela")
    relation = ranked[0].get("context_relation")
    check("recupera evidencia de otro eje si es alta", bool(ranked))
    check("queda marcada como other_axis", relation == "other_axis", relation)


def case_e_empty_lesson_uses_axis_course_global():
    print("\n== E) Leccion sin recursos: eje -> curso -> global ==")
    ranked = rank([
        item("global", "teoria universal", 0.65, title="global"),
        item("course", "teoria del curso", 0.60, title="course", axis="", lesson=""),
        item("axis", "apunte de filtros Eje 2", 0.58, title="axis"),
    ], state={"course_id": COURSE, "current_axis_id": AXIS, "current_lesson_id": "E2-L99"})
    scopes = [r["document"].metadata.get("scope") for r in ranked]
    check("axis gana por afinidad de eje", scopes[0] == "axis", str(scopes))


def case_f_allowed_filter():
    print("\n== F) allowed_for_indexing=false no entra ==")
    ranked = rank([
        item("lesson", "texto prohibido", 0.99, title="no_index", lesson=LESSON, allowed=False),
        item("lesson", "texto permitido", 0.40, title="ok", lesson=LESSON, allowed=True),
    ])
    titles = [r["document"].metadata.get("title") for r in ranked]
    check("excluye chunk no permitido", "no_index" not in titles, str(titles))


def case_g_hidden_visible_allowed():
    print("\n== G) visible=false + allowed=true se usa, pero viaja oculto ==")
    ranked = rank([
        item("lesson", "solucion interna indexable", 0.61, title="hidden", lesson=LESSON, visible=False),
    ])
    chunks = _chunks_desde_evidencias(ranked)
    check("chunk oculto indexable entra como conocimiento", bool(chunks))
    check("visible_to_student=false viaja en fuente", chunks[0].get("visible_to_student") is False, str(chunks[0]))


def case_h_hard_course_global_filter():
    print("\n== H) Curso actual o global explicito solamente ==")
    state = {"course_id": COURSE, "current_axis_id": AXIS, "current_lesson_id": LESSON}
    other_course = meta("course", course="999", axis="", lesson="", title="other")
    fake_global = meta("course", course="", axis="", lesson="", title="fake_global")
    real_global = meta("global", title="real_global")
    check("bloquea otro curso", not _matches_course_scope(other_course, state))
    check("bloquea course_id vacio sin global explicito", not _matches_course_scope(fake_global, state))
    check("permite global explicito", _matches_course_scope(real_global, state))
    check("relacion global explicita", _context_relation(real_global, state) == "global")


def main():
    case_a_lesson_wins()
    case_b_specific_limits_generic()
    case_c_course_global_when_no_specific()
    case_d_other_axis_marked()
    case_e_empty_lesson_uses_axis_course_global()
    case_f_allowed_filter()
    case_g_hidden_visible_allowed()
    case_h_hard_course_global_filter()
    print(f"\n=== RESULTADO FASE 3 CONTEXTUAL: {len(_passes)} PASS, {len(_fails)} FAIL ===")
    if _fails:
        print("Fallaron: " + ", ".join(_fails))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
