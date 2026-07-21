from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)


def generate_response(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated response.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    return response.text or ""