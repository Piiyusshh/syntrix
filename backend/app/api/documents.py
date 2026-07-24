from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import (
    DocumentResponse,
    DocumentSummaryResponse,
)
from app.services.document_service import (
    delete_document,
    get_document_for_download,
    get_user_documents,
    save_document,
)
from app.services.summary_service import (
    generate_document_summary,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload a document.
    """

    return save_document(
        db=db,
        uploaded_file=file,
        owner_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all documents belonging to the authenticated user.
    """

    return get_user_documents(
        db=db,
        owner_id=current_user.id,
    )


@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Download a document owned by the authenticated user.
    """

    document = get_document_for_download(
        db=db,
        document_id=document_id,
        owner_id=current_user.id,
    )

    return FileResponse(
        path=document.file_path,
        filename=document.filename,
        media_type="application/octet-stream",
    )


@router.post(
    "/{document_id}/summary",
    response_model=DocumentSummaryResponse,
)
def summarize_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate an AI summary for a document.
    The summary is generated only once and cached.
    """

    return generate_document_summary(
        db=db,
        document_id=document_id,
        owner_id=current_user.id,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
)
def remove_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a document owned by the authenticated user.
    """

    deleted = delete_document(
        db=db,
        document_id=document_id,
        owner_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return {
        "message": "Document deleted successfully."
    }