from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
local_audit = json.loads((OUT / "LOCAL_CANONICAL_AUDIT.json").read_text(encoding="utf-8-sig"))
pre = json.loads((OUT / "CHROMA_PRE_AUDIT.json").read_text(encoding="utf-8-sig"))
server_status = (OUT / "SERVER_PRE_AUDIT.txt").read_text(encoding="utf-8-sig", errors="replace")
local_files = set((OUT / "LOCAL_DOCUMENTOS_FILES.txt").read_text(encoding="utf-8-sig").splitlines())
server_files = set((OUT / "SERVER_DOCUMENTOS_FILES.txt").read_text(encoding="utf-8-sig").splitlines())

# SERVER_PRE_AUDIT.md
status_lines = server_status.splitlines()
server_deleted = [line.strip()[2:] for line in status_lines if line.startswith(" D tesis-rag/documentos/")]
server_untracked = [line.strip()[3:] for line in status_lines if line.startswith("?? tesis-rag/documentos/")]
health_line = ""
for line in reversed(status_lines):
    if line.startswith("{") and '"status"' in line:
        health_line = line
        break
try:
    health = json.loads(health_line) if health_line else {}
except Exception:
    health = {}
server_md = [
    "# Auditoria previa del servidor",
    "",
    "## Resumen",
    f"- HEAD servidor: `c9f496c1402fc0d6983c03b020816356f424ef2f` (segun captura).",
    "- `origin/main`: coincide con HEAD en la captura.",
    f"- Worktree servidor limpio: `{len(server_deleted) == 0 and len(server_untracked) == 0}`.",
    f"- Borrados bajo `tesis-rag/documentos`: {len(server_deleted)}.",
    f"- Untracked bajo `tesis-rag/documentos`: {len(server_untracked)}.",
    f"- Health status: `{health.get('status', 'no_parseado')}`.",
    f"- Chroma health chunks: `{health.get('details', {}).get('chroma_chunks', 'no_parseado')}`.",
    f"- Ollama: `{health.get('ollama', 'no_parseado')}`; modelos: `{health.get('models', {})}`.",
    "",
    "## Hallazgo operativo",
    "El servidor esta sano para lectura, pero no esta limpio para una escritura de indice: conserva cambios locales sin commit en `tesis-rag/documentos` y reportes untracked. Por tanto cualquier correccion de Chroma debe tener backup previo y quedar documentada; un deploy por `git pull` no es suficiente mientras el worktree siga dirty.",
    "",
    "## Captura cruda",
    "```text",
    server_status.strip(),
    "```",
]
(OUT / "SERVER_PRE_AUDIT.md").write_text("\n".join(server_md) + "\n", encoding="utf-8")

# CHROMA_PRE_AUDIT.md
vc = pre.get("violation_counts", {})
counts = pre.get("counts", {})
stale_rows = [r for r in pre.get("diff_table", []) if r.get("status") == "STALE_IN_CHROMA"]
missing_rows = [r for r in pre.get("diff_table", []) if r.get("status") == "MISSING_FROM_CHROMA"]
excluded_rows = [r for r in pre.get("diff_table", []) if r.get("status") == "EXCLUDED_BUT_INDEXED"]
status_counts = Counter(r.get("status") for r in pre.get("diff_table", []))
chroma_md = [
    "# Chroma pre-audit",
    "",
    f"- Chroma dir: `{pre.get('chroma_dir')}`",
    f"- Coleccion: `{pre.get('collection')}`",
    f"- Total chunks: {pre.get('total_chunks')}",
    f"- Fuentes unicas: {pre.get('unique_sources')}",
    "",
    "## Distribucion",
    f"- Por course_id: `{counts.get('by_course_id', {})}`",
    f"- Por section_number: `{counts.get('by_section_number', {})}`",
    f"- Por moodle_section_id: `{counts.get('by_moodle_section_id', {})}`",
    f"- Por lesson_id: `{counts.get('by_lesson_id', {})}`",
    f"- Por source_type: `{counts.get('by_source_type', {})}`",
    f"- Por corpus_version: `{counts.get('by_corpus_version', {})}`",
    "",
    "## Controles de basura/stale",
]
for key in sorted(vc):
    chroma_md.append(f"- {key}: {vc[key]}")
chroma_md += ["", "## Estados corpus vs Chroma"]
for key, val in sorted(status_counts.items()):
    chroma_md.append(f"- {key}: {val}")
chroma_md += ["", "## Stale chunks detectados"]
if stale_rows:
    for r in stale_rows:
        chroma_md.append(f"- `{r['source_path']}` -> {r['found_chunks']} chunks")
else:
    chroma_md.append("- 0")
chroma_md += ["", "## Faltantes aprobados"]
if missing_rows:
    for r in missing_rows:
        chroma_md.append(f"- `{r['source_path']}`")
else:
    chroma_md.append("- 0")
chroma_md += ["", "## Excluidos indexados"]
if excluded_rows:
    for r in excluded_rows:
        chroma_md.append(f"- `{r['source_path']}` -> {r['found_chunks']} chunks")
else:
    chroma_md.append("- 0")
(OUT / "CHROMA_PRE_AUDIT.md").write_text("\n".join(chroma_md) + "\n", encoding="utf-8")

# CORPUS_VS_CHROMA_DIFF.md
corpus_md = [
    "# Diff corpus canonico vs Chroma",
    "",
    "| Archivo canonico / fuente Chroma | Esperado en Chroma | Encontrado chunks | Estado |",
    "|---|---:|---:|---|",
]
for r in pre.get("diff_table", []):
    corpus_md.append(f"| `{r['source_path']}` | {str(r['expected']).lower()} | {r['found_chunks']} | {r['status']} |")
corpus_md += [
    "",
    "## Resumen",
    f"- OK_INDEXED: {status_counts.get('OK_INDEXED', 0)} archivos.",
    f"- MISSING_FROM_CHROMA: {status_counts.get('MISSING_FROM_CHROMA', 0)} archivos.",
    f"- STALE_IN_CHROMA: {status_counts.get('STALE_IN_CHROMA', 0)} fuentes, {vc.get('deleted_local_paths', 0)} chunks.",
    f"- EXCLUDED_BUT_INDEXED: {status_counts.get('EXCLUDED_BUT_INDEXED', 0)} fuentes.",
    f"- axis_id/scope=axis: {vc.get('axis_id', 0)}/{vc.get('scope_axis', 0)} chunks.",
    f"- prompts evaluacion/QA/manifests operativos/reportes/corpus raiz: {vc.get('evaluation_prompt', 0)}/{vc.get('qa', 0)}/{vc.get('operational_manifest', 0)}/{vc.get('report', 0)}/{vc.get('root_corpus', 0)} chunks.",
]
(OUT / "CORPUS_VS_CHROMA_DIFF.md").write_text("\n".join(corpus_md) + "\n", encoding="utf-8")

# LOCAL_SERVER_DIFF.md
only_local = sorted(local_files - server_files)
only_server = sorted(server_files - local_files)
local_deleted = [p.replace("tesis-rag/", "") for p in local_audit["git"]["deleted_documentos"]]
local_server_md = [
    "# Diff local/main/servidor",
    "",
    "## Estado Git local",
    f"- Branch/status: `{local_audit['git']['branch_status'].splitlines()[0]}`",
    f"- HEAD local: `{local_audit['git']['head']}`",
    f"- origin/main local: `{local_audit['git']['origin_main']}`",
    f"- local HEAD == origin/main: `{local_audit['git']['head'] == local_audit['git']['origin_main']}`",
    f"- Borrados locales bajo documentos: {len(local_deleted)}.",
    "",
    "## Estado servidor",
    "- HEAD servidor == origin/main: `true` segun captura.",
    f"- Worktree servidor limpio: `{len(server_deleted) == 0 and len(server_untracked) == 0}`.",
    f"- Borrados servidor bajo documentos: {len(server_deleted)}.",
    f"- Untracked servidor bajo documentos: {len(server_untracked)}.",
    "",
    "## Comparacion filesystem local vs servidor",
    f"- Archivos presentes solo local: {len(only_local)}.",
    f"- Archivos presentes solo servidor: {len(only_server)}.",
    "",
    "### Solo local",
]
local_server_md += [f"- `{p}`" for p in only_local[:100]] or ["- 0"]
local_server_md += ["", "### Solo servidor"]
local_server_md += [f"- `{p}`" for p in only_server[:100]] or ["- 0"]
local_server_md += ["", "## Borrados locales relevantes para Chroma"]
for p in local_deleted:
    local_server_md.append(f"- `{p}`")
local_server_md += ["", "## Conclusion"]
local_server_md.append("Hay drift: local/main no incorporan todavia los borrados locales del usuario, el servidor esta dirty con un conjunto distinto de borrados, y Chroma conserva 7 fuentes canonicas eliminadas localmente. No se puede declarar alineado sin limpiar Chroma y normalizar el estado Git/servidor.")
(OUT / "LOCAL_SERVER_DIFF.md").write_text("\n".join(local_server_md) + "\n", encoding="utf-8")

print(json.dumps({
    "total_chunks": pre.get("total_chunks"),
    "ok_indexed": status_counts.get("OK_INDEXED", 0),
    "stale_sources": status_counts.get("STALE_IN_CHROMA", 0),
    "stale_chunks": vc.get("deleted_local_paths", 0),
    "missing": status_counts.get("MISSING_FROM_CHROMA", 0),
    "server_deleted": len(server_deleted),
    "only_server": len(only_server),
}, indent=2))