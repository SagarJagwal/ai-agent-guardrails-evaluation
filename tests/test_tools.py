
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
    try:
        search_documents("security", simulate_failure=True)
    except ToolError:
        pass
    else:
        assert False, "Expected ToolError"


def test_safe_search_recovers_from_tool_exception():
    def failing_tool(query):
        raise ToolError("Service unavailable")

    result = safe_search_documents(
        "device security",
        search_fn=failing_tool,
    )

    assert result["status"] == "error"
    assert result["results"] == []
    assert "temporarily unavailable" in result["message"]


def test_safe_search_recovers_from_timeout():
    def timeout_tool(query):
        raise TimeoutError("Request timed out")

    result = safe_search_documents(
        "device security",
        search_fn=timeout_tool,
    )

    assert result["status"] == "error"
    assert result["results"] == []


def test_safe_search_rejects_malformed_response():
    def malformed_tool(query):
        return {"status": "success", "results": "not-a-list"}

    result = safe_search_documents(
        "device security",
        search_fn=malformed_tool,
    )

    assert result["status"] == "error"
    assert result["results"] == []


def test_safe_search_accepts_valid_response():
    result = safe_search_documents("device security")

    assert result["status"] == "success"
    assert result["results"][0]["source_id"] == "manual_x200"
