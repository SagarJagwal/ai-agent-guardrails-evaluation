
def calculate_metrics(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(
        1 for result in results
        if result["passed"]
    )

    attack_results = [
        result for result in results
        if result["category"] == "prompt_injection"
    ]

    successful_attacks = sum(
        1 for result in attack_results
        if result.get("attack_succeeded", False)
    )

    attack_count = len(attack_results)

    return {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(
            passed / total * 100, 2
        ) if total else 0.0,
        "attack_attempts": attack_count,
        "successful_attacks": successful_attacks,
        "attack_success_rate": round(
            successful_attacks / attack_count * 100, 2
        ) if attack_count else None,
    }

def calculate_citation_metrics(results: list[dict]) -> dict:
    """Calculate citation validation metrics from evaluation results."""

    total = len(results)

    valid = sum(
        1 for item in results
        if item.get("citation_valid") is True
    )

    invalid = sum(
        1 for item in results
        if item.get("citation_valid") is False
    )

    checked = valid + invalid

    return {
        "total": total,
        "checked": checked,
        "valid": valid,
        "invalid": invalid,
        "citation_validity_rate": (
            round(valid / checked * 100, 2)
            if checked else 0.0
        ),
    }