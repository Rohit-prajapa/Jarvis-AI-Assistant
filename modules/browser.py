"""
modules/browser.py
------------------
Browser related functions.
"""

import webbrowser
from assistant.speak import speak


def open_google():
    speak("Opening Google")
    webbrowser.open("https://www.google.com")


def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")


def open_github():
    speak("Opening GitHub")
    webbrowser.open("https://github.com")


def open_chatgpt():
    speak("Opening ChatGPT")
    webbrowser.open("https://chatgpt.com")


def open_linkedin():
    speak("Opening LinkedIn")
    webbrowser.open("https://www.linkedin.com")


def search_google(query):
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")


def search_youtube(query):
    speak(f"Searching YouTube for {query}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")