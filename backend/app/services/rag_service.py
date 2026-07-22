from app.services.llm_service import generate_response
from app.services.prompt_builder import build_rag_prompt
from app.services.vector_store_service import search_chunks


SNIPPET_LENGTH = 120


def retrieve_context(
    query: str,
    top_k: int = 5,
) -> tuple[str, list[dict]]:
    """
    Retrieve the most relevant document chunks,
    combine them into a single context string,
    and return unique source metadata.
    """

    matches = search_chunks(
        query=query,
        top_k=top_k,
    )

    if not matches:
        return "", []

    # Build context using all retrieved chunks.
    context = "\n\n".join(
        match["content"]
        for match in matches
    )

    # Keep only the first occurrence of each document.
    seen_documents = set()
    sources = []

    for match in matches:
        document_name = match["document_name"]

        if document_name not in seen_documents:
            snippet = match["content"].strip()

            if len(snippet) > SNIPPET_LENGTH:
                snippet = snippet[:SNIPPET_LENGTH].rstrip() + "..."

            sources.append(
                {
                    "document_name": document_name,
                    "chunk_index": match["chunk_index"],
                    "snippet": snippet,
                }
            )

            seen_documents.add(document_name)

    return context, sources


def answer_question(
    question: str,
    conversation_history: str = "",
    top_k: int = 5,
) -> dict:
    """
    Retrieve relevant context and generate
    an answer using Gemini.
    """

    context, sources = retrieve_context(
        query=question,
        top_k=top_k,
    )

    if not context:
        return {
            "answer": (
                "I couldn't find any relevant information "
                "in the uploaded documents."
            ),
            "sources": [],
        }

    prompt = build_rag_prompt(
        question=question,
        context=context,
        conversation_history=conversation_history,
    )

    answer = generate_response(prompt)

    return {
        "answer": answer,
        "sources": sources,
    }