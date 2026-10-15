
from app.guardrails import (
    validate_answer_grounding,
    validate_citation_mapping,
)


def test_supported_answer_passes():
    answer = "The device uses encrypted communication."
    sources = [
        "The device uses encrypted communication."
    ]

    assert validate_answer_grounding(answer, sources)


def test_unsupported_answer_fails():
    answer = "The device lasts 72 hours."
    sources = [
        "The device uses encrypted communication."
    ]

    assert not validate_answer_grounding(answer, sources)


def test_valid_citation_mapping_passes():
    citations = ["manual_x200"]
    citation_map = {
        "manual_x200": "Section 3: Device security"
    }

    assert validate_citation_mapping(citations, citation_map)


def test_unknown_citation_fails():
    citations = ["fake_manual"]
    citation_map = {
        "manual_x200": "Section 3: Device security"
    }

    assert not validate_citation_mapping(citations, citation_map)


def test_empty_citations_fail():
    assert not validate_citation_mapping(
        [],
        {"manual_x200": "Section 3: Device security"},
    )
