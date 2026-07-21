from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.conversation import ConversationResponse
from app.services.conversation_service import create_conversation

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new conversation for the authenticated user.
    """

    return create_conversation(
        db=db,
        user_id=current_user.id,
    )