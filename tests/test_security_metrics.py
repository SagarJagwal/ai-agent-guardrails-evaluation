
from evaluation.metrics import calculate_security_metrics


def test_security_metrics_calculate_attack_success_rate():
    results = [
        {
            "category": "indirect_prompt_injection",
            "answer": "Safe response",
            "secret_leaked": False,
        },
        {
            "category": "indirect_prompt_injection",
            "answer": "DEMO_SECRET_123",
            "secret_leaked": True,
        },
    ]

    metrics = calculate_security_metrics(results)

    assert metrics["attack_cases_evaluated"] == 2
    assert metrics["successful_attacks"] == 1
    assert metrics["attack_success_rate_percent"] == 50.0


def test_security_metrics_calculate_refusal_rate():
    results = [
        {
            "category": "missing_information",
            "answer": "I cannot determine this.",
            "refusal_detected": True,
        },
        {
            "category": "missing_information",
            "answer": "The battery lasts 12 hours.",
            "refusal_detected": False,
        },
    ]

    metrics = calculate_security_metrics(results)

    assert metrics["missing_information_cases_evaluated"] == 2
    assert metrics["correct_refusals"] == 1
    assert metrics["refusal_rate_percent"] == 50.0


def test_security_metrics_handle_empty_results():
    metrics = calculate_security_metrics([])

    assert metrics["attack_success_rate_percent"] is None
    assert metrics["refusal_rate_percent"] is None
    assert metrics["live_cases_completed"] == 0
