"""Mide la distribucion real de tamanos de chunk en Chroma.

Read-only. No modifica el indice. Reporta:
- distribucion global de longitud (chars y tokens aprox)
- breakdown por doc_type y por scope
- chunks sospechosos: muy grandes, muy chicos, o cortados a mitad de palabra
"""
import os
import statistics
import collections

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "bd_vectorial")

import chromadb

client = chromadb.PersistentClient(CHROMA_DIR)
cols = client.list_collections()
print(f"Colecciones: {[c.name for c in cols]}")

col = client.get_collection("langchain")
data = col.get(include=["documents", "metadatas"])
docs = data.get("documents") or []
metas = data.get("metadatas") or []
print(f"Total chunks: {len(docs)}\n")


def approx_tokens(n_chars):
    # aprox conservador es/en: ~4 chars por token
    return n_chars / 4.0


def pct(values, p):
    if not values:
        return 0
    s = sorted(values)
    k = (len(s) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] + (s[c] - s[f]) * (k - f)


def resumen(nombre, lengths):
    if not lengths:
        print(f"  {nombre}: (sin chunks)")
        return
    print(
        f"  {nombre:28s} n={len(lengths):4d} "
        f"min={min(lengths):4d} p25={int(pct(lengths,25)):4d} "
        f"med={int(statistics.median(lengths)):4d} p75={int(pct(lengths,75)):4d} "
        f"p90={int(pct(lengths,90)):4d} p95={int(pct(lengths,95)):4d} "
        f"max={max(lengths):5d} | tokens med~{int(approx_tokens(statistics.median(lengths))):3d} "
        f"max~{int(approx_tokens(max(lengths))):4d}"
    )


lengths_all = [len(d or "") for d in docs]

print("=== DISTRIBUCION GLOBAL (chars) ===")
resumen("TODOS", lengths_all)

print("\n=== POR doc_type ===")
by_type = collections.defaultdict(list)
for d, m in zip(docs, metas):
    by_type[(m or {}).get("doc_type") or "(sin doc_type)"].append(len(d or ""))
for k in sorted(by_type):
    resumen(k, by_type[k])

print("\n=== POR scope ===")
by_scope = collections.defaultdict(list)
for d, m in zip(docs, metas):
    m = m or {}
    scope = m.get("scope")
    if not scope:
        if m.get("is_global"):
            scope = "(is_global)"
        elif m.get("lesson_id"):
            scope = "(infer:lesson)"
        elif m.get("axis_id"):
            scope = "(infer:axis)"
        elif m.get("course_id"):
            scope = "(infer:course)"
        else:
            scope = "(vacio)"
    by_scope[scope].append(len(d or ""))
for k in sorted(by_scope):
    resumen(k, by_scope[k])

print("\n=== media_type (recursos) ===")
by_media = collections.defaultdict(list)
for d, m in zip(docs, metas):
    mt = (m or {}).get("media_type")
    if mt:
        by_media[mt].append(len(d or ""))
for k in sorted(by_media):
    resumen(k, by_media[k])

print("\n=== CHUNKS SOSPECHOSOS ===")
muy_chico = [(d, m) for d, m in zip(docs, metas) if 0 < len(d or "") < 120]
muy_grande = [(d, m) for d, m in zip(docs, metas) if len(d or "") > 1600]
vacios = [(d, m) for d, m in zip(docs, metas) if len(d or "") == 0]

print(f"  vacios (0 chars):       {len(vacios)}")
print(f"  muy chicos (<120 chars): {len(muy_chico)}")
print(f"  muy grandes (>1600):     {len(muy_grande)}")


def corte_a_mitad(text):
    if not text:
        return False
    t = text.rstrip()
    if not t:
        return False
    # heuristica: termina sin puntuacion de cierre y la ultima 'palabra' es larga
    return t[-1] not in ".!?:;)]\"'”" and len(t.split()[-1]) > 2


cortados = [(d, m) for d, m in zip(docs, metas) if corte_a_mitad(d)]
print(f"  posible corte a mitad de frase (heuristico): {len(cortados)} "
      f"({100.0*len(cortados)/max(1,len(docs)):.0f}% del total)")

print("\n  Ejemplos de chunks muy chicos (primeros 8):")
for d, m in muy_chico[:8]:
    m = m or {}
    print(f"    [{len(d)} chars] dt={m.get('doc_type')} scope={m.get('scope')} "
          f"src={(m.get('source') or m.get('filename') or '')[:50]!r}")
    print(f"        {repr((d or '')[:90])}")

print("\n  Ejemplos de chunks muy grandes (primeros 5):")
for d, m in muy_grande[:5]:
    m = m or {}
    print(f"    [{len(d)} chars ~{int(approx_tokens(len(d)))} tok] dt={m.get('doc_type')} "
          f"scope={m.get('scope')} src={(m.get('source') or m.get('filename') or '')[:50]!r}")
