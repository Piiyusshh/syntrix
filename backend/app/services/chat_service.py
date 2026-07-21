from sqlalchemy.orm import Session

from app.models.message import MessageRole
from app.services.conversation_service import get_conversation
from app.services.message_service import create_message
from app.services.rag_service import answer_question


def process_chat(
    db: Session,
    conversation_id: int,
    user_id: int,
    question: str,
) -> str:
    """
    Process a chat request by validating the conversation,
    generating an AI response, and saving both user and
    assistant messages.
    """

    # Ensure the conversation belongs to the user.
    get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
    )

    # Save the user's message.
    create_message(
        db=db,
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=question,
    )

    # Generate AI response.
    answer = answer_question(question)

    # Save the assistant's reply.
    create_message(
        db=db,
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
        content=answer,
    )

    return answer