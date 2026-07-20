from app.services.vector_store_service import search_chunks

query = "How does authentication work?"

results = search_chunks(query)

print("\n========== MATCHED CHUNKS ==========\n")

if not results:
    print("No matching chunks found.")
else:
    for i, result in enumerate(results, start=1):
        print(f"Result #{i}")
        print(f"Distance: {result['distance']}")
        print(f"Document ID: {result['document_id']}")
        print(f"Chunk Index: {result['chunk_index']}")
        print(f"Content:\n{result['content']}")
        print("-" * 80)