"""
modules/system.py
-----------------
System related functions.
"""

import os
from assistant.speak import speak


def open_notepad():
    speak("Opening Notepad")
    os.system("notepad")


def open_calculator():
    speak("Opening Calculator")
    os.system("calc")


def open_paint():
    speak("Opening Paint")
    os.system("mspaint")


def open_cmd():
    speak("Opening Command Prompt")
    os.system("start cmd")


def open_explorer():
    speak("Opening File Explorer")
    os.system("explorer")


def open_control_panel():
    speak("Opening Control Panel")
    os.system("control")


def lock_pc():
    speak("Locking your computer")
    os.system("rundll32.exe user32.dll,LockWorkStation")


def shutdown_pc():
    speak("Shutting down your computer")
    os.system("shutdown /s /t 5")


def restart_pc():
    speak("Restarting your computer")
    os.system("shutdown /r /t 5")