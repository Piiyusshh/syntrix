import re

import chromadb
from chromadb.config import Settings

from app.services.embedding_service import generate_embedding

client = chromadb.PersistentClient(
    path="chroma_db",
    settings=Settings(
        anonymized_telemetry=False,
    ),
)

collection = client.get_or_create_collection(
    name="document_chunks",
)


def add_chunk(
    chunk_id: str,
    document_id: int,
    document_name: str,
    page_number: int,
    chunk_index: int,
    content: str,
) -> None:
    """
    Store a chunk and its embedding in ChromaDB.
    """

    embedding = generate_embedding(content)

    collection.add(
        ids=[chunk_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[
            {
                "document_id": document_id,
                "document_name": document_name,
                "page_number": page_number,
                "chunk_index": chunk_index,
            }
        ],
    )


def _keyword_score(query: str, content: str) -> float:
    """
    Calculate a simple keyword overlap score.
    """

    query_words = set(re.findall(r"\w+", query.lower()))
    content_words = set(re.findall(r"\w+", content.lower()))

    if not query_words:
        return 0.0

    matches = len(query_words.intersection(content_words))

    return matches / len(query_words)


def search_chunks(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Hybrid Search:
    1. Retrieve a larger candidate set using semantic search.
    2. Re-rank candidates using keyword overlap.
    3. Return the best results.
    """

    query_embedding = generate_embedding(query)

    candidate_pool = max(top_k * 4, 20)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_pool,
    )

    documents = results.get("documents")
    metadatas = results.get("metadatas")
    distances = results.get("distances")

    if not documents or not metadatas or not distances:
        return []

    matches = []

    for document, metadata, distance in zip(
        documents[0],
        metadatas[0],
        distances[0],
    ):
        semantic_score = 1 / (1 + distance)
        keyword_score = _keyword_score(query, document)

        hybrid_score = (
            semantic_score * 0.7
            + keyword_score * 0.3
        )

        matches.append(
            {
                "document_id": metadata["document_id"],
                "document_name": metadata["document_name"],
                "page_number": metadata["page_number"],
                "chunk_index": metadata["chunk_index"],
                "content": document,
                "distance": distance,
                "semantic_score": semantic_score,
                "keyword_score": keyword_score,
                "hybrid_score": hybrid_score,
            }
        )

    matches.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True,
    )

    return matches[:top_k]