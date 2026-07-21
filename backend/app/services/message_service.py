from sqlalchemy.orm import Session

from app.models.message import Message, MessageRole


def create_message(
    db: Session,
    conversation_id: int,
    role: MessageRole,
    content: str,
) -> Message:
    """
    Save a message for a conversation.
    """

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_messages(
    db: Session,
    conversation_id: int,
) -> list[Message]:
    """
    Return all messages for a conversation
    ordered chronologically.
    """

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id,
        )
        .order_by(Message.created_at.asc())
        .all()
    )