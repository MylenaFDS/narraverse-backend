import os
import time

from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_text(prompt: str):

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )

            return response.text

        except Exception:

            if attempt == 2:
                raise

            time.sleep(2)