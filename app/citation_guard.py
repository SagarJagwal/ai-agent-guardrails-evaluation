
import re


def validate_citations(
    answer: str,
    allowed_source_ids: list[str],
) -> dict:
    """Reject citations that refer to unknown source IDs."""

    citations = re.findall(
        r"\[([A-Za-z0-9_-]+)\]",
        answer,
    )

    invalid = [
        citation
        for citation in citations
        if citation not in allowed_source_ids
    ]

    return {
        "valid": len(invalid) == 0,
        "citations_found": citations,
        "invalid_citations": invalid,
    }
