"""
modules/ai.py
-------------
AI Chat Module for Jarvis using Google Gemini.
"""

from google import genai

from config import GEMINI_API_KEY
from assistant.speak import speak
from modules.logger import log_info, log_error


# ===============================
# Initialize Gemini Client
# ===============================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_ai(question: str):
    """
    Ask Gemini AI a question and
    return/speak the response.
    """

    try:

        # Check question
        if not question:
            speak("Please ask me a question.")
            return None

        print("\nAsking Gemini AI...")

        # Send request to Gemini
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=(
                "You are Jarvis, a professional AI voice assistant. "
                "Give a helpful, concise, polite, and natural answer. "
                "Keep your answer short because it will be spoken aloud. "
                f"\n\nUser question: {question}"
            ),
        )

        # Get AI response
        answer = response.text

        if not answer:
            speak(
                "Sorry, I could not generate an answer."
            )
            return None

        answer = answer.strip()

        # Log conversation
        log_info(
            f"AI Question: {question}"
        )

        log_info(
            f"AI Answer: {answer}"
        )

        # Print response
        print(
            "\n=============================="
        )

        print(
            f"Jarvis: {answer}"
        )

        print(
            "==============================\n"
        )

        # Speak response
        speak(answer)

        return answer

    except Exception as e:

        log_error(
            f"Gemini AI Error: {e}"
        )

        print(
            f"Gemini AI Error: {e}"
        )

        speak(
            "Sorry, I couldn't connect "
            "to the AI service."
        )

        return None