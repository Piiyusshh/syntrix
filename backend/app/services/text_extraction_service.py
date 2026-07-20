from pathlib import Path

import fitz  # PyMuPDF
from docx import Document as DocxDocument
from fastapi import HTTPException


SUPPORTED_FILE_TYPES = {
    "pdf",
    "docx",
    "txt",
}


def extract_text(file_path: str) -> str:
    """
    Extract text from a supported document.
    """

    path = Path(file_path)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document file not found.",
        )

    extension = path.suffix.lower().removeprefix(".")

    if extension not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}",
        )

    try:
        if extension == "pdf":
            text = extract_pdf_text(path)

        elif extension == "docx":
            text = extract_docx_text(path)

        else:
            text = extract_txt_text(path)

        return clean_text(text)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text: {str(exc)}",
        )


def extract_pdf_text(path: Path) -> str:
    """
    Extract text from a PDF document.
    """

    document = fitz.open(path)

    try:
        pages = []

        for page in document:
            pages.append(page.get_text())

        return "\n".join(pages)

    finally:
        document.close()


def extract_docx_text(path: Path) -> str:
    """
    Extract text from a DOCX document.
    """

    document = DocxDocument(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:
        paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_txt_text(path: Path) -> str:
    """
    Extract text from a TXT document.
    """

    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def clean_text(text: str) -> str:
    """
    Normalize extracted text.
    """

    lines = []

    for line in text.splitlines():

        cleaned = " ".join(line.split())

        if cleaned:
            lines.append(cleaned)

    return "\n".join(lines).strip()