from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: int
    question: str


class Source(BaseModel):
    document_name: str
    chunk_index: int
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]