from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evaluation.eval_utils import (  # noqa: E402
    DEFAULT_DATASET,
    compact_result,
    invoke_agent,
    load_dataset,
    write_report,
)
from services.agent_service import super_agente  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(description="Run a lightweight RAG agent evaluation.")
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET),
        help="Path to a JSON evaluation dataset.",
    )
    parser.add_argument(
        "--strict-exit",
        action="store_true",
        help="Exit with code 1 when any evaluation case fails.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    dataset_path = Path(args.dataset).resolve()
    dataset = load_dataset(dataset_path)

    results = []
    for index, item in enumerate(dataset, start=1):
        question = item["question"]
        print(f"[{index}/{len(dataset)}] {item.get('id', '')}: {question}")
        try:
            raw_result, duration_ms, logs = invoke_agent(super_agente, question)
            result = compact_result(item, raw_result, duration_ms, logs)
        except Exception as exc:
            result = {
                "id": item.get("id"),
                "question": question,
                "category": item.get("category", "uncategorized"),
                "pass": False,
                "checks": [{
                    "name": "runtime_error",
                    "pass": False,
                    "expected": "no exception",
                    "actual": repr(exc),
                }],
                "duration_ms": None,
                "route": None,
                "intent": None,
                "answer_type": None,
                "evidence_level": None,
                "source_count": 0,
                "warnings": [],
                "answer": "",
                "sources": [],
                "logs_excerpt": "",
                "notes": item.get("notes", ""),
            }
        results.append(result)
        status = "PASS" if result["pass"] else "FAIL"
        print(
            f"  {status} route={result.get('route')} "
            f"intent={result.get('intent')} answer_type={result.get('answer_type')} "
            f"sources={result.get('source_count')} duration_ms={result.get('duration_ms')}"
        )

    report_path, payload = write_report(dataset_path, results)

    # --- Global summary ---
    summary = payload["summary"]
    print("\n" + "=" * 60)
    print("RESUMEN GLOBAL")
    print("=" * 60)
    print(f"  total:     {summary['total']}")
    print(f"  passed:    {summary['passed']}")
    print(f"  failed:    {summary['failed']}")
    print(f"  pass_rate: {summary['pass_rate']}")

    # --- Per-category summary ---
    by_cat = payload["summary_by_category"]
    print("\n" + "-" * 60)
    print("RESUMEN POR CATEGORIA")
    print("-" * 60)
    for cat, cat_summary in by_cat.items():
        status_icon = "OK" if cat_summary["failed"] == 0 else "!!"
        print(
            f"  {status_icon} {cat:<25s}  "
            f"{cat_summary['passed']}/{cat_summary['total']}  "
            f"pass_rate={cat_summary['pass_rate']}"
        )

    # --- Failures ---
    failures = payload["failures"]
    if failures:
        print("\n" + "-" * 60)
        print("FALLOS DETECTADOS")
        print("-" * 60)
        for f in failures:
            print(f"  [{f['category']}] {f['id']}")
            print(f"    Q: {f['question']}")
            for c in f["failed_checks"]:
                print(f"    FAIL {c['name']}: expected={c['expected']}  actual={c['actual']}")
    else:
        print("\n  Sin fallos detectados.")

    print(f"\n  report: {report_path}")

    if args.strict_exit and summary["failed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
