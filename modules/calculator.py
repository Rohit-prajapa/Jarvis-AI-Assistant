"""
modules/calculator.py
---------------------
Calculator related functions.
"""

import os
from assistant.speak import speak


def open_calculator():
    """
    Open Windows Calculator.
    """
    speak("Opening Calculator")
    os.system("calc")


def close_calculator():
    """
    Close Windows Calculator.
    """
    speak("Closing Calculator")
    os.system("taskkill /f /im CalculatorApp.exe")
    os.system("taskkill /f /im Calculator.exe")