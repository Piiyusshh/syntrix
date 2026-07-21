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
    limit: int = 10,
) -> list[Message]:
    """
    Return the most recent messages for a conversation
    in chronological order.
    """

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id,
        )
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    return list(reversed(messages))


def format_conversation_history(
    messages: list[Message],
) -> str:
    """
    Convert conversation messages into a format
    suitable for the LLM prompt.
    """

    if not messages:
        return ""

    history = []

    for message in messages:
        history.append(
            f"{message.role.value.capitalize()}: {message.content}"
        )

    return "\n\n".join(history)