from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.llm_service import generate_response


SUMMARY_PROMPT = """
You are an expert document summarizer.

Create a clear and well-structured summary of the following document.

Requirements:
- Keep the summary between 150 and 250 words.
- Focus only on important information.
- Do not invent facts.
- Use simple professional English.
- If the document contains interview questions, study material, or notes,
  explain what topics it covers.
- Return only the summary.

Document:

{document}
"""


def generate_document_summary(
    db: Session,
    document_id: int,
    owner_id: int,
) -> dict:
    """
    Generate a summary for a document.
    The summary is generated only once and then stored
    in the database for future requests.
    """

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == owner_id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    if document.summary:
        return {
            "document_id": document.id,
            "document_name": document.filename,
            "summary": document.summary,
            "cached": True,
        }

    if not document.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Document has no extracted text.",
        )

    prompt = SUMMARY_PROMPT.format(
        document=document.extracted_text,
    )

    summary = generate_response(prompt)

    document.summary = summary

    db.commit()
    db.refresh(document)

    return {
        "document_id": document.id,
        "document_name": document.filename,
        "summary": summary,
        "cached": False,
    }