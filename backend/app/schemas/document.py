from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    stored_filename: str
    file_type: str
    file_size: int
    file_path: str
    uploaded_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)