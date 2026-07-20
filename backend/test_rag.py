from app.services.rag_service import retrieve_context

query = "What are the technical skills?"

context = retrieve_context(query)

print("\n========== RETRIEVED CONTEXT ==========\n")

if not context:
    print("No context found.")
else:
    print(context)