import os
from google import genai


def ask_gemini(user_message):
    """
    Sends the user's message to Gemini and returns the AI response.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Please add it in PyCharm environment variables."

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        return response.text

    except Exception as error:
        return f"Gemini API error: {error}"