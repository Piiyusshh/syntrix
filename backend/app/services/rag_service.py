from app.services.llm_service import generate_response
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


def answer_question(
    question: str,
    top_k: int = 5,
) -> str:
    """
    Retrieve relevant context and generate
    an answer using Gemini.
    """

    context = retrieve_context(
        query=question,
        top_k=top_k,
    )

    if not context:
        return "I couldn't find any relevant information in the uploaded documents."

    prompt = f"""
You are Syntrix, an AI-powered document assistant.

Use ONLY the information provided in the context below.

If the answer cannot be found in the context, clearly say:
"I couldn't find that information in the uploaded documents."

Do not make up information.
Do not use outside knowledge.

Context:
---------
{context}
---------

Question:
{question}

Answer:
"""

    return generate_response(prompt)