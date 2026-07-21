from app.services.llm_service import generate_response
from app.services.prompt_builder import build_rag_prompt
from app.services.vector_store_service import search_chunks


def retrieve_context(
    query: str,
    top_k: int = 5,
) -> tuple[str, list[dict]]:
    """
    Retrieve the most relevant document chunks,
    combine them into a single context string,
    and return the retrieved source metadata.
    """

    matches = search_chunks(
        query=query,
        top_k=top_k,
    )

    if not matches:
        return "", []

    context = "\n\n".join(
        match["content"]
        for match in matches
    )

    sources = [
        {
            "document_name": match["document_name"],
            "chunk_index": match["chunk_index"],
        }
        for match in matches
    ]

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