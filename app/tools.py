
from collections.abc import Callable
from typing import Any


class ToolError(Exception):
    """Raised when an agent tool fails."""


def search_documents(
    query: str,
    simulate_failure: bool = False,
) -> dict[str, Any]:
    """Mock document-search tool."""

    if simulate_failure:
        raise ToolError("Document search service unavailable.")

    if not query.strip():
        return {
            "status": "error",
            "results": [],
            "message": "Search query cannot be empty.",
        }

    return {
        "status": "success",
        "results": [
            {
                "source_id": "manual_x200",
                "text": "The device uses encrypted communication.",
            }
        ],
        "message": None,
    }


def safe_search_documents(
    query: str,
    search_fn: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Execute search and recover safely from tool failures."""

    tool = search_fn or search_documents

    try:
        result = tool(query)

        # Validate the tool response before trusting it.
        if not isinstance(result, dict):
            raise ToolError("Invalid tool response format.")

        if result.get("status") == "error":
            return {
                "status": "error",
                "results": [],
                "message": "Document search could not be completed.",
            }

        if result.get("status") != "success":
            raise ToolError("Unexpected tool status.")

        if not isinstance(result.get("results"), list):
            raise ToolError("Invalid search results.")

        for item in result["results"]:
            if not isinstance(item, dict):
                raise ToolError("Invalid search result item.")

            if not isinstance(item.get("source_id"), str):
                raise ToolError("Missing source ID.")

            if not isinstance(item.get("text"), str):
                raise ToolError("Missing source text.")

        return result

    except Exception:
        # Fail closed: do not fabricate documents after tool failure.
        return {
            "status": "error",
            "results": [],
            "message": "Document search is temporarily unavailable.",
        }
