"""Validacion FINAL del piloto (READ-ONLY): timeline (P4) + 3 casos de chat.

NO escribe nada. Parsea el mapa de colores REAL desde BlockTimeline.jsx y lo
aplica a los modos de bloque en BD (prueba que P4 es solo visual). Luego corre
3 casos de /chat in-process replicando api/routes/chat.py.
"""

import io
import os
import re
import sys
from contextlib import contextmanager, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BLOCKTIMELINE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "frontend-tesis", "src", "shared", "components", "ai", "BlockTimeline.jsx",
)
COLOR_ES = {"indigo": "indigo", "emerald": "verde", "rose": "rosa", "amber": "ambar", "sky": "azul", "RED": "ROJO(default)"}


@contextmanager
def quiet():
    with redirect_stdout(io.StringIO()):
        yield


def hr(t):
    print("\n" + "=" * 76 + f"\n{t}\n" + "=" * 76)


def short(s, n=200):
    return (s or "").replace("\n", " ").strip()[:n]


# ---- Tarea 2: parsear el mapa REAL del JSX y aplicarlo a la BD ----
def parse_mode_map():
    src = open(BLOCKTIMELINE, encoding="utf-8").read()
    block = src.split("const MODE_COLORS", 1)[1].split("};", 1)[0]
    return {m: fam for m, fam in re.findall(r"(\w+):\s*FAMILY\.(\w+)", block)}


def tarea2():
    hr("TAREA 2 — Timeline (P4): color por modo desde el JSX real, aplicado a BD")
    from services import db_service as d
    mode_map = parse_mode_map()
    print(f"  Modos con color en BlockTimeline.jsx: {len(mode_map)} -> {sorted(set(mode_map.values()))}")
    with quiet():
        _ = d.get_lesson("E2-L01", "2")
    for lid in ("E2-L01", "E3-L01", "E4-L01"):
        with quiet():
            blocks = d.list_lesson_blocks(lid)
        reds = 0
        print(f"\n  {lid}: {len(blocks)} bloques")
        for b in blocks:
            mode = (b.get("interaction_mode") or "").strip().lower()
            fam = mode_map.get(mode, "RED")
            if fam == "RED":
                reds += 1
            print(f"    {b.get('block_id')}: mode={mode!r:32} -> {COLOR_ES[fam]}")
        print(f"    => rojos(default): {reds}/{len(blocks)}")


# ---- Tarea 3: 3 casos de /chat ----
CASES = [
    ("A", "E2-L01", "Eje 2", "E2-L01-B1", 20.0, "¿Debo cortar en solo o en mezcla?"),
    ("B", "E3-L01", "Eje 3", "E3-L01-B2", 60.0, "¿Cuándo uso bell y cuándo shelving?"),
    ("C", "E4-L01", "Eje 4", "E4-L01-B2", 50.0, "¿Qué debo mover primero en el compresor?"),
]


def tarea3():
    hr("TAREA 3 — Flujo del alumno: 3 casos de /chat (in-process)")
    from services.agent_service import super_agente
    from services.context_service import build_envelope, render_context_block
    from services.db_service import resolve_course_numeric

    for tag, lid, axis, expect_block, ts, msg in CASES:
        print(f"\n  ──────── CASO {tag} — {lid} (block esperado {expect_block}, ts={ts}) ────────")
        print(f"  msg: {msg}")
        err = None
        try:
            with quiet():
                scoped = resolve_course_numeric("2") or "2"
                env = build_envelope(question=msg,
                                     raw_activity_context={"current_lesson_id": lid, "current_axis": axis, "current_timestamp": ts},
                                     session_id="", has_image=False)
                ctxb = render_context_block(env)
                estado = {
                    "pregunta": msg, "course_id": scoped,
                    "current_lesson_id": env.activity_context.current_lesson_id,
                    "current_axis_id": env.activity_context.current_axis,
                    "contexto_leccion": "", "imagen": "", "ruta": "", "historial": [],
                    "respuesta_final": "", "evidencias": [], "evidence_level": "",
                    "intent": "", "answer_type": "", "course_module": "", "evaluation_category": "",
                    "requires_course_evidence": True, "warnings": [], "retrieved_chunks": [],
                    "trace_id": f"final-{tag}", "model_used": "", "prompt_id": "",
                    "activity_context_block": ctxb, "tutor_envelope": env,
                }
                res = super_agente.invoke(estado)
        except Exception as e:
            import traceback
            err = e
            print(f"  [ERROR 500] {e}")
            traceback.print_exc()
            continue

        ab = env.active_block or {}
        chunks = res.get("retrieved_chunks") or []
        usa_pdf = any(c.get("doc_type") == "pdf" for c in chunks)
        usa_tr = any(c.get("doc_type") == "video_transcript" or (c.get("source") or "").startswith("transcription:") for c in chunks)
        focus = ab.get("tutor_focus") or ""
        focus_inj = bool(focus) and focus in (ctxb or "")
        same_lesson_top = [c for c in chunks[:3] if str(c.get("lesson_id")) == lid]
        resp = res.get("respuesta_final") or ""
        # contextual: top chunks de la lección + evidencia no baja + responde sin "no tengo respaldo"
        generico = any(k in resp.lower() for k in ["no tengo suficiente", "no veo una fuente", "no hay respaldo"])
        contextual = (len(same_lesson_top) >= 1) and res.get("evidence_level") in ("alto", "medio") and not generico

        print(f"  error 500          : NO")
        print(f"  bloque activo      : {ab.get('block_id')} ({ab.get('start_time')}–{ab.get('end_time')}s)  [esperado {expect_block}: {'OK' if ab.get('block_id')==expect_block else 'MISMATCH'}]")
        print(f"  tutor_focus inyect.: {focus_inj}")
        print(f"  usó transcript     : {usa_tr}")
        print(f"  usó PDF            : {usa_pdf}")
        print(f"  intent / ruta      : {res.get('intent')} / {res.get('ruta')}  (evidence={res.get('evidence_level')})")
        print(f"  source_policy      : A_INDEXED_RAG={bool(chunks)} B_RUNTIME_CONTEXT={bool(ctxb)} C_SYSTEM_RULES=True")
        print(f"  top 3 chunks:")
        for i, c in enumerate(chunks[:3], 1):
            src = (c.get("source") or "")
            srcn = src.split("/")[-1] if "/" in src else src
            print(f"      #{i} score={c.get('score')} type={c.get('doc_type')} lesson={c.get('lesson_id')} src={srcn[:46]}")
        print(f"  respuesta {'CONTEXTUAL' if contextual else 'GENÉRICA'} (250c): {short(resp, 250)}")


def main():
    print("VALIDACIÓN FINAL DEL PILOTO (read-only)")
    tarea2()
    tarea3()


if __name__ == "__main__":
    main()
