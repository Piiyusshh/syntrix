from app.services.chunking_service import chunk_text


sample_text = "A" * 2500

chunks = chunk_text(sample_text)

print(f"Total Chunks: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print(f"Chunk {index}: {len(chunk)} characters")