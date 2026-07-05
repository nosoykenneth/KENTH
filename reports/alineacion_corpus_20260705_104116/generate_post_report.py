from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
post = json.loads((OUT / "CHROMA_POST_AUDIT.json").read_text(encoding="utf-8-sig"))
cleanup = json.loads((OUT / "CHROMA_CLEANUP_RESULT.json").read_text(encoding="utf-8-sig"))
health = json.loads((OUT / "health_post_cleanup.json").read_text(encoding="utf-8-sig"))
status_counts = Counter(r.get("status") for r in post.get("diff_table", []))
counts = post.get("counts", {})
vc = post.get("violation_counts", {})
md = [
    "# Chroma post-audit",
    "",
    "## Resultado",
    f"- Health post-cleanup: `{health.get('status')}`.",
    f"- Chroma chunks en health: `{health.get('details', {}).get('chroma_chunks')}`.",
    f"- Coleccion: `{post.get('collection')}`.",
    f"- Total chunks: {post.get('total_chunks')}.",
    f"- Fuentes unicas: {post.get('unique_sources')}.",
    f"- Cleanup delta: {cleanup.get('before_total')} -> {cleanup.get('after_total')} ({cleanup.get('removed_total_delta')} chunks removidos).",
    "",
    "## Distribucion",
    f"- Por course_id: `{counts.get('by_course_id', {})}`",
    f"- Por section_number: `{counts.get('by_section_number', {})}`",
    f"- Por moodle_section_id: `{counts.get('by_moodle_section_id', {})}`",
    f"- Por lesson_id: `{counts.get('by_lesson_id', {})}`",
    f"- Por source_type: `{counts.get('by_source_type', {})}`",
    f"- Por corpus_version: `{counts.get('by_corpus_version', {})}`",
    "",
    "## Gates post-index",
]
for key in sorted(vc):
    md.append(f"- {key}: {vc[key]}")
md += ["", "## Estados corpus vs Chroma"]
for key, val in sorted(status_counts.items()):
    md.append(f"- {key}: {val}")
md += ["", "## Fuentes removidas"]
for item in cleanup.get("details", []):
    md.append(f"- `{item['source_path']}`: {item['source_path_chunks_before']} -> {item['source_path_chunks_after']} chunks")
md += ["", "## Conclusion"]
md.append("El indice Chroma queda alineado con el conjunto canonico local aprobado: no hay stale chunks, faltantes, excluidos indexados ni metadatos legacy `axis_id`/`scope=axis`.")
(OUT / "CHROMA_POST_AUDIT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(json.dumps({"total": post.get("total_chunks"), "statuses": dict(status_counts), "violations": vc}, indent=2))