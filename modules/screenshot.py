"""
modules/screenshot.py
---------------------
Screenshot Module for Jarvis.
"""

import os
import datetime
import pyautogui

from assistant.speak import speak
from modules.logger import log_info, log_error


# Folder where screenshots will be saved
SCREENSHOT_FOLDER = "screenshots"


def take_screenshot():
    """
    Take a screenshot and save it with
    the current date and time.
    """

    try:
        # Create screenshots folder if it doesn't exist
        os.makedirs(
            SCREENSHOT_FOLDER,
            exist_ok=True
        )

        # Create unique filename
        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = f"screenshot_{timestamp}.png"

        file_path = os.path.join(
            SCREENSHOT_FOLDER,
            filename
        )

        # Take screenshot
        screenshot = pyautogui.screenshot()

        # Save screenshot
        screenshot.save(file_path)

        log_info(
            f"Screenshot saved: {file_path}"
        )

        print(
            f"Screenshot saved at: {file_path}"
        )

        speak(
            "Screenshot taken successfully."
        )

        return file_path

    except Exception as e:

        log_error(
            f"Screenshot Error: {e}"
        )

        print(
            f"Screenshot Error: {e}"
        )

        speak(
            "Sorry, I could not take the screenshot."
        )

        return None