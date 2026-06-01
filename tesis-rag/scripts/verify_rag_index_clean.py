import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import chromadb

from config import CHROMA_DIR


PROHIBITED_PATTERNS = (
    r"(^|[/\\])paquetes_limpios([/\\]|$)",
    r"02_paquete_limpio\.md$",
    r".*_paquete_limpio\.md$",
    r".*paquete_limpio.*",
    r".*paquete.*limpio.*",
    r"auditoria_forense_autoria_rabinovich\.md$",
    r".*dossier_fuente.*",
    r".*fuente_protegida.*",
    r".*transcripci[oó]n.*cruda.*",
    r".*transcripci[oó]n.*corregida.*",
    r".*backup.*",
    r".*\.bak.*",
    r".*log.*",
    r".*debug.*",
    r".*tmp.*",
    r".*temp.*",
)


def _is_prohibited(value: str) -> bool:
    text = (value or "").replace("\\", "/").lower()
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in PROHIBITED_PATTERNS)


def main() -> int:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    violations = []
    total_chunks = 0
    sources = set()

    for collection in client.list_collections():
        data = collection.get(include=["metadatas"])
        metadatas = data.get("metadatas") or []
        total_chunks += len(metadatas)

        for meta in metadatas:
            if not meta:
                continue
            checked_values = [
                meta.get("source", ""),
                meta.get("filename", ""),
                meta.get("layer", ""),
                meta.get("capa", ""),
                meta.get("doc_type", ""),
            ]
            source = meta.get("source", "")
            if source:
                sources.add(source)
            if any(_is_prohibited(value) for value in checked_values):
                violations.append(
                    {
                        "collection": collection.name,
                        "source": source,
                        "filename": meta.get("filename", ""),
                        "layer": meta.get("layer", ""),
                        "doc_type": meta.get("doc_type", ""),
                    }
                )

    print(f"[VERIFY] Chroma dir: {CHROMA_DIR}")
    print(f"[VERIFY] Chunks revisados: {total_chunks}")
    print(f"[VERIFY] Fuentes unicas: {len(sources)}")

    if violations:
        print("[VERIFY][FAIL] Se encontraron fuentes prohibidas en el indice:")
        for item in violations[:50]:
            print(
                " - "
                f"{item['source']} | filename={item['filename']} "
                f"layer={item['layer']} doc_type={item['doc_type']}"
            )
        if len(violations) > 50:
            print(f" - ... {len(violations) - 50} violaciones adicionales")
        return 1

    print("[VERIFY][OK] Indice limpio: no hay paquetes limpios ni patrones prohibidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
