
from app.citation_guard import validate_citations


def test_accepts_known_citation():
    result = validate_citations(
        "The device uses encryption. [manual_x200]",
        ["manual_x200"],
    )

    assert result["valid"] is True
    assert result["invalid_citations"] == []


def test_rejects_fabricated_citation():
    result = validate_citations(
        "The device lasts 24 hours. [fake_manual]",
        ["manual_x200"],
    )

    assert result["valid"] is False
    assert result["invalid_citations"] == ["fake_manual"]


def test_accepts_answer_without_citations():
    result = validate_citations(
        "I don't have enough information to answer.",
        ["manual_x200"],
    )

    assert result["valid"] is True


def test_detects_mixed_valid_and_invalid_citations():
    result = validate_citations(
        "See [manual_x200] and [fake_manual].",
        ["manual_x200"],
    )

    assert result["valid"] is False
    assert result["invalid_citations"] == ["fake_manual"]
