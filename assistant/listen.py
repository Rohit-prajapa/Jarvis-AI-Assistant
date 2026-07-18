"""
assistant/listen.py
-------------------
Handles Speech Recognition for Jarvis.
"""

import speech_recognition as sr
from modules.logger import log_info, log_error


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Improve recognition in noisy environments
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        self.recognizer.dynamic_energy_threshold = True

    def listen_google(self):
        """
        Listen using Google Speech Recognition (Online)
        """

        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

                print("Recognizing...")

                text = self.recognizer.recognize_google(audio)
                text = text.lower()

                print(f"You: {text}")

                # Save user command in log
                log_info(f"User: {text}")

                return text

            except sr.WaitTimeoutError:
                print("No speech detected.")
                log_error("WaitTimeoutError: No speech detected.")
                return ""

            except sr.UnknownValueError:
                print("Sorry, I didn't understand.")
                log_error("UnknownValueError: Speech not recognized.")
                return ""

            except sr.RequestError as e:
                print("Internet connection required.")
                log_error(f"RequestError: {e}")
                return ""

    def listen_offline(self):
        """
        Listen using PocketSphinx (Offline)
        """

        with sr.Microphone() as source:

            print("\n🎤 Listening (Offline)...")

            self.recognizer.adjust_for_ambient_noise(source)

            audio = self.recognizer.listen(source)

        try:

            text = self.recognizer.recognize_sphinx(audio)
            text = text.lower()

            print(f"You: {text}")

            # Save user command in log
            log_info(f"User: {text}")

            return text

        except sr.UnknownValueError:

            print("Could not understand.")

            log_error("Offline Recognition Failed.")

            return ""

        except sr.RequestError as e:

            print(e)

            log_error(f"PocketSphinx Error: {e}")

            return ""


# Global Listener Object
listener = Listener()


def listen():
    return listener.listen_google()


def listen_offline():
    return listener.listen_offline()