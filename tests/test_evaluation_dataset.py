
import json
from pathlib import Path


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "datasets"
    / "security_eval.json"
)

REQUIRED_CATEGORIES = {
    "normal_question",
    "indirect_prompt_injection",
    "missing_information",
    "citation_validation",
}


def load_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_dataset_is_valid_json_list():
    cases = load_dataset()

    assert isinstance(cases, list)
    assert len(cases) >= 8


def test_each_case_has_required_fields():
    for case in load_dataset():
        assert case["id"]
        assert case["category"]
        assert case["question"]
        assert isinstance(case["documents"], list)
        assert case["expected_behavior"]
        assert isinstance(case["expected_source_ids"], list)


def test_all_required_categories_are_present():
    categories = {
        case["category"] for case in load_dataset()
    }

    assert REQUIRED_CATEGORIES.issubset(categories)


def test_case_ids_are_unique():
    ids = [case["id"] for case in load_dataset()]

    assert len(ids) == len(set(ids))


def test_document_source_ids_are_valid():
    for case in load_dataset():
        source_ids = {
            doc["source_id"] for doc in case["documents"]
        }

        assert all(
            source_id in source_ids
            for source_id in case["expected_source_ids"]
        )
