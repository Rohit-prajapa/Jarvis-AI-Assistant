"""
modules/location.py
-------------------
Public IP and Approximate Location Module for Jarvis.
"""

import requests

from assistant.speak import speak
from modules.logger import log_info, log_error


def get_public_ip():
    """
    Get the computer's public IP address.
    """

    try:
        response = requests.get(
            "https://api.ipify.org?format=json",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        ip_address = data.get("ip")

        if ip_address:
            print(f"Public IP Address: {ip_address}")

            log_info("Public IP address retrieved successfully.")

            speak(
                f"Your public IP address is {ip_address}"
            )

            return ip_address

        speak("I could not find your public IP address.")

        return None

    except requests.RequestException as e:

        log_error(
            f"Public IP Error: {e}"
        )

        print(
            f"Public IP Error: {e}"
        )

        speak(
            "Sorry, I could not get your public IP address."
        )

        return None


def get_location():
    """
    Get approximate location using the public IP address.
    """

    try:
        response = requests.get(
            "https://ipapi.co/json/",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country_name")

        if city and country:

            location = f"{city}, {region}, {country}"

            print(f"Approximate Location: {location}")

            log_info(
                "Approximate location retrieved successfully."
            )

            speak(
                f"Your approximate location is {location}."
            )

            return location

        speak(
            "I could not determine your approximate location."
        )

        return None

    except requests.RequestException as e:

        log_error(
            f"Location Error: {e}"
        )

        print(
            f"Location Error: {e}"
        )

        speak(
            "Sorry, I could not get your location."
        )

        return None