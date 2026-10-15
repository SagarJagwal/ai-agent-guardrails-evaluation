
class ToolError(Exception):
    """Raised when an agent tool fails."""


def search_documents(query: str, simulate_failure: bool = False) -> dict:
    """Mock document-search tool for reliability testing."""

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


def safe_search_documents(query: str) -> dict:
    """Handle expected tool failures without crashing the agent."""

    try:
        return search_documents(query)
    except ToolError:
        return {
            "status": "error",
            "results": [],
            "message": "Document search is temporarily unavailable.",
        }
