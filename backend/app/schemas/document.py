from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int

    uploaded_at: datetime

    processing_status: str
    processed_at: datetime | None

    owner_id: int

    model_config = ConfigDict(from_attributes=True)