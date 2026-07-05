from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main():
    stale_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/STALE_SOURCES.json")
    stale = json.loads(stale_path.read_text(encoding="utf-8"))
    import chromadb
    chroma_dir = os.getenv("CHROMA_DIR") or "/app/bd_vectorial"
    client = chromadb.PersistentClient(path=chroma_dir)
    cols = client.list_collections()
    if not cols:
        raise SystemExit("No hay colecciones Chroma")
    name = getattr(cols[0], "name", str(cols[0]))
    collection = client.get_collection(name)
    before_total = collection.count()
    details = []
    for source_path in stale:
        before = collection.get(where={"source_path": source_path}, include=["metadatas"])
        before_legacy = collection.get(where={"source": source_path}, include=["metadatas"])
        count_before = len(before.get("ids") or [])
        count_legacy_before = len(before_legacy.get("ids") or [])
        if count_before:
            collection.delete(where={"source_path": source_path})
        if count_legacy_before:
            collection.delete(where={"source": source_path})
        after = collection.get(where={"source_path": source_path}, include=["metadatas"])
        after_legacy = collection.get(where={"source": source_path}, include=["metadatas"])
        details.append({
            "source_path": source_path,
            "source_path_chunks_before": count_before,
            "legacy_source_chunks_before": count_legacy_before,
            "source_path_chunks_after": len(after.get("ids") or []),
            "legacy_source_chunks_after": len(after_legacy.get("ids") or []),
        })
    after_total = collection.count()
    result = {
        "chroma_dir": chroma_dir,
        "collection": name,
        "before_total": before_total,
        "after_total": after_total,
        "removed_total_delta": before_total - after_total,
        "details": details,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())