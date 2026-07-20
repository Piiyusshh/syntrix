from app.services.vector_store_service import search_chunks


def retrieve_context(
    query: str,
    top_k: int = 5,
) -> str:
    """
    Retrieve the most relevant document chunks and
    combine them into a single context string.
    """

    matches = search_chunks(
        query=query,
        top_k=top_k,
    )

    if not matches:
        return ""

    context = "\n\n".join(
        match["content"]
        for match in matches
    )

    return context