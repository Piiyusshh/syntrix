from fastapi import HTTPException
from google import genai
from google.genai.errors import ClientError

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)


def generate_response(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated response.
    """

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        return response.text or ""

    except ClientError as e:
        if getattr(e, "code", None) == 429:
            raise HTTPException(
                status_code=503,
                detail="Gemini API quota exceeded. Please try again later.",
            )

        raise HTTPException(
            status_code=502,
            detail="Failed to communicate with the AI service.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating the AI response.",
        )