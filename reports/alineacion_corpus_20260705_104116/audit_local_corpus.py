from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESIS = ROOT / "tesis-rag"
DOCUMENTOS = TESIS / "documentos"
OUT = Path(__file__).resolve().parent

sys.path.insert(0, str(TESIS))
from ingest import es_documento_aprobado_para_indexar  # noqa: E402


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8", errors="replace").strip()


def parse_frontmatter(path: Path) -> tuple[bool, dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return False, {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False, {}
    meta: dict[str, str] = {}
    for raw in parts[1].splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip("'\"")
        meta[key.strip()] = value
    return True, meta


def as_boolish(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "si", "sí", "on", "t", "y"}:
        return True
    if text in {"0", "false", "no", "off", "f", "n", "null", "none", "nil", ""}:
        return False
    return None


def classify(path: Path, fm_ok: bool, meta: dict[str, str], gate_ok: bool, reasons: list[str]) -> str:
    rel = path.relative_to(TESIS).as_posix()
    lower = rel.lower()
    allowed = as_boolish(meta.get("allowed_for_indexing"))
    status = (meta.get("status") or "").lower()
    action = (meta.get("action") or "").lower()
    mapped_state = (meta.get("mapped_state") or "").lower()
    source_type = (meta.get("source_type") or "").lower()
    is_pedagogic_resource_manifest = (
        lower.endswith("/08_recursos_manifest.md")
        and source_type == "resource_manifest"
        and allowed is True
    )

    if "no_indexar/" in lower or "/no_indexar/" in lower:
        return "EXCLUDED_NO_INDEX"
    if not fm_ok:
        return "INVALID"
    if "prompt_evaluacion" in lower or source_type == "evaluation_prompt":
        return "EXCLUDED_EVALUATION" if not gate_ok else "INVALID"
    if any(token in lower for token in ("qa_corpus", "plan_ingesta", "recursos_externos_sugeridos")):
        return "EXCLUDED_OPERATIONAL" if not gate_ok else "INVALID"
    if "manifest" in lower and not is_pedagogic_resource_manifest:
        return "EXCLUDED_OPERATIONAL" if not gate_ok else "INVALID"
    if lower.startswith("documentos/oficial/") and not lower.startswith("documentos/oficial/curso_"):
        return "EXCLUDED_OPERATIONAL" if not gate_ok else "INDEXABLE"
    if allowed is False:
        return "HOLD" if "pending" in action or "pending" in mapped_state or "pending" in status else "EXCLUDED_OPERATIONAL"
    if not gate_ok:
        return "INVALID"
    return "INDEXABLE"


def main() -> int:
    md_files = sorted(DOCUMENTOS.rglob("*.md"))
    deleted = [
        p for p in run_git(["ls-files", "-d"]).splitlines()
        if p.startswith("tesis-rag/documentos/")
    ]
    untracked = [
        p for p in run_git(["ls-files", "--others", "--exclude-standard"]).splitlines()
        if p.startswith("tesis-rag/documentos/")
    ]

    rows = []
    conflicts = defaultdict(list)
    for path in md_files:
        rel = path.relative_to(TESIS).as_posix()
        fm_ok, meta = parse_frontmatter(path)
        gate_ok, reasons, gate_meta = es_documento_aprobado_para_indexar(str(path), explicar=True)
        cls = classify(path, fm_ok, meta, bool(gate_ok), list(reasons))
        row = {
            "relative_path": rel,
            "frontmatter_valid": fm_ok,
            "course_id": meta.get("course_id", ""),
            "moodle_section_id": meta.get("moodle_section_id", ""),
            "section_number": meta.get("section_number", ""),
            "lesson_id": meta.get("lesson_id", ""),
            "source_type": meta.get("source_type", ""),
            "scope": meta.get("scope", meta.get("recommended_scope", "")),
            "recommended_scope": meta.get("recommended_scope", ""),
            "allowed_for_indexing": meta.get("allowed_for_indexing", ""),
            "visible_to_student": meta.get("visible_to_student", ""),
            "internal_context": meta.get("internal_context", ""),
            "status": meta.get("status", ""),
            "corpus_version": meta.get("corpus_version", ""),
            "ingestion_batch_id": meta.get("ingestion_batch_id", ""),
            "gate_ok": bool(gate_ok),
            "gate_reasons": list(reasons),
            "classification": cls,
        }
        text_lite = json.dumps(meta, ensure_ascii=False).lower() + "\n" + rel.lower()
        if "axis_id" in text_lite:
            conflicts["axis_id"].append(rel)
        if re.search(r"scope\s*[:=]\s*['\"]?axis", text_lite):
            conflicts["scope_axis"].append(rel)
        if not fm_ok:
            conflicts["missing_or_invalid_frontmatter"].append(rel)
        if meta.get("allowed_for_indexing") and as_boolish(meta.get("allowed_for_indexing")) is None:
            conflicts["allowed_for_indexing_ambiguous"].append(rel)
        if "prompt_evaluacion" in rel.lower() and gate_ok:
            conflicts["evaluation_prompt_indexable"].append(rel)
        if "qa_corpus" in rel.lower() and gate_ok:
            conflicts["qa_indexable"].append(rel)
        is_operational_manifest = ("00_manifest_indexacion" in rel.lower()) or ("ingest_manifest" in rel.lower()) or ("manifest_operativo" in rel.lower())
        if is_operational_manifest and gate_ok:
            conflicts["manifest_indexable"].append(rel)
        if "recursos_externos_sugeridos" in rel.lower() and gate_ok:
            conflicts["external_resources_indexable"].append(rel)
        rows.append(row)

    by_class = Counter(r["classification"] for r in rows)
    by_gate = Counter("gate_ok" if r["gate_ok"] else "gate_reject" for r in rows)
    sections = sorted({str(Path(r["relative_path"]).parts[3]) for r in rows if r["relative_path"].startswith("documentos/oficial/curso_2/") and len(Path(r["relative_path"]).parts) > 3})
    corpus_root_exists = (ROOT / "corpus").exists()

    report = {
        "root": str(ROOT),
        "documentos": str(DOCUMENTOS),
        "git": {
            "branch_status": run_git(["status", "-sb"]),
            "head": run_git(["rev-parse", "HEAD"]),
            "origin_main": run_git(["rev-parse", "origin/main"]),
            "last_commits": run_git(["log", "--oneline", "-5"]).splitlines(),
            "deleted_documentos": deleted,
            "untracked_documentos": untracked,
        },
        "corpus_root_exists": corpus_root_exists,
        "sections_detected": sections,
        "counts": {
            "markdown_files": len(rows),
            "by_classification": dict(by_class),
            "by_gate": dict(by_gate),
            "deleted_documentos": len(deleted),
            "untracked_documentos": len(untracked),
        },
        "conflicts": {k: v for k, v in conflicts.items()},
        "files": rows,
    }

    (OUT / "LOCAL_CANONICAL_AUDIT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Auditoria local del corpus canonico",
        "",
        f"- Root: `{ROOT}`",
        f"- Fuente canonica auditada: `{DOCUMENTOS}`",
        f"- Rama/estado: `{report['git']['branch_status'].splitlines()[0]}`",
        f"- HEAD local: `{report['git']['head']}`",
        f"- origin/main: `{report['git']['origin_main']}`",
        f"- `corpus/` raiz existe: `{corpus_root_exists}`",
        "",
        "## Resumen",
        f"- Markdown existentes auditados: {len(rows)}",
        f"- Borrados locales bajo `tesis-rag/documentos`: {len(deleted)}",
        f"- Untracked bajo `tesis-rag/documentos`: {len(untracked)}",
        "",
        "## Clasificacion",
    ]
    for k, v in sorted(by_class.items()):
        lines.append(f"- {k}: {v}")
    lines += ["", "## Gate oficial"]
    for k, v in sorted(by_gate.items()):
        lines.append(f"- {k}: {v}")
    lines += ["", "## Secciones detectadas en curso_2"]
    for s in sections:
        lines.append(f"- `{s}`")
    lines += ["", "## Conflictos"]
    if conflicts:
        for k, vals in sorted(conflicts.items()):
            lines.append(f"- {k}: {len(vals)}")
            for val in vals[:20]:
                lines.append(f"  - `{val}`")
    else:
        lines.append("- Sin conflictos duros detectados por el auditor local.")
    lines += ["", "## Borrados locales pendientes"]
    for p in deleted:
        lines.append(f"- `{p}`")
    lines += ["", "## Archivos indexables segun gate oficial"]
    for r in rows:
        if r["classification"] == "INDEXABLE":
            lines.append(f"- `{r['relative_path']}` | lesson=`{r['lesson_id']}` scope=`{r['scope']}` visible=`{r['visible_to_student']}` internal=`{r['internal_context']}`")

    (OUT / "LOCAL_CANONICAL_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


