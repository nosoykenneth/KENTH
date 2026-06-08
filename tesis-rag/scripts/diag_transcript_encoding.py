"""Diagnóstico (READ-ONLY) de encoding de transcripts E2-L01/E3-L01/E4-L01.

NO escribe nada. Determina si el mojibake es:
  A) falso (UTF-8 valido, solo se veia mal en consola),
  B) doble-encoding recuperable (cp1252/latin1 -> utf8),
  C) U+FFFD irrecuperable (bytes perdidos).

Analiza codepoints reales (via ascii()) en la BD (transcript_segments) y en
ChromaDB, y prueba la recuperacion. Vuelca detalle a un archivo UTF-8.
"""

import io
import os
import sys
from contextlib import contextmanager, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LESSONS = ["E2-L01", "E3-L01", "E4-L01"]
OUT = os.path.join(os.path.dirname(__file__), "diag_transcript_report.txt")
report = []


@contextmanager
def quiet():
    buf = io.StringIO()
    with redirect_stdout(buf):
        yield buf


def both(s):
    print(s)
    report.append(s)


FFFD = "�"
MOJIBAKE_MARKERS = ["Ã", "Â", "â€", "Ã©", "Ã±", "Ã³", "Ã­", "Ãº", "Ã¡", "ðŸ"]


def analyze(text):
    fffd = text.count(FFFD)
    markers = [m for m in MOJIBAKE_MARKERS if m in text]
    # Intento de recuperacion doble-encoding: utf8 mal leido como cp1252/latin1.
    recovered = None
    for enc in ("cp1252", "latin-1"):
        try:
            cand = text.encode(enc).decode("utf-8")
            recovered = (enc, cand)
            break
        except Exception:
            continue
    return fffd, markers, recovered


def sample_codepoints(text, n=70):
    return ascii(text[:n])  # \uXXXX, nunca crashea, muestra el codepoint real


def main():
    both("DIAGNOSTICO DE ENCODING DE TRANSCRIPTS (read-only)\n" + "=" * 70)

    # ---- BD (fuente de verdad) ----
    from services import db_service as d
    try:
        with quiet():
            _ = d.get_lesson("E2-L01", "2")
        both(f"\nBackend BD: {'MOODLE/MySQL' if d.using_moodle_db() else 'SQLite'}")
    except Exception as e:
        both(f"[ERROR conexion BD] {e}")
        return

    both("\n##### 1) BASE DE DATOS (transcript_segments) #####")
    db_state = {}
    for lid in LESSONS:
        try:
            with quiet():
                segs = d.list_transcript(lid)
        except Exception as e:
            both(f"  {lid}: [ERROR] {e}")
            continue
        tot_fffd = 0
        any_markers = set()
        recov_ok = 0
        first_dirty = None
        for s in segs:
            t = s.get("text") or ""
            fffd, markers, recovered = analyze(t)
            tot_fffd += fffd
            any_markers.update(markers)
            if markers and recovered and FFFD not in recovered[1]:
                recov_ok += 1
            if first_dirty is None and (fffd or markers):
                first_dirty = (t, recovered)
        db_state[lid] = {"fffd": tot_fffd, "markers": any_markers, "n": len(segs)}
        both(f"\n  {lid}: {len(segs)} segmentos | U+FFFD total={tot_fffd} | mojibake markers={sorted(any_markers)} | recuperables(latin1->utf8)={recov_ok}")
        if first_dirty:
            t, recovered = first_dirty
            both(f"    SAMPLE crudo     : {sample_codepoints(t)}")
            if recovered:
                both(f"    SAMPLE recuperado: {sample_codepoints(recovered[1])}  (via {recovered[0]})")
            else:
                both("    SAMPLE recuperado: (no aplica / no decodifica como utf8)")

    # ---- Chroma (indice) ----
    both("\n\n##### 2) CHROMADB (chunks de transcripcion) #####")
    import services.agent.retrieval as r
    db = r._get_vector_store()
    data = db._collection.get(include=["metadatas", "documents"])
    metas = data.get("metadatas") or []
    docs = data.get("documents") or []
    for lid in LESSONS:
        chunks = [(m or {}, dc or "") for m, dc in zip(metas, docs)
                  if (m or {}).get("source") == f"transcription:{lid}"]
        tot_fffd = sum(dc.count(FFFD) for _, dc in chunks)
        markers = set()
        for _, dc in chunks:
            for mk in MOJIBAKE_MARKERS:
                if mk in dc:
                    markers.add(mk)
        both(f"\n  {lid}: {len(chunks)} chunks | U+FFFD total={tot_fffd} | mojibake markers={sorted(markers)}")
        if chunks:
            both(f"    SAMPLE chunk     : {sample_codepoints(chunks[0][1])}")

    # ---- Veredicto ----
    both("\n\n##### 3) VEREDICTO #####")
    total_fffd_db = sum(v["fffd"] for v in db_state.values())
    total_markers_db = any(v["markers"] for v in db_state.values())
    if total_fffd_db > 0:
        both("  -> CASO C (parcial): hay U+FFFD en BD = bytes perdidos, IRRECUPERABLES desde texto.")
    if total_markers_db:
        both("  -> CASO B: hay marcadores de doble-encoding en BD = RECUPERABLES por re-decodificacion.")
    if total_fffd_db == 0 and not total_markers_db:
        both("  -> CASO A: BD limpia (UTF-8 valido). El mojibake era artefacto de consola; NO hay que tocar datos.")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    both(f"\n(Detalle completo en {OUT})")


if __name__ == "__main__":
    main()
