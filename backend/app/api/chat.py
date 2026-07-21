from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import answer_question

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Answer a user's question using the RAG pipeline.
    """

    answer = answer_question(request.question)

    return ChatResponse(
        answer=answer,
    )