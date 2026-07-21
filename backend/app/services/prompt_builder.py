def build_rag_prompt(
    question: str,
    context: str,
    conversation_history: str = "",
) -> str:
    """
    Build the prompt for the RAG pipeline.
    """

    history_section = ""

    if conversation_history:
        history_section = f"""
Conversation History:
---------------------
{conversation_history}
"""

    return f"""
You are Syntrix, an AI-powered document assistant.

Use ONLY the information provided in the context below.

If the answer cannot be found in the context, clearly say:

"I couldn't find that information in the uploaded documents."

Do not make up information.
Do not use outside knowledge.

{history_section}

Context:
---------
{context}
---------

Current Question:
{question}

Answer:
"""