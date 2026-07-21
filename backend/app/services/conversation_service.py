from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.schemas.conversation import ConversationUpdate


def _get_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> Conversation:
    """
    Return a conversation owned by the authenticated user.
    """

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation


def create_conversation(
    db: Session,
    user_id: int,
) -> Conversation:
    """
    Create a new empty conversation.
    """

    conversation = Conversation(
        title=None,
        user_id=user_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_user_conversations(
    db: Session,
    user_id: int,
) -> list[Conversation]:
    """
    Return all conversations belonging to the authenticated user.
    """

    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


def get_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> Conversation:
    """
    Return a single conversation owned by the authenticated user.
    """

    return _get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
    )


def update_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
    conversation_update: ConversationUpdate,
) -> Conversation:
    """
    Update a conversation title.
    """

    conversation = _get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
    )

    conversation.title = conversation_update.title

    db.commit()
    db.refresh(conversation)

    return conversation


def delete_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> bool:
    """
    Delete a conversation owned by the authenticated user.
    """

    conversation = _get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
    )

    db.delete(conversation)
    db.commit()

    return True