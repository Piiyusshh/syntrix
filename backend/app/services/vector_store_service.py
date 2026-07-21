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
                "chunk_index": chunk_index,
            }
        ],
    )


def search_chunks(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Search for the most relevant chunks and return a clean result.
    """

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
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
        matches.append(
            {
                "document_id": metadata["document_id"],
                "document_name": metadata["document_name"],
                "chunk_index": metadata["chunk_index"],
                "content": document,
                "distance": distance,
            }
        )

    return matches