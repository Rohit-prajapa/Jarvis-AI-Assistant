"""
assistant/ai_mode.py
--------------------
Continuous AI Voice Conversation Mode.
"""

from assistant.listen import listen
from assistant.speak import speak
from modules.ai import ask_ai
from modules.logger import log_info


EXIT_COMMANDS = [
    "exit ai mode",
    "stop ai",
    "close ai",
    "goodbye",
    "bye"
]


class AIMode:

    def start(self):

        speak("AI mode activated.")

        speak("Ask me anything.")

        while True:

            command = listen()

            if not command:
                continue

            command = command.lower().strip()

            if command in EXIT_COMMANDS:

                speak("Leaving AI mode.")

                log_info("AI Mode Closed")

                return

            ask_ai(command)