"""
assistant/news.py
-----------------
Latest News Module for Jarvis.
"""

import requests

from assistant.speak import speak
from modules.logger import log_info, log_error
from config import NEWS_API_KEY


def get_latest_news(country="us", limit=5):
    """
    Fetch and speak the latest news headlines.
    """

    if not NEWS_API_KEY:
        speak("News API key is not configured.")
        log_error("NEWS_API_KEY is missing.")
        return []

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "country": country,
        "apiKey": NEWS_API_KEY,
        "pageSize": limit,
    }

    try:
        speak("Getting the latest news.")

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            speak("I could not find any news headlines.")
            return []

        headlines = []

        for article in articles[:limit]:

            title = article.get("title")

            if title:
                headlines.append(title)

        if not headlines:
            speak("No news headlines are available.")
            return []

        speak(
            f"Here are the top {len(headlines)} news headlines."
        )

        for number, headline in enumerate(
            headlines,
            start=1
        ):
            print(
                f"{number}. {headline}"
            )

            speak(
                f"Headline {number}. {headline}"
            )

        log_info(
            f"Fetched {len(headlines)} news headlines."
        )

        return headlines

    except requests.RequestException as e:

        log_error(
            f"News Request Error: {e}"
        )

        print(
            f"News Error: {e}"
        )

        speak(
            "Sorry, I could not get the latest news."
        )

        return []

    except Exception as e:

        log_error(
            f"News Error: {e}"
        )

        print(
            f"News Error: {e}"
        )

        speak(
            "Something went wrong while getting the news."
        )

        return []