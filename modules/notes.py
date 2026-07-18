"""
modules/notes.py
----------------
Notes Manager for Jarvis.
"""

import json
import os
import datetime

from modules.logger import log_info, log_error


NOTES_FILE = "data/notes.json"


def load_notes():
    """Load all saved notes."""

    try:
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(NOTES_FILE):
            with open(
                NOTES_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump([], file)

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        log_error(f"Error loading notes: {e}")
        return []


def save_notes(notes):
    """Save notes to JSON file."""

    try:
        os.makedirs("data", exist_ok=True)

        with open(
            NOTES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                notes,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as e:
        log_error(f"Error saving notes: {e}")
        return False


def add_note(content):
    """Add a new note."""

    notes = load_notes()

    new_note = {
        "content": content,
        "created_at": datetime.datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    notes.append(new_note)

    if save_notes(notes):
        log_info(f"Note added: {content}")
        return True

    return False


def get_notes():
    """Return all saved notes."""

    return load_notes()


def get_note(index):
    """Return a specific note."""

    notes = load_notes()

    if 0 <= index < len(notes):
        return notes[index]

    return None


def delete_note(index):
    """Delete a specific note."""

    notes = load_notes()

    if 0 <= index < len(notes):

        deleted_note = notes.pop(index)

        if save_notes(notes):

            log_info(
                f"Note deleted: "
                f"{deleted_note['content']}"
            )

            return True

    return False


def clear_notes():
    """Delete all notes."""

    if save_notes([]):

        log_info("All notes cleared.")

        return True

    return False