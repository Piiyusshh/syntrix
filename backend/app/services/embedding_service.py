from sentence_transformers import SentenceTransformer

# Load the embedding model once when the application starts.
# This avoids reloading the model for every request.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the given text.
    """

    embedding = embedding_model.encode(
        text,
        convert_to_numpy=True,
    )

    return embedding.tolist()