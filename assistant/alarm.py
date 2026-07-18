"""
assistant/alarm.py
------------------
Alarm system for Jarvis.
"""

import datetime
import threading
import time

from assistant.speak import speak
from modules.logger import log_info, log_error


# Store active alarms
alarms = []


def set_alarm(alarm_time):
    """
    Set a new alarm.
    Example alarm_time: 07:30 AM
    """

    try:
        # Validate time format
        datetime.datetime.strptime(
            alarm_time,
            "%I:%M %p"
        )

        alarms.append(alarm_time)

        # Start alarm in background
        thread = threading.Thread(
            target=alarm_worker,
            args=(alarm_time,),
            daemon=True
        )

        thread.start()

        log_info(
            f"Alarm set for {alarm_time}"
        )

        speak(
            f"Alarm has been set for {alarm_time}"
        )

        return True

    except ValueError:

        log_error(
            f"Invalid alarm time: {alarm_time}"
        )

        speak(
            "Invalid time format. "
            "Please use a time like 7:30 AM."
        )

        return False


def alarm_worker(alarm_time):
    """
    Continuously check the current time
    until the alarm time is reached.
    """

    while True:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        if current_time == alarm_time:

            speak(
                "Alarm ringing. "
                "Wake up! It's time."
            )

            log_info(
                f"Alarm triggered: {alarm_time}"
            )

            if alarm_time in alarms:
                alarms.remove(alarm_time)

            break

        # Check every second
        time.sleep(1)


def show_alarms():
    """
    Return all active alarms.
    """

    return alarms.copy()


def cancel_all_alarms():
    """
    Remove all alarms.
    """

    alarms.clear()

    log_info(
        "All alarms cancelled"
    )

    speak(
        "All alarms have been cancelled."
    )