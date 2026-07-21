from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """
    Answer a user's question and store the conversation.
    """

    result = process_chat(
        db=db,
        conversation_id=request.conversation_id,
        user_id=current_user.id,
        question=request.question,
    )

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )