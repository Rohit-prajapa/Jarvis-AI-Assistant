"""
modules/history.py
------------------
Command History Manager for Jarvis.
"""

import json
import os
import datetime

from modules.logger import log_info, log_error


HISTORY_FILE = "data/history.json"


def load_history():
    """Load command history."""

    try:
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(HISTORY_FILE):
            with open(
                HISTORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump([], file)

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        log_error(f"History Load Error: {e}")
        return []


def save_history(history):
    """Save command history."""

    try:
        os.makedirs("data", exist_ok=True)

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as e:
        log_error(f"History Save Error: {e}")
        return False


def add_command(command):
    """Add a command to history."""

    if not command:
        return False

    history = load_history()

    history.append(
        {
            "command": command,
            "timestamp": datetime.datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )
        }
    )

    # Keep only the latest 100 commands
    history = history[-100:]

    if save_history(history):
        log_info(f"Command saved to history: {command}")
        return True

    return False


def get_command_history():
    """Return saved command history."""

    return load_history()


def clear_command_history():
    """Delete all command history."""

    if save_history([]):
        log_info("Command history cleared.")
        return True

    return False