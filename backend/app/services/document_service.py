from datetime import UTC, datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.file_service import (
    delete_uploaded_file,
    save_uploaded_file,
)
from app.services.text_extraction_service import extract_text


def save_document(
    db: Session,
    uploaded_file: UploadFile,
    owner_id: int,
) -> Document:
    """
    Save a document, extract its text,
    and store everything in a single transaction.
    """

    if not uploaded_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must have a filename.",
        )

    (
        stored_filename,
        file_path,
        file_size,
        file_type,
    ) = save_uploaded_file(uploaded_file)

    try:
        extracted_text = extract_text(file_path)

        document = Document(
            filename=uploaded_file.filename,
            stored_filename=stored_filename,
            file_type=file_type,
            file_size=file_size,
            file_path=file_path,
            uploaded_at=datetime.now(UTC).replace(tzinfo=None),
            owner_id=owner_id,
            extracted_text=extracted_text,
            processing_status="COMPLETED",
            processed_at=datetime.now(UTC).replace(tzinfo=None),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()

        delete_uploaded_file(file_path)

        raise HTTPException(
            status_code=500,
            detail="Failed to process and save document.",
        )


def get_user_documents(
    db: Session,
    owner_id: int,
) -> list[Document]:
    """
    Return all documents belonging to a specific user.
    """

    return (
        db.query(Document)
        .filter(Document.owner_id == owner_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


def get_document_for_download(
    db: Session,
    document_id: int,
    owner_id: int,
) -> Document:
    """
    Return a document if it belongs to the authenticated user.
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

    if not Path(document.file_path).exists():
        raise HTTPException(
            status_code=404,
            detail="Physical file not found.",
        )

    return document


def delete_document(
    db: Session,
    document_id: int,
    owner_id: int,
) -> bool:
    """
    Delete a document owned by the specified user.
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
        return False

    try:
        delete_uploaded_file(document.file_path)

        db.delete(document)
        db.commit()

        return True

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete document.",
        )