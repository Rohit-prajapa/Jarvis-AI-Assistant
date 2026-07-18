"""
modules/whatsapp.py
-------------------
WhatsApp Messaging Module for Jarvis.
"""

import datetime
import pywhatkit

from assistant.speak import speak
from modules.logger import log_info, log_error


def send_whatsapp_message(phone_number, message):
    """
    Send a WhatsApp message using WhatsApp Web.

    Phone number must include country code.
    Example for India: +919876543210
    """

    try:
        # Validate basic input
        if not phone_number or not message:
            speak("Phone number and message are required.")
            return False

        # Add Indian country code if only
        # a 10-digit number is provided
        if phone_number.isdigit() and len(phone_number) == 10:
            phone_number = "+91" + phone_number

        # Get current time
        now = datetime.datetime.now()

        # Schedule message 2 minutes ahead
        send_time = now + datetime.timedelta(minutes=2)

        hour = send_time.hour
        minute = send_time.minute

        speak("Opening WhatsApp Web.")

        log_info(
            f"WhatsApp message scheduled for {phone_number}"
        )

        pywhatkit.sendwhatmsg(
            phone_number,
            message,
            hour,
            minute,
            wait_time=15,
            tab_close=True,
            close_time=3
        )

        speak("WhatsApp message sent successfully.")

        log_info(
            f"WhatsApp message sent to {phone_number}"
        )

        return True

    except Exception as e:

        log_error(
            f"WhatsApp Error: {e}"
        )

        print(
            f"WhatsApp Error: {e}"
        )

        speak(
            "Sorry, I could not send the WhatsApp message."
        )

        return False