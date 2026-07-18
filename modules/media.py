"""
modules/media.py
----------------
Media control functions.
"""

import keyboard
import pywhatkit
from assistant.speak import speak


def play_youtube(video):
    """Play a video on YouTube."""
    speak(f"Playing {video} on YouTube")
    pywhatkit.playonyt(video)


def pause_media():
    """Pause or resume media."""
    speak("Pausing media")
    keyboard.press_and_release("play/pause media")


def next_track():
    """Play next track."""
    speak("Playing next track")
    keyboard.press_and_release("next track")


def previous_track():
    """Play previous track."""
    speak("Playing previous track")
    keyboard.press_and_release("previous track")


def volume_up():
    """Increase volume."""
    speak("Increasing volume")

    for _ in range(5):
        keyboard.press_and_release("volume up")


def volume_down():
    """Decrease volume."""

    speak("Decreasing volume")

    for _ in range(5):
        keyboard.press_and_release("volume down")


def mute_volume():
    """Mute system volume."""

    speak("Muting volume")

    keyboard.press_and_release("volume mute")