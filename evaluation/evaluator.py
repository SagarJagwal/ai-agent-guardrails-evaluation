
import json
from pathlib import Path
from datetime import datetime, timezone


def build_report(pytest_json_path: str = "reports/pytest_results.json") -> dict:
    """Build evaluation metrics from actual pytest execution results."""

    source = Path(pytest_json_path)

    if not source.exists():
        raise FileNotFoundError(
            f"Pytest report not found: {source}. "
            "Run pytest with --json-report first."
        )

    data = json.loads(source.read_text(encoding="utf-8"))
    summary = data.get("summary", {})

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    errors = summary.get("error", 0)
    skipped = summary.get("skipped", 0)

    tests = []

    for test in data.get("tests", []):
        outcome = test.get("outcome", "unknown")
        tests.append({
            "test_id": test.get("nodeid", "unknown"),
            "category": (
                test.get("nodeid", "").split("::")[-1]
            ),
            "outcome": outcome,
            "passed": outcome == "passed",
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "pass_rate": round(passed / total * 100, 2)
            if total else 0.0,
        },
        "results": tests,
    }


def save_report(report: dict, output_path: str = "reports/evaluation_report.json") -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    report = build_report()
    save_report(report)
    print(json.dumps(report["metrics"], indent=2))
