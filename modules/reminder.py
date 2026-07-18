"""
modules/reminder.py
-------------------
Reminder Module
"""

import json
import os
import threading
import time

from assistant.speak import speak
from modules.logger import log_info

REMINDER_FILE = "data/reminders.json"


def load_reminders():

    if not os.path.exists(REMINDER_FILE):

        with open(REMINDER_FILE, "w") as f:
            json.dump([], f)

    with open(REMINDER_FILE, "r") as f:
        return json.load(f)


def save_reminders(reminders):

    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)


def add_reminder(task, minutes):

    reminders = load_reminders()

    reminder = {
        "task": task,
        "minutes": minutes
    }

    reminders.append(reminder)

    save_reminders(reminders)

    threading.Thread(
        target=run_reminder,
        args=(task, minutes),
        daemon=True
    ).start()

    log_info(f"Reminder Added: {task}")


def run_reminder(task, minutes):

    time.sleep(minutes * 60)

    speak(f"Reminder. {task}")


def list_reminders():

    return load_reminders()


def delete_reminder(index):

    reminders = load_reminders()

    if 0 <= index < len(reminders):

        reminders.pop(index)

        save_reminders(reminders)

        return True

    return False