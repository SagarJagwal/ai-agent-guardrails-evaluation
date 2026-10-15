
from app.guardrails import detect_indirect_injection


def run_agent(question: str, documents: list[str]) -> dict:
    """Mock agent with basic indirect-injection filtering."""

    if not documents:
        return {
            "answer": "I don't have enough information to answer.",
            "citations": [],
            "tool_error": None,
        }

    # Filter suspicious documents before using them as evidence.
    safe_documents = [
        document
        for document in documents
        if not detect_indirect_injection(document)
    ]

    if not safe_documents:
        return {
            "answer": "I cannot answer safely because the retrieved "
                      "documents contain suspicious instructions.",
            "citations": [],
            "tool_error": None,
        }

    if "ignore previous instructions" in question.lower():
        return {
            "answer": "I cannot follow instructions that conflict "
                      "with my safety rules.",
            "citations": [],
            "tool_error": None,
        }

    return {
        "answer": safe_documents[0],
        "citations": ["manual_x200"],
        "tool_error": None,
    }
