"""
modules/notepad.py
------------------
Notepad related functions.
"""

import os
from assistant.speak import speak


def open_notepad():
    """Open Windows Notepad."""
    speak("Opening Notepad")
    os.system("notepad")


def close_notepad():
    """Close Windows Notepad."""
    speak("Closing Notepad")
    os.system("taskkill /f /im notepad.exe")