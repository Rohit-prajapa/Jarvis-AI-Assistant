"""
modules/explorer.py
-------------------
Explorer related functions.
"""

import os
from assistant.speak import speak


def open_explorer():
    """Open File Explorer."""
    speak("Opening File Explorer")
    os.system("explorer")


def open_desktop():
    """Open Desktop folder."""
    speak("Opening Desktop")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    os.startfile(desktop)


def open_documents():
    """Open Documents folder."""
    speak("Opening Documents")
    documents = os.path.join(os.path.expanduser("~"), "Documents")
    os.startfile(documents)


def open_downloads():
    """Open Downloads folder."""
    speak("Opening Downloads")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    os.startfile(downloads)


def open_pictures():
    """Open Pictures folder."""
    speak("Opening Pictures")
    pictures = os.path.join(os.path.expanduser("~"), "Pictures")
    os.startfile(pictures)


def open_music():
    """Open Music folder."""
    speak("Opening Music")
    music = os.path.join(os.path.expanduser("~"), "Music")
    os.startfile(music)


def open_videos():
    """Open Videos folder."""
    speak("Opening Videos")
    videos = os.path.join(os.path.expanduser("~"), "Videos")
    os.startfile(videos)