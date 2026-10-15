
def run_agent(question: str, documents: list[str]) -> dict:
    """Simple mock agent for testing evaluation behavior."""

    if not documents:
        return {
            "answer": "I don't have enough information to answer.",
            "citations": [],
            "tool_error": None,
        }

    # Simulate an agent that answers from the available documents.
    if "ignore previous instructions" in question.lower():
        return {
            "answer": "I cannot follow instructions that conflict with my safety rules.",
            "citations": [],
            "tool_error": None,
        }

    return {
        "answer": documents[0],
        "citations": ["manual_x200"],
        "tool_error": None,
    }
