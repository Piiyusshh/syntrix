import re

from app.services.llm_service import generate_response


FOLLOW_UP_PATTERNS = [
    r"\bit\b",
    r"\bits\b",
    r"\bthey\b",
    r"\bthem\b",
    r"\btheir\b",
    r"\bthis\b",
    r"\bthat\b",
    r"\bthese\b",
    r"\bthose\b",
    r"\bhe\b",
    r"\bshe\b",
    r"\bfirst\b",
    r"\bsecond\b",
    r"\bthird\b",
    r"\bprevious\b",
    r"\babove\b",
]


def is_follow_up_question(question: str) -> bool:
    """
    Returns True if the question appears to depend
    on previous conversation context.
    """
    question = question.lower()

    return any(
        re.search(pattern, question)
        for pattern in FOLLOW_UP_PATTERNS
    )


def rewrite_query(
    question: str,
    conversation_history: str,
) -> str:
    """
    Rewrite follow-up questions into standalone questions.

    Standalone questions bypass rewriting to save
    LLM requests.
    """

    if not conversation_history.strip():
        print("\n=== Query Rewriter ===")
        print("No conversation history.")
        print("======================\n")
        return question

    if not is_follow_up_question(question):
        print("\n=== Query Rewriter ===")
        print("Standalone question detected.")
        print("Skipping rewrite.")
        print("======================\n")
        return question

    prompt = f"""
You are an AI assistant that rewrites follow-up questions.

Convert the latest question into a standalone question.

Rules:
- Do not answer.
- Do not add information.
- Preserve intent.
- Return only the rewritten question.

Conversation History:
{conversation_history}

Latest Question:
{question}

Standalone Question:
"""

    rewritten_question = generate_response(prompt).strip()

    if not rewritten_question:
        rewritten_question = question

    print("\n=== Query Rewriter ===")
    print(f"Original : {question}")
    print(f"Rewritten: {rewritten_question}")
    print("======================\n")

    return rewritten_question