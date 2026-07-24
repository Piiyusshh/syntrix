from pydantic import BaseModel


class ExtractedPage(BaseModel):
    page_number: int
    text: str


class ExtractedDocument(BaseModel):
    pages: list[ExtractedPage]