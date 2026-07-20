from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import HTTPException, UploadFile

UPLOAD_DIRECTORY = (
    Path(__file__).resolve().parent.parent.parent
    / "uploads"
    / "documents"
)

UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(
    uploaded_file: UploadFile,
) -> tuple[str, str, int, str]:
    """
    Save an uploaded file to disk.

    Returns:
        stored_filename,
        file_path,
        file_size,
        file_type
    """

    if not uploaded_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must have a filename.",
        )

    original_filename = uploaded_file.filename

    extension = Path(original_filename).suffix.lower()
    file_type = extension.removeprefix(".")

    stored_filename = f"{uuid4()}{extension}"

    destination = UPLOAD_DIRECTORY / stored_filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return (
        stored_filename,
        str(destination),
        destination.stat().st_size,
        file_type,
    )


def delete_uploaded_file(file_path: str) -> None:
    """
    Delete a file from disk if it exists.
    """

    path = Path(file_path)

    if path.exists():
        path.unlink()