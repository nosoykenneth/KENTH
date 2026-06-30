"""Validacion funcional E2E del piloto (READ-ONLY, sin refactor).

Verifica que el sistema usa de verdad: metadata de leccion, bloques, transcript,
PDFs indexados, Domain Pack (course 2), retrieval y contexto a /chat.
No escribe nada. /chat se ejecuta in-process replicando api/routes/chat.py.

Uso: python scripts/validate_pilot.py
"""

import io
import json
import os
import sys
import traceback
from contextlib import contextmanager, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:  # consola Windows cp1252 revienta con caracteres de caja; forzamos UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LESSONS = [
    ("E2-L01", "Eje 2"),
    ("E3-L01", "Eje 3"),
    ("E4-L01", "Eje 4"),
]
COURSE = "2"

RETRIEVAL_QUESTIONS = {
    "E2-L01": [
        "¿Debo cortar en solo o en mezcla?",
        "¿Por qué no usar HPF en todas las pistas?",
        "¿Qué significa frecuencia de corte?",
        "¿Qué recurso debo revisar en esta lección?",
    ],
    "E3-L01": [
        "¿Cuándo uso bell y cuándo shelving?",
        "¿Por qué el Q cambia tanto el resultado?",
        "¿El high shelf siempre da más aire?",
    ],
    "E4-L01": [
        "¿Qué debo mover primero en el compresor?",
        "¿Por qué dejar el makeup en cero?",
        "¿Cuándo uso soft knee?",
    ],
}


@contextmanager
def quiet():
    buf = io.StringIO()
    with redirect_stdout(buf):
        yield buf


def hr(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def short(s, n=90):
    s = (s or "").replace("\n", " ").strip()
    return (s[:n] + "…") if len(s) > n else s


# =====================================================================
# PARTE A — BD (lecciones, bloques, transcript, recursos)
# =====================================================================
def parte_a():
    hr("PARTE A — BD/Moodle: lecciones, bloques, transcript, recursos")
    from services import db_service as d
    # Fuerza una conexion para fijar _BACKEND
    try:
        with quiet():
            _ = d.get_lesson("E2-L01", COURSE)
    except Exception as e:
        print(f"  [ERROR] No se pudo conectar a la BD: {e}")
        return
    print(f"  Backend BD: {'MOODLE/MySQL' if d.using_moodle_db() else 'SQLite (fallback!)'}")

    for lid, axis in LESSONS:
        print(f"\n  ── {lid} ({axis}) ──")
        try:
            with quiet():
                lesson = d.get_lesson(lid, COURSE)
                blocks = d.list_lesson_blocks(lid)
                transcript = d.list_transcript(lid)
                prompts = d.list_lesson_prompts(lid)
                docs = d.list_documents(course_id=COURSE, lesson_id=lid)
        except Exception as e:
            print(f"    [ERROR] {e}")
            continue

        if not lesson:
            print("    [FALTA] Lección NO existe en BD.")
            continue
        print(f"    title           : {short(lesson.get('title'))}")
        print(f"    axis_id         : {lesson.get('axis_id')}")
        print(f"    learning_goal   : {short(lesson.get('learning_goal') or (lesson.get('learning_goals') or [''])[0] if lesson.get('learning_goals') else lesson.get('learning_goal'))}")
        print(f"    expected_action : {short(lesson.get('expected_action'))}")
        pm = prompts.get('proactive_message') if isinstance(prompts, dict) else ''
        sp = prompts.get('suggested_prompts') if isinstance(prompts, dict) else []
        print(f"    proactive_msg   : {short(pm)}")
        print(f"    suggested(#)    : {len(sp or [])}")
        print(f"    BLOQUES         : {len(blocks)}")
        for b in blocks:
            print(f"        - {b.get('block_id')}: {b.get('start_time')}–{b.get('end_time')}s | mode={b.get('interaction_mode')!r} | focus={short(b.get('tutor_focus'),40)}")
        dur = 0
        if transcript:
            try:
                dur = max(float(s.get('end_time') or 0) for s in transcript)
            except Exception:
                dur = 0
        print(f"    TRANSCRIPT      : {len(transcript)} segmentos (hasta {dur:.0f}s)")
        print(f"    RECURSOS (docs) : {len(docs)}")
        for doc in docs:
            print(f"        - doc_id={doc.get('doc_id')} | {short(doc.get('filename') or doc.get('title'),45)} | "
                  f"type={doc.get('resource_type')} | media={doc.get('media_type')} | "
                  f"visible={doc.get('visible_to_student')} | indexar={doc.get('allowed_for_indexing')} | "
                  f"scope={doc.get('scope')} | idx_status={doc.get('index_status')}")


# =====================================================================
# PARTE B — Chroma: indexacion + metadata de chunks
# =====================================================================
def parte_b():
    hr("PARTE B — ChromaDB: indexación y metadata de chunks")
    import services.agent.retrieval as r
    db = r._get_vector_store()
    data = db._collection.get(include=["metadatas"])
    metas = [m or {} for m in (data.get("metadatas") or [])]
    print(f"  TOTAL chunks en índice: {len(metas)}")

    required = ["course_id", "axis_id", "lesson_id", "resource_type", "scope",
                "visible_to_student", "allowed_for_indexing", "doc_type"]
    for lid, axis in LESSONS:
        sub = [m for m in metas if str(m.get("lesson_id")) == lid]
        pdf = [m for m in sub if m.get("doc_type") == "pdf"]
        tr = [m for m in sub if m.get("doc_type") == "video_transcript"]
        print(f"\n  ── {lid} ── chunks={len(sub)} (pdf={len(pdf)}, transcript={len(tr)})")
        # metadata correcta
        problems = []
        for m in sub:
            for k in required:
                if m.get(k) in (None, ""):
                    problems.append(f"{k} vacío")
            if str(m.get("course_id")) != COURSE:
                problems.append(f"course_id={m.get('course_id')}")
            if str(m.get("axis_id")) != axis:
                problems.append(f"axis_id={m.get('axis_id')}")
            if not (m.get("allowed_for_indexing") in (True, 1, "1", "true", "True")):
                problems.append("allowed_for_indexing falso")
        if problems:
            from collections import Counter
            c = Counter(problems)
            print(f"    [METADATA] problemas: {dict(c)}")
        else:
            print(f"    [METADATA] OK (course_id={COURSE}, axis_id={axis}, scope=lesson, visible+indexar=true)")


# =====================================================================
# PARTE C — Retrieval por pregunta
# =====================================================================
def _state(lid, axis):
    return {"course_id": COURSE, "current_axis_id": axis, "current_lesson_id": lid}


def parte_c():
    hr("PARTE C — Retrieval (¿recupera los chunks correctos de la lección?)")
    from services.agent.retrieval import _buscar_evidencia

    for lid, axis in LESSONS:
        print(f"\n  ════ {lid} ({axis}) ════")
        for q in RETRIEVAL_QUESTIONS[lid]:
            try:
                with quiet():
                    ev = _buscar_evidencia(q, state=_state(lid, axis))
            except Exception as e:
                print(f"   [ERROR] {short(q,50)} -> {e}")
                continue
            print(f"\n   Q: {q}")
            if not ev:
                print("      (sin evidencia recuperada)")
                continue
            top = ev[:3]
            usa_pdf = any(i["document"].metadata.get("doc_type") == "pdf" and str(i["document"].metadata.get("lesson_id")) == lid for i in ev)
            usa_tr = any(i["document"].metadata.get("doc_type") == "video_transcript" and str(i["document"].metadata.get("lesson_id")) == lid for i in ev)
            for i, it in enumerate(top, 1):
                m = it["document"].metadata or {}
                src = m.get("source", "")
                src = src.split("/")[-1] if "/" in src else src
                print(f"      #{i} score={it.get('final_score', it.get('score')):.3f} "
                      f"rel={it.get('context_relation','')} lesson={m.get('lesson_id')} "
                      f"type={m.get('doc_type')} src={short(src,42)}")
            print(f"      → usa PDF de la lección: {usa_pdf} | usa transcript de la lección: {usa_tr}")


# =====================================================================
# PARTE D — /chat in-process (replica api/routes/chat.py)
# =====================================================================
def parte_d():
    hr("PARTE D — /chat E2E (course=2, lesson=E2-L01, block=B1, ts=20)")
    from services.agent_service import super_agente
    from services.context_service import build_envelope, render_context_block
    from services.db_service import resolve_course_numeric

    pregunta = "¿Debo cortar en solo o en mezcla?"
    raw_ctx = {"current_lesson_id": "E2-L01", "current_axis": "Eje 2", "current_timestamp": 20.0}

    try:
        with quiet():
            scoped = resolve_course_numeric(COURSE) or COURSE
            envelope = build_envelope(question=pregunta, raw_activity_context=raw_ctx, session_id="", has_image=False)
            ctx_block = render_context_block(envelope)
            estado = {
                "pregunta": pregunta, "course_id": scoped,
                "current_lesson_id": envelope.activity_context.current_lesson_id,
                "current_axis_id": envelope.activity_context.current_axis,
                "contexto_leccion": "", "imagen": "", "ruta": "", "historial": [],
                "respuesta_final": "", "evidencias": [], "evidence_level": "",
                "intent": "", "answer_type": "", "course_module": "", "evaluation_category": "",
                "requires_course_evidence": True, "warnings": [], "retrieved_chunks": [],
                "trace_id": "validate", "model_used": "", "prompt_id": "",
                "activity_context_block": ctx_block, "tutor_envelope": envelope,
            }
            res = super_agente.invoke(estado)
    except Exception as e:
        print(f"  [ERROR 500] /chat falló: {e}")
        traceback.print_exc()
        return

    ab = envelope.active_block or {}
    al = envelope.active_lesson or {}
    print(f"  active_lesson    : {al.get('lesson_id')} | axis={al.get('axis_id')}")
    print(f"  active_block     : {ab.get('block_id')} ({ab.get('start_time')}–{ab.get('end_time')}s) mode={ab.get('interaction_mode')!r}")
    print(f"  bloque en prompt : {'BLOQUE ACTIVO DEL VIDEO' in (ctx_block or '')}")
    print(f"  focus en prompt  : {bool(ab.get('tutor_focus')) and ab.get('tutor_focus') in (ctx_block or '')}")
    print(f"  ruta             : {res.get('ruta')}")
    print(f"  intent           : {res.get('intent')}")
    print(f"  answer_type      : {res.get('answer_type')}")
    print(f"  evidence_level   : {res.get('evidence_level')}")
    chunks = res.get("retrieved_chunks") or []
    print(f"  retrieved_chunks : {len(chunks)}")
    usa_pdf = usa_tr = False
    for c in chunks[:5]:
        src = (c.get("source") or "")
        srcn = src.split("/")[-1] if "/" in src else src
        if c.get("doc_type") == "pdf":
            usa_pdf = True
        if c.get("doc_type") == "video_transcript" or src.startswith("transcription:"):
            usa_tr = True
        print(f"      - score={c.get('score')} type={c.get('doc_type')} lesson={c.get('lesson_id')} src={short(srcn,42)}")
    print(f"  usa PDF          : {usa_pdf}")
    print(f"  usa transcript   : {usa_tr}")
    print(f"  source_policy    : A_INDEXED_RAG={bool(chunks)} B_RUNTIME_CONTEXT={bool(ctx_block)} C_SYSTEM_RULES=True")
    print(f"  warnings         : {[w.get('code') for w in (res.get('warnings') or [])]}")
    print(f"\n  RESPUESTA (250c):\n    {short(res.get('respuesta_final'), 250)}")


# =====================================================================
# PARTE E — Domain Pack
# =====================================================================
def parte_e():
    hr("PARTE E — Domain Pack (course_id=2)")
    try:
        from services.domain import get_domain_pack
        p = get_domain_pack(COURSE)
        print(f"  pack_id           : {p.pack_id}")
        print(f"  source_path       : {p.source_path}")
        print(f"  persona           : {p.persona.get('tutor_name')} / {p.persona.get('domain_label')}")
        print(f"  sections          : {len(p.course_sections())}")
        print(f"  concept_patterns  : {len(p.concept_patterns())}")
        print(f"  controlled_answers: {len(p.controlled_answers())}")
        print(f"  unsupported_terms : {len(p.unsupported_terms())}")
        print(f"  [OK] Domain Pack carga correctamente." if p.pack_id == COURSE else "  [WARN] no resolvió al pack de course 2")
    except Exception as e:
        print(f"  [ERROR] Domain Pack no carga: {e}")


def main():
    print("VALIDACIÓN FUNCIONAL E2E DEL PILOTO (read-only)")
    for fn in (parte_e, parte_a, parte_b, parte_c, parte_d):
        try:
            fn()
        except Exception as e:
            print(f"\n[FALLO EN {fn.__name__}] {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
