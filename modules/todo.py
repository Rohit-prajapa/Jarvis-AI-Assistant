"""
modules/todo.py
---------------
To-Do List Manager for Jarvis.
"""

import json
import os

from modules.logger import log_info, log_error


TODO_FILE = "data/todo.json"


def load_tasks():
    """Load all tasks from JSON file."""

    try:
        # Create data folder if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Create todo.json if it doesn't exist
        if not os.path.exists(TODO_FILE):
            with open(TODO_FILE, "w", encoding="utf-8") as file:
                json.dump([], file)

        with open(TODO_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError) as e:
        log_error(f"Error loading tasks: {e}")
        return []


def save_tasks(tasks):
    """Save tasks to JSON file."""

    try:
        os.makedirs("data", exist_ok=True)

        with open(TODO_FILE, "w", encoding="utf-8") as file:
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as e:
        log_error(f"Error saving tasks: {e}")
        return False


def add_task(task):
    """Add a new task."""

    tasks = load_tasks()

    new_task = {
        "task": task,
        "completed": False
    }

    tasks.append(new_task)

    if save_tasks(tasks):
        log_info(f"Task added: {task}")
        return True

    return False


def get_tasks():
    """Return all tasks."""

    return load_tasks()


def complete_task(index):
    """Mark a task as completed."""

    tasks = load_tasks()

    if 0 <= index < len(tasks):

        tasks[index]["completed"] = True

        if save_tasks(tasks):
            log_info(
                f"Task completed: {tasks[index]['task']}"
            )

            return True

    return False


def delete_task(index):
    """Delete a task."""

    tasks = load_tasks()

    if 0 <= index < len(tasks):

        deleted_task = tasks.pop(index)

        if save_tasks(tasks):
            log_info(
                f"Task deleted: {deleted_task['task']}"
            )

            return True

    return False


def clear_tasks():
    """Delete all tasks."""

    if save_tasks([]):

        log_info("All tasks cleared")

        return True

    return False