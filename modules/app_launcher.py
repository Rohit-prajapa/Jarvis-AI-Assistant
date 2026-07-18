"""
modules/app_launcher.py
-----------------------
Application Launcher Module for Jarvis.
"""

import os
import subprocess
import shutil

from assistant.speak import speak
from modules.logger import log_info, log_error


def launch_app(app_name):
    """
    Launch an installed Windows application.
    """

    try:
        app_name = app_name.lower().strip()

        # ==========================
        # Windows Built-in Apps
        # ==========================

        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "command prompt": "cmd.exe",
            "cmd": "cmd.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "file explorer": "explorer.exe",
        }

        if app_name in apps:

            subprocess.Popen(
                apps[app_name]
            )

            speak(
                f"Opening {app_name}."
            )

            log_info(
                f"Application opened: {app_name}"
            )

            return True

        # ==========================
        # Windows Settings
        # ==========================

        if app_name == "settings":

            os.startfile(
                "ms-settings:"
            )

            speak(
                "Opening Windows Settings."
            )

            log_info(
                "Windows Settings opened."
            )

            return True

        # ==========================
        # Apps Available in PATH
        # ==========================

        executable = shutil.which(
            app_name
        )

        if executable:

            subprocess.Popen(
                [executable]
            )

            speak(
                f"Opening {app_name}."
            )

            log_info(
                f"Application opened: {app_name}"
            )

            return True

        # ==========================
        # Common Applications
        # ==========================

        common_apps = {
            "chrome": [
                os.path.expandvars(
                    r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
                ),
                os.path.expandvars(
                    r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
                ),
                os.path.expandvars(
                    r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
                ),
            ],

            "edge": [
                os.path.expandvars(
                    r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
                ),
                os.path.expandvars(
                    r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
                ),
            ],

            "vs code": [
                os.path.expandvars(
                    r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe"
                ),
            ],

            "vscode": [
                os.path.expandvars(
                    r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe"
                ),
            ],

            "spotify": [
                os.path.expandvars(
                    r"%AppData%\Spotify\Spotify.exe"
                ),
            ],
        }

        if app_name in common_apps:

            for app_path in common_apps[app_name]:

                if os.path.exists(app_path):

                    subprocess.Popen(
                        [app_path]
                    )

                    speak(
                        f"Opening {app_name}."
                    )

                    log_info(
                        f"Application opened: {app_name}"
                    )

                    return True

        # Application not found
        speak(
            f"Sorry, I could not find {app_name} "
            f"on your computer."
        )

        log_error(
            f"Application not found: {app_name}"
        )

        return False

    except Exception as e:

        log_error(
            f"Application Launcher Error: {e}"
        )

        print(
            f"Application Launcher Error: {e}"
        )

        speak(
            f"Sorry, I could not open {app_name}."
        )

        return False