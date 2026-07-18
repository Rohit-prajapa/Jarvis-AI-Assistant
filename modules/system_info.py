"""
modules/system_info.py
----------------------
System Information Module for Jarvis.
"""

import psutil

from assistant.speak import speak
from modules.logger import log_info, log_error


def get_cpu_usage():
    """Get current CPU usage."""

    try:
        cpu_usage = psutil.cpu_percent(interval=1)

        message = f"Current CPU usage is {cpu_usage} percent."

        log_info(message)
        speak(message)

        return cpu_usage

    except Exception as e:
        log_error(f"CPU Usage Error: {e}")
        speak("Sorry, I could not get the CPU usage.")
        return None


def get_ram_usage():
    """Get current RAM usage."""

    try:
        memory = psutil.virtual_memory()

        ram_usage = memory.percent

        message = f"Current RAM usage is {ram_usage} percent."

        log_info(message)
        speak(message)

        return ram_usage

    except Exception as e:
        log_error(f"RAM Usage Error: {e}")
        speak("Sorry, I could not get the RAM usage.")
        return None


def get_battery_status():
    """Get battery percentage and charging status."""

    try:
        battery = psutil.sensors_battery()

        if battery is None:
            speak("Battery information is not available.")
            return None

        percentage = battery.percent

        if battery.power_plugged:
            status = "charging"
        else:
            status = "not charging"

        message = (
            f"Battery is at {percentage} percent "
            f"and is currently {status}."
        )

        log_info(message)
        speak(message)

        return percentage

    except Exception as e:
        log_error(f"Battery Status Error: {e}")
        speak("Sorry, I could not get the battery information.")
        return None


def get_disk_usage():
    """Get disk usage for the C drive."""

    try:
        disk = psutil.disk_usage("C:\\")

        used_percentage = disk.percent

        free_gb = disk.free / (1024 ** 3)

        message = (
            f"Your C drive is {used_percentage} percent full. "
            f"You have {free_gb:.1f} gigabytes of free space."
        )

        log_info(message)
        speak(message)

        return used_percentage

    except Exception as e:
        log_error(f"Disk Usage Error: {e}")
        speak("Sorry, I could not get the disk information.")
        return None


def get_system_status():
    """Get complete system status."""

    speak("Checking your system status.")

    get_cpu_usage()
    get_ram_usage()
    get_battery_status()
    get_disk_usage()

    log_info("Complete system status checked.")