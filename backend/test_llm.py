from app.services.llm_service import generate_response

prompt = """
Say hello in one sentence.
"""

print("\n========== GEMINI TEST ==========\n")

response = generate_response(prompt)

print(response)