"""
modules/file_manager.py
-----------------------
File Manager Module for Jarvis.
"""

import os

from assistant.speak import speak
from modules.logger import log_info, log_error


# User home directory
HOME_DIRECTORY = os.path.expanduser("~")


def create_folder(folder_name):
    """
    Create a new folder on the Desktop.
    """

    try:
        desktop = os.path.join(
            HOME_DIRECTORY,
            "Desktop"
        )

        folder_path = os.path.join(
            desktop,
            folder_name
        )

        if os.path.exists(folder_path):
            speak(
                f"The folder {folder_name} already exists."
            )
            return False

        os.makedirs(folder_path)

        log_info(
            f"Folder created: {folder_path}"
        )

        speak(
            f"Folder {folder_name} created successfully."
        )

        return True

    except Exception as e:

        log_error(
            f"Create Folder Error: {e}"
        )

        speak(
            "Sorry, I could not create the folder."
        )

        return False


def open_folder(folder_name):
    """
    Find and open a folder.
    """

    try:
        search_locations = [
            os.path.join(HOME_DIRECTORY, "Desktop"),
            os.path.join(HOME_DIRECTORY, "Documents"),
            os.path.join(HOME_DIRECTORY, "Downloads"),
        ]

        for location in search_locations:

            folder_path = os.path.join(
                location,
                folder_name
            )

            if os.path.isdir(folder_path):

                os.startfile(folder_path)

                log_info(
                    f"Folder opened: {folder_path}"
                )

                speak(
                    f"Opening folder {folder_name}"
                )

                return True

        speak(
            f"I could not find the folder {folder_name}."
        )

        return False

    except Exception as e:

        log_error(
            f"Open Folder Error: {e}"
        )

        speak(
            "Sorry, I could not open the folder."
        )

        return False


def search_file(file_name):
    """
    Search for a file inside common user folders.
    """

    search_locations = [
        os.path.join(HOME_DIRECTORY, "Desktop"),
        os.path.join(HOME_DIRECTORY, "Documents"),
        os.path.join(HOME_DIRECTORY, "Downloads"),
    ]

    try:

        for location in search_locations:

            if not os.path.exists(location):
                continue

            for root, dirs, files in os.walk(location):

                for file in files:

                    if file_name.lower() in file.lower():

                        file_path = os.path.join(
                            root,
                            file
                        )

                        log_info(
                            f"File found: {file_path}"
                        )

                        return file_path

        log_info(
            f"File not found: {file_name}"
        )

        return None

    except Exception as e:

        log_error(
            f"File Search Error: {e}"
        )

        return None


def open_file(file_name):
    """
    Search for and open a file.
    """

    try:

        file_path = search_file(file_name)

        if file_path:

            speak(
                f"Opening {os.path.basename(file_path)}"
            )

            os.startfile(file_path)

            log_info(
                f"File opened: {file_path}"
            )

            return True

        speak(
            f"I could not find {file_name}."
        )

        return False

    except Exception as e:

        log_error(
            f"Open File Error: {e}"
        )

        speak(
            "Sorry, I could not open the file."
        )

        return False