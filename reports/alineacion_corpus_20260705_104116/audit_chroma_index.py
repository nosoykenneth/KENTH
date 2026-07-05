from __future__ import annotations

import collections
import json
import os
import sys
from pathlib import Path


def norm_path(value):
    if value is None:
        return ""
    p = str(value).replace("\\", "/").strip()
    for prefix in ("/app/", "./", "tesis-rag/"):
        if p.startswith(prefix):
            p = p[len(prefix):]
    return p


def is_truthy_false(value):
    if value is None:
        return False
    return str(value).strip().lower() in {"0", "false", "no", "off", "f", "n", "null", "none", "nil", ""}


def main():
    expected_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/CANONICAL_EXPECTED.json")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    indexable = set(norm_path(p) for p in expected.get("indexable_paths", []))
    excluded = set(norm_path(p) for p in expected.get("excluded_paths", []))
    deleted = set(norm_path(p) for p in expected.get("deleted_paths", []))

    import chromadb

    chroma_dir = os.getenv("CHROMA_DIR") or "/app/bd_vectorial"
    client = chromadb.PersistentClient(path=chroma_dir)
    cols = client.list_collections()
    if not cols:
        out = {"chroma_dir": chroma_dir, "collections": [], "total_chunks": 0}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    collection_names = [getattr(c, "name", str(c)) for c in cols]
    collection = client.get_collection(collection_names[0])
    total = collection.count()

    ids = []
    metas = []
    step = 1000
    for offset in range(0, total, step):
        batch = collection.get(limit=step, offset=offset, include=["metadatas"])
        ids.extend(batch.get("ids") or [])
        metas.extend(batch.get("metadatas") or [])

    by_course = collections.Counter()
    by_section_number = collections.Counter()
    by_moodle_section_id = collections.Counter()
    by_lesson_id = collections.Counter()
    by_source_type = collections.Counter()
    by_corpus_version = collections.Counter()
    by_source_path = collections.Counter()
    source_meta_values = collections.defaultdict(lambda: collections.defaultdict(set))
    source_hash_paths = collections.defaultdict(set)

    violations = {
        "allowed_for_indexing_false": [],
        "visible_to_student_false": [],
        "axis_id": [],
        "scope_axis": [],
        "evaluation_prompt": [],
        "qa": [],
        "operational_manifest": [],
        "resource_manifest_chunks": [],
        "report": [],
        "external_resources_suggested": [],
        "root_corpus": [],
        "deleted_local_paths": [],
        "excluded_paths": [],
        "canonical_source_not_expected": [],
        "pending_or_hold": [],
    }

    for i, meta in enumerate(metas):
        m = meta or {}
        source_path = norm_path(m.get("source_path") or m.get("source") or "")
        source_type = str(m.get("source_type") or m.get("source") or "").strip()
        scope = str(m.get("scope") or "").strip().lower()
        status = str(m.get("status") or "").strip().lower()
        row_ref = {"i": i, "id": ids[i] if i < len(ids) else "", "source_path": source_path, "source_type": source_type, "scope": scope, "status": status}

        by_course[str(m.get("course_id") or "") or "<empty>"] += 1
        by_section_number[str(m.get("section_number") or "") or "<empty>"] += 1
        by_moodle_section_id[str(m.get("moodle_section_id") or m.get("section_id") or "") or "<empty>"] += 1
        by_lesson_id[str(m.get("lesson_id") or "") or "<empty>"] += 1
        by_source_type[source_type or "<empty>"] += 1
        by_corpus_version[str(m.get("corpus_version") or "") or "<empty>"] += 1
        by_source_path[source_path or "<empty>"] += 1

        for key in ("course_id", "moodle_section_id", "section_number", "lesson_id", "source_type", "visible_to_student", "allowed_for_indexing", "internal_context", "corpus_version", "scope", "status"):
            if m.get(key) is not None:
                source_meta_values[source_path][key].add(str(m.get(key)))
        if m.get("source_hash"):
            source_hash_paths[str(m.get("source_hash"))].add(source_path)

        low = source_path.lower()
        if is_truthy_false(m.get("allowed_for_indexing")):
            violations["allowed_for_indexing_false"].append(row_ref)
        if is_truthy_false(m.get("visible_to_student")):
            violations["visible_to_student_false"].append(row_ref)
        if str(m.get("axis_id") or "").strip():
            violations["axis_id"].append(row_ref)
        if scope == "axis":
            violations["scope_axis"].append(row_ref)
        if "prompt_evaluacion" in low or source_type == "evaluation_prompt":
            violations["evaluation_prompt"].append(row_ref)
        if "qa_corpus" in low or source_type == "qa_report":
            violations["qa"].append(row_ref)
        if "00_manifest_indexacion" in low or source_type == "operational_manifest":
            violations["operational_manifest"].append(row_ref)
        if source_type == "resource_manifest":
            violations["resource_manifest_chunks"].append(row_ref)
        if low.startswith("reports/") or "/reports/" in low:
            violations["report"].append(row_ref)
        if "recursos_externos_sugeridos" in low:
            violations["external_resources_suggested"].append(row_ref)
        if low.startswith("corpus/") or "/corpus/" in low:
            violations["root_corpus"].append(row_ref)
        if source_path in deleted:
            violations["deleted_local_paths"].append(row_ref)
        if source_path in excluded or "/no_indexar/" in low or low.startswith("documentos/no_indexar/"):
            violations["excluded_paths"].append(row_ref)
        if source_path.startswith("documentos/") and source_path not in indexable:
            violations["canonical_source_not_expected"].append(row_ref)
        if "pending" in status or status == "hold":
            violations["pending_or_hold"].append(row_ref)

    chroma_sources = set(p for p in by_source_path if p and p != "<empty>")
    missing = sorted(indexable - chroma_sources)
    extra_canonical = sorted(p for p in chroma_sources if p.startswith("documentos/") and p not in indexable)

    diff_table = []
    for p in sorted(indexable):
        found = by_source_path.get(p, 0)
        diff_table.append({"source_path": p, "expected": True, "found_chunks": found, "status": "OK_INDEXED" if found else "MISSING_FROM_CHROMA"})
    for p in extra_canonical:
        if p in deleted:
            status = "STALE_IN_CHROMA"
        elif p in excluded or "/no_indexar/" in p or p.startswith("documentos/no_indexar/"):
            status = "EXCLUDED_BUT_INDEXED"
        else:
            status = "SHOULD_NOT_EXIST"
        diff_table.append({"source_path": p, "expected": False, "found_chunks": by_source_path[p], "status": status})

    duplicate_hashes = {h: sorted(paths) for h, paths in source_hash_paths.items() if len(paths) > 1}
    metadata_mismatch = {
        p: {k: sorted(v) for k, v in values.items() if len(v) > 1}
        for p, values in source_meta_values.items()
    }
    metadata_mismatch = {p: v for p, v in metadata_mismatch.items() if v}

    out = {
        "chroma_dir": chroma_dir,
        "collection": collection_names[0],
        "collections": collection_names,
        "total_chunks": total,
        "unique_sources": len(chroma_sources),
        "counts": {
            "by_course_id": dict(by_course),
            "by_section_number": dict(by_section_number),
            "by_moodle_section_id": dict(by_moodle_section_id),
            "by_lesson_id": dict(by_lesson_id),
            "by_source_type": dict(by_source_type),
            "by_corpus_version": dict(by_corpus_version),
            "by_source_path": dict(by_source_path),
        },
        "violations": violations,
        "violation_counts": {k: len(v) for k, v in violations.items()},
        "missing_indexables": missing,
        "extra_canonical_sources": extra_canonical,
        "duplicate_hashes": duplicate_hashes,
        "metadata_mismatch": metadata_mismatch,
        "diff_table": diff_table,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())