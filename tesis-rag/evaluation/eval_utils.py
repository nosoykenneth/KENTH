from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path
import json
import time


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = PROJECT_ROOT / "evaluation" / "datasets" / "rag_eval_v2.json"
REPORTS_DIR = PROJECT_ROOT / "evaluation" / "reports"


def load_dataset(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def initial_state(question: str):
    return {
        "pregunta": question,
        "contexto_leccion": "",
        "historial": [],
        "imagen": "",
        "ruta": "",
        "respuesta_final": "",
        "evidencias": [],
        "evidence_level": "",
        "intent": "",
        "answer_type": "",
        "course_module": "",
        "evaluation_category": "",
        "requires_course_evidence": True,
        "warnings": [],
        "retrieved_chunks": [],
        "model_used": "",
        "prompt_id": "",
    }


def invoke_agent(agent, question: str):
    started = time.perf_counter()
    logs = StringIO()
    with redirect_stdout(logs):
        result = agent.invoke(initial_state(question))
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    return result, duration_ms, logs.getvalue()


def source_count(result: dict):
    return len(result.get("evidencias") or [])


def evaluate_expectations(item: dict, result: dict):
    checks = []
    route = result.get("ruta")
    intent = result.get("intent")
    answer_type = result.get("answer_type")
    answer = result.get("respuesta_final") or ""
    sources = source_count(result)

    def add(name: str, passed: bool, expected=None, actual=None):
        checks.append({
            "name": name,
            "pass": bool(passed),
            "expected": expected,
            "actual": actual,
        })

    if item.get("expected_route") is not None:
        add("expected_route", route == item["expected_route"], item["expected_route"], route)
    if item.get("expected_intent") is not None:
        add("expected_intent", intent == item["expected_intent"], item["expected_intent"], intent)
    if item.get("expected_answer_type") is not None:
        add(
            "expected_answer_type",
            answer_type == item["expected_answer_type"],
            item["expected_answer_type"],
            answer_type,
        )
    if item.get("should_block") is True:
        add(
            "should_block",
            route == "bloqueo" or answer_type == "out_of_domain",
            "bloqueo/out_of_domain",
            f"{route}/{answer_type}",
        )
    if item.get("should_clarify") is True:
        add(
            "should_clarify",
            answer_type in ("clarification", "needs_more_context"),
            "clarification|needs_more_context",
            answer_type,
        )
    if item.get("should_have_sources") is True:
        add("should_have_sources", sources > 0, "> 0", sources)
    if item.get("forbid_visible_source_label") is True:
        add("forbid_visible_source_label", "Fuente " not in answer, "no Fuente X", "Fuente " in answer)

    passed = all(check["pass"] for check in checks) if checks else True
    return passed, checks


def compact_result(item: dict, result: dict, duration_ms: float, logs: str):
    passed, checks = evaluate_expectations(item, result)
    answer = result.get("respuesta_final") or ""
    warnings = result.get("warnings") or []

    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "category": item.get("category", "uncategorized"),
        "pass": passed,
        "checks": checks,
        "duration_ms": duration_ms,
        "route": result.get("ruta"),
        "intent": result.get("intent"),
        "answer_type": result.get("answer_type"),
        "evidence_level": result.get("evidence_level"),
        "source_count": source_count(result),
        "warnings": warnings,
        "answer": answer,
        "sources": result.get("evidencias") or [],
        "logs_excerpt": logs[-2000:] if logs else "",
        "notes": item.get("notes", ""),
    }


def summarize(results: list):
    total = len(results)
    passed = sum(1 for item in results if item["pass"])
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total, 4) if total else 0,
    }


def summarize_by_category(results: list):
    """Return a dict keyed by category with pass/fail/total/pass_rate."""
    categories: dict[str, list] = {}
    for r in results:
        cat = r.get("category", "uncategorized")
        categories.setdefault(cat, []).append(r)
    summary = {}
    for cat, items in sorted(categories.items()):
        total = len(items)
        passed = sum(1 for i in items if i["pass"])
        failed = total - passed
        summary[cat] = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total, 4) if total else 0,
        }
    return summary


def summarize_failures(results: list):
    """Return a list of compact failure descriptors."""
    failures = []
    for r in results:
        if r["pass"]:
            continue
        failed_checks = [c for c in r.get("checks", []) if not c["pass"]]
        failures.append({
            "id": r["id"],
            "category": r.get("category", "uncategorized"),
            "question": r["question"],
            "failed_checks": [
                {"name": c["name"], "expected": c["expected"], "actual": c["actual"]}
                for c in failed_checks
            ],
        })
    return failures


def write_report(dataset_path: Path, results: list):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"rag_eval_report_{timestamp}.json"
    payload = {
        "dataset": str(dataset_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": summarize(results),
        "summary_by_category": summarize_by_category(results),
        "failures": summarize_failures(results),
        "results": results,
    }
    with report_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    return report_path, payload
