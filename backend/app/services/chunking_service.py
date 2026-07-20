from typing import List


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text: str) -> List[str]:
    """
    Split text into overlapping chunks.

    Example:
    Chunk 1: 0-1000
    Chunk 2: 800-1800
    Chunk 3: 1600-2600
    """

    text = text.strip()

    if not text:
        return []

    chunks: List[str] = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks