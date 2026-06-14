"""Audita metadata RAG legacy de ejes frente a moodle_section_id.

No modifica Chroma ni la base. Sirve como preflight antes de un reindex completo.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import db_service


def audit_course_documents(course_id: str = "") -> dict:
    docs = db_service.list_documents(course_id=course_id or None)
    counts = Counter()
    examples = {"legacy_axis": [], "with_section": [], "missing_section": []}
    for doc in docs:
        has_axis = bool(str(doc.get("axis_id") or "").strip())
        has_section = bool(str(doc.get("moodle_section_id") or "").strip())
        if has_section:
            counts["with_section"] += 1
            if len(examples["with_section"]) < 5:
                examples["with_section"].append(doc.get("doc_id"))
        elif has_axis:
            counts["legacy_axis"] += 1
            if len(examples["legacy_axis"]) < 5:
                examples["legacy_axis"].append(doc.get("doc_id"))
        else:
            counts["missing_section"] += 1
            if len(examples["missing_section"]) < 5:
                examples["missing_section"].append(doc.get("doc_id"))
    return {"documents": dict(counts), "examples": examples}


def main() -> int:
    course_id = sys.argv[1] if len(sys.argv) > 1 else ""
    report = audit_course_documents(course_id)
    report["recommendation"] = (
        "Reindexar curso completo cuando legacy_axis o missing_section sean mayores que cero."
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
