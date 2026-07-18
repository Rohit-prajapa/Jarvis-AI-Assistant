"""
assistant/conversation.py
-------------------------
Conversation mode for Jarvis.
"""

import time

from assistant.listen import listen
from assistant.speak import speak
from assistant.commands import CommandHandler

from config import (
    CONVERSATION_TIMEOUT,
    EXIT_COMMANDS
)

from modules.logger import log_info


class ConversationMode:

    def __init__(self):
        self.handler = CommandHandler()

    def start(self):

        speak("I'm listening.")

        start_time = time.time()

        while True:

            # Timeout
            if time.time() - start_time > CONVERSATION_TIMEOUT:

                speak("Going back to sleep.")

                log_info("Conversation Timeout")

                return

            command = listen()

            if not command:
                continue

            start_time = time.time()

            if command in EXIT_COMMANDS:

                speak("Okay. Call me when you need me.")

                log_info("Conversation Ended")

                return

            self.handler.execute(command)