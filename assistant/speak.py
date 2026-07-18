"""
assistant/speak.py
------------------
Handles Text-to-Speech for Jarvis.
"""

import pyttsx3
from config import VOICE_RATE, VOICE_VOLUME
from modules.logger import log_info


class Speaker:
    def __init__(self):
        """Initialize the speech engine."""

        self.engine = pyttsx3.init()

        # Speech settings
        self.engine.setProperty("rate", VOICE_RATE)
        self.engine.setProperty("volume", VOICE_VOLUME)

        # Select male voice
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id)

    def speak(self, text: str):
        """Speak the given text."""

        if not text:
            return

        print(f"Jarvis: {text}")

        # Save response in log file
        log_info(f"Jarvis: {text}")

        # Speak the text
        self.engine.say(text)
        self.engine.runAndWait()


# Global Speaker Object
speaker = Speaker()


def speak(text: str):
    """
    Shortcut function.
    Example:
        speak("Hello Rohit")
    """
    speaker.speak(text)