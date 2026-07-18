"""
main.py
-------
Main entry point for Jarvis AI Assistant.
"""

from assistant.speak import speak
from assistant.wake_word import wait_for_wake_word
from assistant.conversation import ConversationMode

from modules.logger import (
    log_info,
    log_error,
)


def main():
    """
    Start Jarvis AI Assistant.
    """

    try:
        print(
            "\n"
            "==================================\n"
            "       JARVIS AI ASSISTANT\n"
            "==================================\n"
        )

        log_info(
            "Jarvis application starting."
        )

        # Start Jarvis
        speak(
            "Jarvis is online and ready to help you."
        )

        # Create conversation mode
        conversation = ConversationMode()

        # Main program loop
        while True:

            try:
                # Wait for "Jarvis"
                wait_for_wake_word()

                # Start conversation
                conversation.start()

            except KeyboardInterrupt:
                raise

            except Exception as e:

                log_error(
                    f"Jarvis Loop Error: {e}"
                )

                print(
                    f"Jarvis Loop Error: {e}"
                )

                speak(
                    "I encountered an error, "
                    "but I am still running."
                )

    except KeyboardInterrupt:

        print(
            "\nJarvis shutting down..."
        )

        log_info(
            "Jarvis stopped by user."
        )

        speak(
            "Goodbye Rohit."
        )

    except Exception as e:

        log_error(
            f"Critical Jarvis Error: {e}"
        )

        print(
            f"Critical Error: {e}"
        )

        try:
            speak(
                "A critical error occurred. "
                "Jarvis is shutting down."
            )

        except Exception:
            pass


if __name__ == "__main__":
    main()