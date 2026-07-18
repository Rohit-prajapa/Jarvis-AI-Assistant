"""
config.py
---------
Central configuration file for Jarvis.
"""

import os
from dotenv import load_dotenv


# ===============================
# Load Environment Variables
# ===============================

load_dotenv()


# ===============================
# API Keys
# ===============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ===============================
# Email Configuration
# ===============================

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


# ===============================
# Jarvis Settings
# ===============================

ASSISTANT_NAME = "Jarvis"
USER_NAME = "Rohit"

VOICE_RATE = 180
VOICE_VOLUME = 1.0

LANGUAGE = "en"
DEFAULT_CITY = "Pune"


# ===============================
# Conversation Settings
# ===============================

CONVERSATION_TIMEOUT = 30  # seconds

EXIT_COMMANDS = [
    "stop listening",
    "go to sleep",
    "sleep",
    "goodbye",
    "bye",
]