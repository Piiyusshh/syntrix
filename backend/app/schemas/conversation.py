from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    pass


class ConversationUpdate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: int
    title: str | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)