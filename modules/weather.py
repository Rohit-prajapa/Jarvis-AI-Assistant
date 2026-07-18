"""
modules/weather.py
------------------
Weather module for Jarvis AI Assistant.

Gets current weather information using
the OpenWeatherMap API.
"""

import requests

from assistant.speak import speak
from config import WEATHER_API_KEY


# ==================================
# OpenWeatherMap Configuration
# ==================================

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ==================================
# Get Weather
# ==================================

def get_weather(city):
    """
    Get current weather information
    for the given city.
    """

    # Clean city name
    city = city.strip()

    print(f"Weather requested for: {city}")

    # Check city
    if not city:
        message = "Please tell me the city name."
        print(f"Jarvis: {message}")
        speak(message)
        return None

    # Check API key
    if not WEATHER_API_KEY:
        message = (
            "Weather API key is not configured. "
            "Please check your environment file."
        )

        print("ERROR: WEATHER_API_KEY is missing.")
        speak(message)

        return None

    # API parameters
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }

    try:
        # Send request to OpenWeatherMap
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10,
        )

        print(
            f"Weather API Status Code: "
            f"{response.status_code}"
        )

        # Convert response to JSON
        data = response.json()

        # Check API response
        if response.status_code != 200:

            error_message = data.get(
                "message",
                "Unknown weather API error",
            )

            print(
                f"Weather API Error: "
                f"{error_message}"
            )

            if response.status_code == 401:
                message = (
                    "The weather API key is invalid "
                    "or not activated yet."
                )

            elif response.status_code == 404:
                message = (
                    f"Sorry, I could not find "
                    f"weather information for {city}."
                )

            else:
                message = (
                    "Sorry, I could not get "
                    "the weather information."
                )

            speak(message)

            return None

        # Extract weather data
        temperature = data["main"]["temp"]

        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        description = (
            data["weather"][0]["description"]
        )

        wind_speed = data["wind"]["speed"]

        # Get official city name
        city_name = data.get(
            "name",
            city,
        )

        # Create weather report
        report = (
            f"The weather in {city_name} "
            f"is {description}. "
            f"The temperature is "
            f"{round(temperature)} degrees Celsius. "
            f"It feels like "
            f"{round(feels_like)} degrees Celsius. "
            f"The humidity is "
            f"{humidity} percent. "
            f"The wind speed is "
            f"{wind_speed} meters per second."
        )

        # Print response
        print(
            f"\nJarvis: {report}\n"
        )

        # Speak response
        speak(report)

        return report

    # Internet / API connection errors
    except requests.exceptions.Timeout:

        message = (
            "The weather service took too long "
            "to respond. Please try again."
        )

        print(
            "Weather API Error: Request timeout."
        )

        speak(message)

        return None

    except requests.exceptions.ConnectionError:

        message = (
            "I could not connect to the weather "
            "service. Please check your internet "
            "connection."
        )

        print(
            "Weather API Error: Connection failed."
        )

        speak(message)

        return None

    except requests.exceptions.RequestException as e:

        print(
            f"Weather Request Error: {e}"
        )

        speak(
            "Sorry, there was a problem "
            "connecting to the weather service."
        )

        return None

    # Other unexpected errors
    except Exception as e:

        print(
            f"Weather Error: {e}"
        )

        speak(
            "Sorry, I could not get "
            "the weather information."
        )

        return None