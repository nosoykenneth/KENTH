"""Validacion de robustez / adversarial del piloto (READ-ONLY).

NO escribe en BD (solo build_envelope + super_agente.invoke + retrieval, que ya
solo leen). Cubre categorias A-J. Escribe resultados incrementales a JSONL y un
resumen final. La capa Pydantic/HTTP/auth se razona aparte (auth bloquea HTTP).

Uso: python scripts/validate_pilot_hardening.py
"""

import io
import json
import os
import sys
import time
import traceback
from contextlib import contextmanager, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_JSONL = os.path.join(os.path.dirname(__file__), "hardening_results.jsonl")
OUT_TXT = os.path.join(os.path.dirname(__file__), "hardening_report.txt")
AXIS = {"E2-L01": "Eje 2", "E3-L01": "Eje 3", "E4-L01": "Eje 4"}


@contextmanager
def quiet():
    with redirect_stdout(io.StringIO()):
        yield


def _lazy():
    from services.agent_service import super_agente
    from services.context_service import build_envelope, render_context_block
    from services.agent.retrieval import _buscar_evidencia
    from services.db_service import resolve_course_numeric
    return super_agente, build_envelope, render_context_block, _buscar_evidencia, resolve_course_numeric


def run_chat(message, lesson_id="", axis="", timestamp=None, include_ctx=True, course="2"):
    """Replica api/routes/chat.py in-process (sin auth, sin escribir BD)."""
    super_agente, build_envelope, render_context_block, _, resolve_course_numeric = _lazy()
    t0 = time.perf_counter()
    raw_ctx = None
    if include_ctx and (lesson_id or timestamp is not None or axis):
        raw_ctx = {}
        if lesson_id:
            raw_ctx["current_lesson_id"] = lesson_id
        if axis:
            raw_ctx["current_axis"] = axis
        if timestamp is not None:
            raw_ctx["current_timestamp"] = float(timestamp)
    try:
        with quiet():
            scoped = resolve_course_numeric(course) or course
            env = build_envelope(question=message, raw_activity_context=raw_ctx, session_id="", has_image=False)
            ctxb = render_context_block(env)
            estado = {
                "pregunta": message, "course_id": scoped,
                "current_lesson_id": env.activity_context.current_lesson_id,
                "current_axis_id": env.activity_context.current_axis,
                "contexto_leccion": "", "imagen": "", "ruta": "", "historial": [],
                "respuesta_final": "", "evidencias": [], "evidence_level": "",
                "intent": "", "answer_type": "", "course_module": "", "evaluation_category": "",
                "requires_course_evidence": True, "warnings": [], "retrieved_chunks": [],
                "trace_id": "hard", "model_used": "", "prompt_id": "",
                "activity_context_block": ctxb, "tutor_envelope": env,
            }
            res = super_agente.invoke(estado)
        ab = env.active_block or {}
        chunks = res.get("retrieved_chunks") or []
        focus = ab.get("tutor_focus") or ""
        resp = res.get("respuesta_final") or ""
        return {
            "error": None,
            "lat_ms": int((time.perf_counter() - t0) * 1000),
            "ruta": res.get("ruta"), "intent": res.get("intent"),
            "answer_type": res.get("answer_type"), "evidence_level": res.get("evidence_level"),
            "active_block": ab.get("block_id"),
            "focus_injected": bool(focus) and focus in (ctxb or ""),
            "ctx_block": bool(ctxb),
            "used_pdf": any(c.get("doc_type") == "pdf" for c in chunks),
            "used_transcript": any((c.get("doc_type") == "video_transcript") or (c.get("source") or "").startswith("transcription:") for c in chunks),
            "top": [{"t": c.get("doc_type"), "l": c.get("lesson_id"), "rel": c.get("context_relation"), "s": c.get("score")} for c in chunks[:3]],
            "warnings": [w.get("code") for w in (res.get("warnings") or [])],
            "resp": resp[:240].replace("\n", " "),
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-800:], "lat_ms": int((time.perf_counter() - t0) * 1000)}


def run_block(lesson_id, timestamp, axis=""):
    """Solo resolucion de bloque por timestamp (sin LLM)."""
    _, build_envelope, _, _, _ = _lazy()
    try:
        with quiet():
            raw = {"current_lesson_id": lesson_id} if lesson_id else None
            if raw is not None:
                if axis:
                    raw["current_axis"] = axis
                if timestamp is not None:
                    raw["current_timestamp"] = float(timestamp)
            env = build_envelope(question="x", raw_activity_context=raw, session_id="", has_image=False)
        ab = env.active_block or {}
        return {"error": None, "active_block": ab.get("block_id"),
                "range": f"{ab.get('start_time')}-{ab.get('end_time')}" if ab else None}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def run_retr(message, lesson_id, axis):
    """Solo retrieval (embeddings, sin LLM de texto)."""
    _, _, _, _buscar_evidencia, _ = _lazy()
    try:
        with quiet():
            ev = _buscar_evidencia(message, state={"course_id": "2", "current_axis_id": axis, "current_lesson_id": lesson_id})
        top = [{"t": i["document"].metadata.get("doc_type"), "l": i["document"].metadata.get("lesson_id"),
                "rel": i.get("context_relation"), "s": round(i.get("final_score", i.get("score")), 3)} for i in ev[:3]]
        same = all(str(t["l"]) == lesson_id for t in top) if top else False
        return {"error": None, "n": len(ev), "top": top, "all_same_lesson": same,
                "used_pdf": any((i["document"].metadata.get("doc_type") == "pdf" and str(i["document"].metadata.get("lesson_id")) == lesson_id) for i in ev)}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


# ============ BATERIA ============
def build_cases():
    C = []
    A = {
        "E2-L01": ["¿Debo cortar en solo o en mezcla?", "¿Por qué no usar HPF en todas las pistas?", "¿Qué significa frecuencia de corte?", "¿Qué recurso debo revisar?"],
        "E3-L01": ["¿Cuándo uso bell y cuándo shelving?", "¿Por qué el Q cambia tanto el resultado?", "¿El high shelf siempre da más aire?"],
        "E4-L01": ["¿Qué debo mover primero en el compresor?", "¿Por qué dejar el makeup en cero?", "¿Cuándo uso soft knee?"],
    }
    for lid, qs in A.items():
        for q in qs:
            C.append({"cat": "A", "mode": "chat", "lesson": lid, "ts": 20, "msg": q})

    B = ["hola", "ok", "gracias", "no entiendo", "y eso?", "qué hago?", "ahora qué?", "esto está bien?",
         "no me sale", "me perdí", "explícamelo más fácil", "puedes repetir?", "dónde estoy?", "qué debo hacer aquí?"]
    for q in B:
        C.append({"cat": "B", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": q})

    Cs = ["ke ago con el hpf", "pork no korto todo", "q es frecuensia de corte", "cuando uso shelvin",
          "como muevo el treshold", "q es ratio y kne", "me suena feo q hago"]
    for q in Cs:
        C.append({"cat": "C", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": q})

    D = ["¿Quién fue Napoleón?", "¿Cómo hago una pizza?", "¿Qué opinas de Bitcoin?", "¿Qué es una célula?", "¿Cómo arreglo mi impresora?", "¿Qué clima hace mañana?"]
    for q in D:
        C.append({"cat": "D", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": q})

    E = ["¿El HPF funciona como una dieta para adelgazar?", "¿El compresor es como Bitcoin?", "¿Puedo usar EQ para arreglar mi computadora?", "¿Qué tiene que ver Napoleón con el mastering?"]
    for q in E:
        C.append({"cat": "E", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": q})

    F = ["¿Qué PDF debo revisar?", "¿Qué recurso hay en esta lección?", "¿El tutor está usando la guía?", "¿De dónde sacaste eso?", "¿Está eso en el PDF o en el video?"]
    for lid in ("E2-L01", "E3-L01", "E4-L01"):
        for q in F:
            C.append({"cat": "F", "mode": "retr", "lesson": lid, "ts": 20, "msg": q})

    G = {"E2-L01": [0, 20, 34, 35, 79, 480, -5, 9999], "E3-L01": [0, 60, 499, 9999], "E4-L01": [0, 50, 499, 9999]}
    for lid, tss in G.items():
        for ts in tss:
            C.append({"cat": "G", "mode": "block", "lesson": lid, "ts": ts})

    # H — payloads incompletos/raros
    C += [
        {"cat": "H", "mode": "chat", "lesson": "E2-L01", "ts": None, "msg": "¿qué es frecuencia de corte?", "note": "sin timestamp"},
        {"cat": "H", "mode": "chat", "lesson": "", "ts": None, "msg": "¿qué es frecuencia de corte?", "note": "sin lesson_id"},
        {"cat": "H", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": "¿qué es frecuencia de corte?", "include_ctx": False, "note": "sin activity_context"},
        {"cat": "H", "mode": "chat", "lesson": "LECCION_INVALIDA", "ts": 20, "msg": "¿qué es hpf?", "note": "lesson_id inválido"},
        {"cat": "H", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": "", "note": "mensaje vacío"},
        {"cat": "H", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": "     ", "note": "solo espacios"},
        {"cat": "H", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": ("hpf " * 800).strip(), "note": "mensaje larguísimo"},
        {"cat": "H", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": "¿corto en solo?", "course": 2, "note": "course_id int"},
    ]

    # I — fuga entre lecciones
    I = [("E2-L01", "¿Cuándo uso bell y shelving?"), ("E2-L01", "¿Qué es soft knee?"),
         ("E3-L01", "¿Debo cortar con HPF?"), ("E3-L01", "¿Qué es threshold?"),
         ("E4-L01", "¿Qué es high shelf?"), ("E4-L01", "¿Por qué no usar HPF en todas las pistas?")]
    for lid, q in I:
        C.append({"cat": "I", "mode": "chat", "lesson": lid, "ts": 20, "msg": q})

    # J — estabilidad repetida
    for k in range(5):
        C.append({"cat": "J", "mode": "chat", "lesson": "E2-L01", "ts": 20, "msg": "¿Debo cortar en solo o en mezcla?", "note": f"run {k+1}"})

    return C


def main():
    cases = build_cases()
    open(OUT_JSONL, "w", encoding="utf-8").close()
    results = []
    print(f"Ejecutando {len(cases)} casos...")
    for i, c in enumerate(cases, 1):
        mode = c["mode"]
        if mode == "block":
            r = run_block(c["lesson"], c["ts"], AXIS.get(c["lesson"], ""))
        elif mode == "retr":
            r = run_retr(c["msg"], c["lesson"], AXIS.get(c["lesson"], ""))
        else:
            r = run_chat(c["msg"], c.get("lesson", ""), AXIS.get(c.get("lesson", ""), ""),
                         c.get("ts"), c.get("include_ctx", True), c.get("course", "2"))
        row = {**{k: c.get(k) for k in ("cat", "mode", "lesson", "ts", "msg", "note")}, **r}
        results.append(row)
        with open(OUT_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        tag = "ERR" if r.get("error") else "ok"
        print(f"  [{i}/{len(cases)}] {c['cat']} {mode} [{tag}] {str(c.get('msg',''))[:40]}")

    # ---- resumen ----
    cats = {}
    errs = []
    for r in results:
        cats.setdefault(r["cat"], []).append(r)
        if r.get("error"):
            errs.append(r)
    lines = ["", "=" * 70, "RESUMEN POR CATEGORIA", "=" * 70]
    for cat in sorted(cats):
        rows = cats[cat]
        n = len(rows)
        e = sum(1 for x in rows if x.get("error"))
        lines.append(f"  {cat}: {n} casos | errores(500/excepcion)={e}")
    lines.append(f"\nTOTAL casos={len(results)} | con error={len(errs)}")
    if errs:
        lines.append("\nERRORES:")
        for r in errs:
            lines.append(f"  [{r['cat']}] msg={r.get('msg')!r} ts={r.get('ts')} -> {r['error']}")
    out = "\n".join(lines)
    print(out)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(out + "\n")
    print(f"\nDetalle: {OUT_JSONL}\nResumen: {OUT_TXT}\nDONE")


if __name__ == "__main__":
    main()
