"""
assistant/commands.py
---------------------
Handles all voice commands.
"""


import datetime
import os
import pyjokes

from assistant.speak import speak
from assistant.ai_mode import AIMode
from modules.screenshot import take_screenshot
from modules.internet import check_internet
from modules.whatsapp import send_whatsapp_message
from assistant.news import get_latest_news
from modules.app_launcher import launch_app
from modules.logger import log_info, log_error

from modules.todo import (
    add_task,
    get_tasks,
    complete_task,
    delete_task,
    clear_tasks,
)
from assistant.alarm import (
    set_alarm,
    show_alarms,
    cancel_all_alarms,
)
from modules.file_manager import (
    create_folder,
    open_folder,
    search_file,
    open_file,
)
from modules.history import (
    add_command,
    get_command_history,
    clear_command_history,
)
from modules.notes import (
    add_note,
    get_notes,
    get_note,
    delete_note,
    clear_notes,
)
from modules.location import (
    get_public_ip,
    get_location,
)
from modules.clipboard import (
    read_clipboard,
    copy_to_clipboard,
    clear_clipboard,
)
from modules.system_info import (
    get_cpu_usage,
    get_ram_usage,
    get_battery_status,
    get_disk_usage,
    get_system_status,
)
from modules.browser import (
    open_google,
    open_youtube,
    open_github,
    open_chatgpt,
    open_linkedin,
    search_google,
    search_youtube,
)

from modules.notepad import (
    open_notepad,
    close_notepad,
)

from modules.calculator import (
    open_calculator,
    close_calculator,
)

from modules.system import (
    open_paint,
    open_cmd,
    open_control_panel,
    lock_pc,
    shutdown_pc,
    restart_pc,
)

from modules.explorer import (
    open_explorer,
    open_desktop,
    open_documents,
    open_downloads,
    open_pictures,
    open_music,
    open_videos,
)

from modules.media import (
    play_youtube,
    pause_media,
    next_track,
    previous_track,
    volume_up,
    volume_down,
    mute_volume,
)

from modules.memory import (
    remember,
    recall,
    forget,
    show_memory,
)

from modules.reminder import (
    add_reminder,
    list_reminders,
    delete_reminder,
)
from modules.weather import get_weather
from modules.ai import ask_ai
from modules.email import send_email
from modules.wikipedia_search import search_wikipedia


class CommandHandler:

    def execute(self, command):
        try:
            if not command:
                return

            command = command.lower().strip()
            log_info(f"Executing Command: {command}")
            add_command(command)

            # ==========================
            # Memory Commands
            # ==========================

            if command.startswith("remember"):
                data = command.replace("remember", "", 1).strip()

                if " is " in data:
                    key, value = data.split(" is ", 1)

                    key = key.strip()
                    value = value.strip()

                    remember(key, value)
                    speak(f"I'll remember that your {key} is {value}.")
                else:
                    speak(
                        "Please say it like, remember my name is Rohit."
                    )

                return

            if command.startswith("what do you remember"):
                memory = show_memory()

                if memory:
                    for key, value in memory.items():
                        speak(f"{key} is {value}")
                else:
                    speak("I don't remember anything yet.")

                return

            if command.startswith("forget"):
                key = command.replace("forget", "", 1).strip()

                if key:
                    if forget(key):
                        speak("Done.")
                    else:
                        speak("I couldn't find that.")
                else:
                    speak("Please tell me what you want me to forget.")

                return

            if command.startswith("what is my"):
                key = command.replace("what is my", "", 1).strip()

                if key:
                    value = recall(key)

                    if value:
                        speak(f"Your {key} is {value}")
                    else:
                        speak("I don't know that yet.")
                else:
                    speak("Please tell me what you want to know.")

                return

            # ==========================
            # AI Voice Mode
            # ==========================

            if command == "ai mode" or "start ai mode" in command:
                ai = AIMode()
                ai.start()
                return

            # ==========================
            # Reminder Commands
            # ==========================

            if command.startswith("remind me to"):
                try:
                    text = command.replace(
                        "remind me to", "", 1
                    ).strip()

                    task, minutes = text.rsplit(" in ", 1)

                    minutes = (
                        minutes
                        .replace("minutes", "")
                        .replace("minute", "")
                        .strip()
                    )

                    minutes = int(minutes)

                    add_reminder(task.strip(), minutes)

                    speak(
                        f"Okay. I will remind you to "
                        f"{task.strip()} in {minutes} minutes."
                    )

                except (ValueError, TypeError):
                    speak(
                        "Please say it like: "
                        "remind me to study in 30 minutes."
                    )

                return

            if "show reminders" in command:
                reminders = list_reminders()

                if not reminders:
                    speak("You have no reminders.")
                else:
                    for i, reminder in enumerate(
                        reminders, start=1
                    ):
                        speak(
                            f"Reminder {i}. "
                            f"{reminder['task']} in "
                            f"{reminder['minutes']} minutes."
                        )

                return

            if command.startswith("delete reminder"):
                try:
                    number = int(
                        command
                        .replace("delete reminder", "", 1)
                        .strip()
                    )

                    if delete_reminder(number - 1):
                        speak("Reminder deleted.")
                    else:
                        speak("Invalid reminder number.")

                except ValueError:
                    speak(
                        "Please tell me the reminder "
                        "number to delete."
                    )

                return

            # ==========================
            # AI Chat
            # ==========================

            if command.startswith("ask"):
                question = command.replace(
                    "ask", "", 1
                ).strip()

                if question:
                    ask_ai(question)
                else:
                    speak("What would you like to ask?")

                return

            # ==========================
            # Greetings
            # ==========================

            if "hello" in command:
                speak("Hello Rohit. How can I help you?")
                return

            # ==========================
            # Browser Commands
            # ==========================

            if "open google" in command:
                open_google()
                return

            if "open youtube" in command:
                open_youtube()
                return

            if "open github" in command:
                open_github()
                return

            if "open chatgpt" in command:
                open_chatgpt()
                return

            if "open linkedin" in command:
                open_linkedin()
                return

            if command.startswith("search google"):
                query = command.replace(
                    "search google", "", 1
                ).strip()

                if query:
                    search_google(query)
                else:
                    speak("What should I search on Google?")

                return

            if command.startswith("search youtube"):
                query = command.replace(
                    "search youtube", "", 1
                ).strip()

                if query:
                    search_youtube(query)
                else:
                    speak("What should I search on YouTube?")

                return

            # ==========================
            # Calculator Commands
            # ==========================

            if "close calculator" in command:
                close_calculator()
                return

            if (
                "open calculator" in command
                or command == "calculator"
            ):
                open_calculator()
                return

            # ==========================
            # Notepad Commands
            # ==========================

            if "close notepad" in command:
                close_notepad()
                return

            if (
                "open notepad" in command
                or command == "notepad"
            ):
                open_notepad()
                return

            # ==========================
            # System Commands
            # ==========================

            if "open paint" in command:
                open_paint()
                return

            if (
                "open cmd" in command
                or "open command prompt" in command
            ):
                open_cmd()
                return

            if "open control panel" in command:
                open_control_panel()
                return

            if "lock pc" in command:
                lock_pc()
                return

            if "shutdown pc" in command:
                shutdown_pc()
                return

            if "restart pc" in command:
                restart_pc()
                return

            # ==========================
            # Explorer Commands
            # ==========================

            if (
                "open file explorer" in command
                or "open explorer" in command
            ):
                open_explorer()
                return

            if "open desktop" in command:
                open_desktop()
                return

            if "open documents" in command:
                open_documents()
                return

            if "open downloads" in command:
                open_downloads()
                return

            if "open pictures" in command:
                open_pictures()
                return

            if "open music" in command:
                open_music()
                return

            if "open videos" in command:
                open_videos()
                return

            # ==========================
            # Media Commands
            # ==========================

            if command.startswith("play"):
                song = command.replace(
                    "play", "", 1
                ).strip()

                if song:
                    play_youtube(song)
                else:
                    speak("What should I play?")

                return

            if "pause" in command:
                pause_media()
                return

            if (
                "next song" in command
                or "next track" in command
            ):
                next_track()
                return

            if (
                "previous song" in command
                or "previous track" in command
            ):
                previous_track()
                return

            if "volume up" in command:
                volume_up()
                return

            if "volume down" in command:
                volume_down()
                return

            if "mute" in command:
                mute_volume()
                return

            # ==========================
            # Weather Commands
            # ==========================

            if command.startswith("weather in "):
                city = command.replace("weather in ", "", 1).strip()

                if city:
                    print(f"Getting weather for: {city}")
                    get_weather(city)
                else:
                    speak("Please tell me the city name.")

                return

            if command.startswith("weather "):
                city = command.replace("weather ", "", 1).strip()

                if city:
                    print(f"Getting weather for: {city}")
                    get_weather(city)
                else:
                    speak("Please tell me the city name.")

                return

            if command == "weather":
                speak("Please tell me the city name.")
                return

            # ==========================
            # Joke
            # ==========================

            if "joke" in command:
                joke = pyjokes.get_joke()
                speak(joke)
                return

            # ==========================
            # Email Commands
            # ==========================

            if command.startswith("send email to"):
                try:
                    receiver = command.replace(
                        "send email to", "", 1
                    ).strip()

                    if not receiver:
                        speak(
                            "Please say the email address "
                            "you want to send the email to."
                        )
                        return

                    subject = "Message from Jarvis"
                    body = "Hello, this email was sent by Jarvis."

                    speak(f"Sending email to {receiver}")

                    success = send_email(
                        receiver,
                        subject,
                        body
                    )

                    if success:
                        speak("Your email has been sent.")
                    else:
                        speak("I could not send your email.")

                except Exception as error:
                    print(f"Email command error: {error}")
                    speak(
                        "Sorry, something went wrong "
                        "while sending the email."
                    )

                return

            # ==========================
            # Alarm Commands
            # ==========================

            if command.startswith("set alarm for"):
                alarm_time = command.replace(
                    "set alarm for",
                    ""
                ).strip().upper()

                if alarm_time:
                    set_alarm(alarm_time)
                else:
                    speak(
                        "Please tell me what time "
                        "you want to set the alarm."
                    )

                return

            if "show alarms" in command:
                active_alarms = show_alarms()

                if active_alarms:
                    speak(
                        f"You have {len(active_alarms)} "
                        f"active alarms."
                    )

                    for alarm in active_alarms:
                        speak(
                            f"Alarm set for {alarm}"
                        )

                else:
                    speak(
                        "You have no active alarms."
                    )

                return

            if (
                "cancel all alarms" in command
                or "delete all alarms" in command
            ):
                cancel_all_alarms()
                return

            # ==========================
            # To-Do List Commands
            # ==========================

            if command.startswith("add") and "to my todo list" in command:
                task = command.replace(
                    "add",
                    "",
                    1
                ).replace(
                    "to my todo list",
                    ""
                ).strip()

                if task:
                    if add_task(task):
                        speak(
                            f"I added {task} to your todo list."
                        )
                    else:
                        speak(
                            "Sorry, I could not add the task."
                        )
                else:
                    speak(
                        "Please tell me what task you want to add."
                    )

                return

            # ==========================
            # Show Tasks
            # ==========================

            if (
                "show my tasks" in command
                or "show todo list" in command
                or "show my todo list" in command
            ):
                tasks = get_tasks()

                if not tasks:
                    speak(
                        "Your todo list is empty."
                    )
                else:
                    speak(
                        f"You have {len(tasks)} tasks."
                    )

                    for index, task in enumerate(
                        tasks,
                        start=1
                    ):
                        status = (
                            "completed"
                            if task["completed"]
                            else "pending"
                        )

                        speak(
                            f"Task {index}. "
                            f"{task['task']}. "
                            f"Status {status}."
                        )

                return

            # ==========================
            # Complete Task
            # ==========================

            if command.startswith("complete task"):
                try:
                    number = int(
                        command.replace(
                            "complete task",
                            ""
                        ).strip()
                    )

                    if complete_task(number - 1):
                        speak(
                            f"Task {number} marked as completed."
                        )
                    else:
                        speak(
                            "Invalid task number."
                        )

                except ValueError:
                    speak(
                        "Please tell me the task number."
                    )

                return

            # ==========================
            # Delete Task
            # ==========================

            if command.startswith("delete task"):
                try:
                    number = int(
                        command.replace(
                            "delete task",
                            ""
                        ).strip()
                    )

                    if delete_task(number - 1):
                        speak(
                            f"Task {number} deleted."
                        )
                    else:
                        speak(
                            "Invalid task number."
                        )

                except ValueError:
                    speak(
                        "Please tell me the task number."
                    )

                return

            # ==========================
            # Clear All Tasks
            # ==========================

            if (
                "clear all tasks" in command
                or "delete all tasks" in command
            ):
                if clear_tasks():
                    speak(
                        "All tasks have been cleared."
                    )
                else:
                    speak(
                        "Sorry, I could not clear your tasks."
                    )

                return

            # ==========================
            # Wikipedia Commands
            # ==========================

            if command.startswith("search wikipedia for"):
                query = command.replace(
                    "search wikipedia for",
                    "",
                    1
                ).strip()

                if query:
                    search_wikipedia(query)
                else:
                    speak(
                        "What should I search on Wikipedia?"
                    )

                return

            if command.startswith("wikipedia"):
                query = command.replace(
                    "wikipedia",
                    "",
                    1
                ).strip()

                if query:
                    search_wikipedia(query)
                else:
                    speak(
                        "What should I search on Wikipedia?"
                    )

                return

            # ==========================
            # File Manager Commands
            # ==========================

            if command.startswith("create folder"):
                folder_name = command.replace(
                    "create folder",
                    "",
                    1
                ).strip()

                if folder_name:
                    create_folder(folder_name)
                else:
                    speak(
                        "Please tell me the folder name."
                    )

                return

            if command.startswith("open folder"):
                folder_name = command.replace(
                    "open folder",
                    "",
                    1
                ).strip()

                if folder_name:
                    open_folder(folder_name)
                else:
                    speak(
                        "Please tell me which folder to open."
                    )

                return

            if command.startswith("search file"):
                file_name = command.replace(
                    "search file",
                    "",
                    1
                ).strip()

                if file_name:
                    file_path = search_file(file_name)

                    if file_path:
                        speak(
                            f"I found the file {file_name}."
                        )
                        print(
                            f"File Location: {file_path}"
                        )
                    else:
                        speak(
                            f"I could not find {file_name}."
                        )
                else:
                    speak(
                        "Please tell me the file name."
                    )

                return

            if command.startswith("open file"):
                file_name = command.replace(
                    "open file",
                    "",
                    1
                ).strip()

                if file_name:
                    open_file(file_name)
                else:
                    speak(
                        "Please tell me which file to open."
                    )

                return

            # ==========================
            # System Information
            # ==========================

            if (
                "cpu usage" in command
                or "check cpu" in command
            ):
                get_cpu_usage()
                return

            if (
                "ram usage" in command
                or "memory usage" in command
            ):
                get_ram_usage()
                return

            if (
                "battery status" in command
                or "battery percentage" in command
                or command == "battery"
            ):
                get_battery_status()
                return

            if (
                "disk usage" in command
                or "storage status" in command
            ):
                get_disk_usage()
                return

            if (
                "system status" in command
                or "check my computer" in command
            ):
                get_system_status()
                return

            # ==========================
            # Screenshot Commands
            # ==========================

            if (
                "take a screenshot" in command
                or "take screenshot" in command
                or "capture screen" in command
                or command == "screenshot"
            ):
                take_screenshot()
                return

            # ==========================
            # Internet Status Commands
            # ==========================

            if (
                "check internet" in command
                or "internet status" in command
                or "check connection" in command
                or "am i online" in command
            ):
                check_internet()
                return

            # ==========================
            # WhatsApp Commands
            # ==========================

            if (
                "send whatsapp message" in command
                or "send message on whatsapp" in command
            ):
                speak(
                    "Please type the phone number "
                    "with country code."
                )

                phone_number = input(
                    "Phone Number: "
                ).strip()

                speak(
                    "Please type your message."
                )

                message = input(
                    "Message: "
                ).strip()

                if phone_number and message:
                    speak(
                        "Your WhatsApp message is ready. "
                        "Should I send it?"
                    )

                    confirmation = input(
                        "Send message? (yes/no): "
                    ).lower().strip()

                    if confirmation == "yes":
                        send_whatsapp_message(
                            phone_number,
                            message
                        )
                    else:
                        speak(
                            "WhatsApp message cancelled."
                        )
                else:
                    speak(
                        "Phone number and message "
                        "cannot be empty."
                    )

                return

            # ==========================
            # News Commands
            # ==========================

            if (
                "latest news" in command
                or "tell me the news" in command
                or "today's news" in command
                or "read news" in command
            ):
                get_latest_news()
                return

            # ==========================
            # Notes Commands
            # ==========================

            if (
                command == "take a note"
                or command == "create note"
                or command == "write a note"
            ):
                speak("Please type your note.")

                note_content = input(
                    "Note: "
                ).strip()

                if note_content:
                    if add_note(note_content):
                        speak(
                            "Your note has been saved."
                        )
                    else:
                        speak(
                            "Sorry, I could not save your note."
                        )
                else:
                    speak(
                        "The note cannot be empty."
                    )

                return

            # ==========================
            # Show All Notes
            # ==========================

            if (
                "show my notes" in command
                or "list my notes" in command
            ):
                notes = get_notes()

                if not notes:
                    speak(
                        "You have no saved notes."
                    )
                else:
                    speak(
                        f"You have {len(notes)} saved notes."
                    )

                    for index, note in enumerate(
                        notes,
                        start=1
                    ):
                        print(
                            f"{index}. "
                            f"{note['content']} "
                            f"({note['created_at']})"
                        )

                return

            # ==========================
            # Read Specific Note
            # ==========================

            if command.startswith("read note"):
                try:
                    number = int(
                        command.replace(
                            "read note",
                            "",
                            1
                        ).strip()
                    )

                    note = get_note(
                        number - 1
                    )

                    if note:
                        speak(
                            f"Note {number}. "
                            f"{note['content']}"
                        )
                    else:
                        speak(
                            "Invalid note number."
                        )

                except ValueError:
                    speak(
                        "Please tell me the note number."
                    )

                return

            # ==========================
            # Delete Specific Note
            # ==========================

            if command.startswith("delete note"):
                try:
                    number = int(
                        command.replace(
                            "delete note",
                            "",
                            1
                        ).strip()
                    )

                    if delete_note(number - 1):
                        speak(
                            f"Note {number} deleted."
                        )
                    else:
                        speak(
                            "Invalid note number."
                        )

                except ValueError:
                    speak(
                        "Please tell me the note number."
                    )

                return

            # ==========================
            # Clear All Notes
            # ==========================

            if (
                "clear all notes" in command
                or "delete all notes" in command
            ):
                confirmation = input(
                    "Delete all notes? (yes/no): "
                ).lower().strip()

                if confirmation == "yes":
                    if clear_notes():
                        speak(
                            "All your notes have been deleted."
                        )
                else:
                    speak(
                        "Operation cancelled."
                    )

                return

            # ==========================
            # Clipboard Commands
            # ==========================

            if (
                "read clipboard" in command
                or "what is in my clipboard" in command
            ):
                read_clipboard()
                return

            if command.startswith("copy text"):
                text = command.replace(
                    "copy text",
                    "",
                    1
                ).strip()

                if text:
                    copy_to_clipboard(text)
                else:
                    speak("Please type the text you want to copy.")

                    text = input("Text: ").strip()

                    if text:
                        copy_to_clipboard(text)
                    else:
                        speak("No text was provided.")

                return

            if (
                "clear clipboard" in command
                or "delete clipboard" in command
            ):
                clear_clipboard()
                return

            # ==========================
            # IP Address Commands
            # ==========================

            if (
                "what is my ip" in command
                or "my ip address" in command
                or "check my ip" in command
            ):
                get_public_ip()
                return

            # ==========================
            # Location Commands
            # ==========================

            if (
                "where am i" in command
                or "what is my location" in command
                or "check my location" in command
            ):
                get_location()
                return

            # ==========================
            # Command History
            # ==========================

            if (
                "show command history" in command
                or "show my command history" in command
            ):
                history = get_command_history()

                if not history:
                    speak(
                        "Your command history is empty."
                    )
                else:
                    print("\n========== COMMAND HISTORY ==========\n")

                    for index, item in enumerate(
                        history,
                        start=1
                    ):
                        print(
                            f"{index}. "
                            f"{item['command']} "
                            f"- {item['timestamp']}"
                        )

                    print("\n=====================================\n")

                    speak(
                        f"You have {len(history)} "
                        f"commands in your history. "
                        f"I have displayed them on the screen."
                    )

                return

            # ==========================
            # Clear Command History
            # ==========================

            if "clear command history" in command:
                if clear_command_history():
                    speak(
                        "Your command history has been cleared."
                    )
                else:
                    speak(
                        "Sorry, I could not clear "
                        "your command history."
                    )

                return

            # ==========================
            # Application Launcher
            # (kept last so it doesn't
            # swallow the specific "open X"
            # commands handled above)
            # ==========================

            if command.startswith("open"):
                app_name = command.replace(
                    "open",
                    "",
                    1
                ).strip()

                if app_name:
                    launch_app(app_name)
                else:
                    speak(
                        "Please tell me which application "
                        "you want to open."
                    )

                return

            # ==========================
            # AI Fallback
            # ==========================

            try:
                log_info(f"Sending unknown command to AI: {command}")

                ask_ai(command)

            except Exception as e:
                log_error(f"AI fallback error: {e}")
                speak(
                    "Sorry, I could not answer that question right now."
                )

            return

        except Exception as e:
            log_error(f"Command Execution Error: {e}")
            print(f"Command Execution Error: {e}")
            speak(
                "Sorry, something went wrong "
                "while executing that command."
            )