"""
modules/chat_history.py
-----------------------
Conversation History Manager
"""

import json
import os

HISTORY_FILE = "data/chat_history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def add_message(role, content):

    history = load_history()

    history.append({
        "role": role,
        "content": content
    })

    # Keep only last 20 messages
    history = history[-20:]

    save_history(history)


def get_history():
    return load_history()


def clear_history():
    save_history([])