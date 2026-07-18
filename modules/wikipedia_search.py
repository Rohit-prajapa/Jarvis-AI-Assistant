"""
modules/wikipedia_search.py
---------------------------
Wikipedia Search Module for Jarvis.
"""

import wikipedia

from assistant.speak import speak
from modules.logger import log_info, log_error


def search_wikipedia(query, sentences=2):
    """
    Search Wikipedia and return a short summary.
    """

    if not query:
        speak("Please tell me what you want to search on Wikipedia.")
        return None

    try:
        log_info(f"Wikipedia Search: {query}")

        # Set language to English
        wikipedia.set_lang("en")

        # Get Wikipedia summary
        result = wikipedia.summary(
            query,
            sentences=sentences,
            auto_suggest=True
        )

        print("\n==============================")
        print("Wikipedia Result:")
        print(result)
        print("==============================\n")

        log_info(f"Wikipedia Result: {result}")

        speak("According to Wikipedia.")

        speak(result)

        return result

    except wikipedia.exceptions.DisambiguationError as e:

        # The search term has multiple possible results
        options = e.options[:5]

        log_error(
            f"Wikipedia Disambiguation Error: {query}"
        )

        print(
            "Possible Wikipedia results:",
            options
        )

        speak(
            "I found multiple results. "
            "Please be more specific."
        )

        return None

    except wikipedia.exceptions.PageError:

        log_error(
            f"Wikipedia Page Not Found: {query}"
        )

        speak(
            "Sorry, I could not find a Wikipedia page for that."
        )

        return None

    except Exception as e:

        log_error(
            f"Wikipedia Error: {e}"
        )

        print(
            f"Wikipedia Error: {e}"
        )

        speak(
            "Sorry, I could not search Wikipedia right now."
        )

        return None