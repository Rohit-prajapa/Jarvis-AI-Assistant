"""
modules/email.py
----------------
Handles email sending for Jarvis.
"""

import smtplib
from email.message import EmailMessage

from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD
from assistant.speak import speak


def send_email(receiver, subject, body):
    """
    Send an email using Gmail SMTP.
    """

    # Check email configuration
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        speak("Email configuration is missing.")
        return False

    try:
        # Create email
        message = EmailMessage()

        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver
        message["Subject"] = subject

        message.set_content(body)

        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            smtp.send_message(message)

        print("Email sent successfully.")
        speak("Email sent successfully.")

        return True

    except smtplib.SMTPAuthenticationError:
        print("Email authentication failed.")
        speak(
            "Email authentication failed. "
            "Please check your Gmail app password."
        )
        return False

    except Exception as error:
        print(f"Error sending email: {error}")
        speak("Sorry, I could not send the email.")
        return False