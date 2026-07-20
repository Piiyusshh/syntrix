from app.services.embedding_service import generate_embedding

sample_text = "Artificial Intelligence is transforming software development."

embedding = generate_embedding(sample_text)

print(f"Embedding Dimension: {len(embedding)}")
print("\nFirst 10 Values:")
print(embedding[:10])