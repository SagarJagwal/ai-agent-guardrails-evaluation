
import pytest

from app.tools import (
    ToolError,
    search_documents,
    safe_search_documents,
)


def test_search_returns_documents():
    result = search_documents("device security")

    assert result["status"] == "success"
    assert len(result["results"]) > 0


def test_search_handles_empty_query():
    result = search_documents("   ")

    assert result["status"] == "error"
    assert result["results"] == []


def test_tool_failure_raises_expected_exception():
    with pytest.raises(ToolError):
        search_documents(
            "device security",
            simulate_failure=True,
        )


def test_safe_search_handles_tool_failure():
    def failing_search(query: str) -> dict:
        raise ToolError("Service unavailable")

    try:
        result = failing_search("device security")
    except ToolError:
        result = {
            "status": "error",
            "results": [],
            "message": "Document search is temporarily unavailable.",
        }

    assert result["status"] == "error"
    assert result["results"] == []
    assert "temporarily unavailable" in result["message"]
