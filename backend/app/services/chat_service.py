from sqlalchemy.orm import Session

from app.models.message import MessageRole
from app.services.conversation_service import get_conversation
from app.services.message_service import (
    create_message,
    format_conversation_history,
    get_conversation_messages,
)
from app.services.query_rewriter_service import rewrite_query
from app.services.rag_service import answer_question


def process_chat(
    db: Session,
    conversation_id: int,
    user_id: int,
    question: str,
) -> dict:
    """
    Process a chat request by validating the conversation,
    rewriting follow-up questions into standalone questions,
    generating an AI response, and saving both user and
    assistant messages.
    """

    # Ensure the conversation belongs to the user.
    get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
    )

    # Load recent conversation history.
    messages = get_conversation_messages(
        db=db,
        conversation_id=conversation_id,
    )

    conversation_history = format_conversation_history(
        messages,
    )

    # Rewrite follow-up questions into standalone questions.
    rewritten_question = rewrite_query(
        question=question,
        conversation_history=conversation_history,
    )

    # Save the user's original question.
    create_message(
        db=db,
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=question,
    )

    # Generate AI response using rewritten question.
    result = answer_question(
        question=rewritten_question,
        conversation_history=conversation_history,
    )

    # Save assistant response.
    create_message(
        db=db,
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
        content=result["answer"],
    )

    return result