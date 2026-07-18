"""
modules/internet.py
-------------------
Internet Connection Status Module for Jarvis.
"""

import requests

from assistant.speak import speak
from modules.logger import log_info, log_error


def is_internet_connected():
    """
    Check whether an internet connection is available.
    Returns True if connected, otherwise False.
    """

    try:
        response = requests.get(
            "https://www.google.com",
            timeout=5
        )

        return response.status_code == 200

    except requests.RequestException as e:
        log_error(f"Internet Connection Error: {e}")
        return False


def check_internet():
    """
    Check internet status and speak the result.
    """

    if is_internet_connected():

        message = "Your internet connection is working."

        print(message)
        log_info("Internet Status: Connected")
        speak(message)

        return True

    else:

        message = "You are not connected to the internet."

        print(message)
        log_info("Internet Status: Disconnected")
        speak(message)

        return False