"""
modules/clipboard.py
--------------------
Clipboard Manager for Jarvis.
"""

import pyperclip

from assistant.speak import speak
from modules.logger import log_info, log_error


def read_clipboard():
    """
    Read text currently stored in the clipboard.
    """

    try:
        text = pyperclip.paste()

        if text and text.strip():
            print(f"Clipboard: {text}")

            log_info("Clipboard content read.")

            speak(f"Your clipboard contains: {text}")

            return text

        speak("Your clipboard is empty.")

        return ""

    except Exception as e:
        log_error(f"Read Clipboard Error: {e}")

        speak("Sorry, I could not read the clipboard.")

        return ""


def copy_to_clipboard(text):
    """
    Copy text to the clipboard.
    """

    try:
        if not text:
            speak("There is no text to copy.")
            return False

        pyperclip.copy(text)

        log_info(f"Text copied to clipboard: {text}")

        speak("Text copied to clipboard successfully.")

        return True

    except Exception as e:
        log_error(f"Copy Clipboard Error: {e}")

        speak("Sorry, I could not copy the text.")

        return False


def clear_clipboard():
    """
    Clear clipboard content.
    """

    try:
        pyperclip.copy("")

        log_info("Clipboard cleared.")

        speak("Clipboard cleared successfully.")

        return True

    except Exception as e:
        log_error(f"Clear Clipboard Error: {e}")

        speak("Sorry, I could not clear the clipboard.")

        return False