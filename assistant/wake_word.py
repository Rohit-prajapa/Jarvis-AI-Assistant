"""
assistant/wake_word.py
----------------------
Wake Word Detection for Jarvis.
"""

from assistant.listen import listen
from assistant.speak import speak
from modules.logger import log_info


WAKE_WORDS = [
    "jarvis",
    "hey jarvis",
]


def wait_for_wake_word():
    """
    Keep listening until Jarvis wake word is detected.
    """

    print("\nWaiting for wake word: Jarvis...")

    while True:

        text = listen()

        if not text:
            continue

        text = text.lower().strip()

        # Check wake words
        for wake_word in WAKE_WORDS:

            if wake_word in text:

                print("Wake word detected!")

                log_info(
                    f"Wake word detected: {wake_word}"
                )

                speak("Yes Sir.")

                return True