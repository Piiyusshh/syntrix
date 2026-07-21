from sqlalchemy.orm import Session

from app.models.conversation import Conversation


def create_conversation(
    db: Session,
    user_id: int,
) -> Conversation:
    """
    Create a new empty conversation for the authenticated user.
    """

    conversation = Conversation(
        title=None,
        user_id=user_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation