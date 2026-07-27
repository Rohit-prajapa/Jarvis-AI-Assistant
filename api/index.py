"""
api/index.py
------------
Jarvis AI Assistant Web App
Flask + Google Gemini + Vercel
"""

import os

from flask import Flask, jsonify, render_template_string, request
from google import genai


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# WEB INTERFACE
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="theme-color"
        content="#02070d"
    >

    <title>Jarvis AI Assistant</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;

            background:
                radial-gradient(
                    circle at top,
                    #071c2c 0%,
                    #02070d 45%,
                    #000000 100%
                );

            color: white;

            font-family:
                Arial,
                Helvetica,
                sans-serif;
        }

        .container {
            width: 92%;
            max-width: 900px;

            min-height: 100vh;

            margin: auto;

            display: flex;
            flex-direction: column;
            justify-content: center;

            padding: 30px 0;
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        h1 {
            color: #00eaff;

            font-size: 48px;
            letter-spacing: 8px;

            text-shadow:
                0 0 10px #00eaff;

            margin-bottom: 8px;
        }

        .subtitle {
            color: #8b9aaa;
            font-size: 16px;
        }

        /* ==================================================
           JARVIS CIRCLE
        ================================================== */

        .jarvis-circle {
            width: 145px;
            height: 145px;

            margin: 20px auto;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 50%;

            border: 4px solid #00eaff;

            font-size: 52px;

            background:
                radial-gradient(
                    circle,
                    rgba(0, 234, 255, 0.15),
                    rgba(0, 0, 0, 0.5)
                );

            box-shadow:
                0 0 15px #00eaff,
                0 0 35px rgba(0, 234, 255, 0.45),
                inset 0 0 25px rgba(0, 234, 255, 0.25);

            animation:
                jarvisPulse 2s ease-in-out infinite;
        }

        @keyframes jarvisPulse {

            0% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.05);
            }

            100% {
                transform: scale(1);
            }
        }

        /* ==================================================
           CHAT
        ================================================== */

        #chat {
            width: 100%;
            height: 330px;

            overflow-y: auto;

            padding: 20px;
            margin-top: 15px;

            background:
                rgba(4, 13, 22, 0.92);

            border:
                1px solid rgba(0, 234, 255, 0.20);

            border-radius: 16px;

            box-shadow:
                0 0 20px rgba(0, 234, 255, 0.07);

            scroll-behavior: smooth;
        }

        #chat::-webkit-scrollbar {
            width: 7px;
        }

        #chat::-webkit-scrollbar-thumb {
            background: #00eaff;
            border-radius: 10px;
        }

        .message {
            padding: 12px 15px;
            margin-bottom: 12px;

            border-radius: 10px;

            line-height: 1.5;

            word-wrap: break-word;
            white-space: pre-wrap;
        }

        .user-message {
            color: white;

            background:
                rgba(255, 255, 255, 0.05);

            border-left:
                3px solid white;
        }

        .jarvis-message {
            color: #00eaff;

            background:
                rgba(0, 234, 255, 0.05);

            border-left:
                3px solid #00eaff;
        }

        .sender {
            font-weight: bold;
        }

        /* ==================================================
           INPUT
        ================================================== */

        .input-area {
            display: flex;
            align-items: center;

            gap: 10px;

            margin-top: 15px;
        }

        #message {
            flex: 1;
            min-width: 0;

            padding: 16px 20px;

            background: #07111c;

            border:
                1px solid #00eaff;

            border-radius: 30px;

            outline: none;

            color: white;

            font-size: 16px;
        }

        #message:focus {
            box-shadow:
                0 0 15px rgba(0, 234, 255, 0.35);
        }

        #message::placeholder {
            color: #71808d;
        }

        button {
            border: none;
            outline: none;

            cursor: pointer;

            border-radius: 30px;

            padding: 15px 22px;

            background: #00eaff;
            color: #001018;

            font-weight: bold;
            font-size: 15px;

            transition: 0.2s;
        }

        button:hover {
            transform: translateY(-2px);

            box-shadow:
                0 0 18px rgba(0, 234, 255, 0.60);
        }

        button:disabled {
            opacity: 0.5;

            cursor: not-allowed;

            transform: none;
        }

        #micButton {
            width: 55px;
            height: 55px;

            padding: 0;

            font-size: 21px;
        }

        #micButton.listening {
            animation:
                micPulse 1s infinite;
        }

        @keyframes micPulse {

            0% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.12);
            }

            100% {
                transform: scale(1);
            }
        }

        /* ==================================================
           STATUS
        ================================================== */

        #status {
            margin-top: 14px;

            text-align: center;

            color: #00ff88;

            font-size: 14px;
        }

        .footer {
            text-align: center;

            margin-top: 15px;

            color: #53616d;

            font-size: 12px;
        }

        /* ==================================================
           MOBILE
        ================================================== */

        @media (max-width: 650px) {

            .container {
                width: 95%;
                padding: 15px 0;
            }

            h1 {
                font-size: 36px;
                letter-spacing: 5px;
            }

            .jarvis-circle {
                width: 110px;
                height: 110px;

                font-size: 40px;
            }

            #chat {
                height: 350px;
                padding: 15px;
            }

            .input-area {
                gap: 7px;
            }

            #message {
                padding: 14px 16px;
            }

            button {
                padding: 14px 16px;
            }

            #micButton {
                width: 50px;
                height: 50px;
            }
        }

    </style>

</head>


<body>


<div class="container">


    <div class="header">

        <h1>JARVIS</h1>

        <p class="subtitle">
            AI Assistant • Powered by Gemini
        </p>

    </div>


    <div
        class="jarvis-circle"
        id="jarvisCircle"
    >
        🤖
    </div>


    <div id="chat">

        <div class="message jarvis-message">

            <span class="sender">
                Jarvis:
            </span>

            Hello! I'm Jarvis. How can I help you?

        </div>

    </div>


    <div class="input-area">

        <input
            id="message"
            type="text"
            placeholder="Ask Jarvis anything..."
            autocomplete="off"
        >

        <button
            id="sendButton"
            type="button"
        >
            Send
        </button>

        <button
            id="micButton"
            type="button"
            title="Talk to Jarvis"
        >
            🎤
        </button>

    </div>


    <div id="status">
        ● Jarvis Online
    </div>


    <div class="footer">
        Jarvis AI Assistant • Gemini
    </div>


</div>


<script>


// ============================================================
// ELEMENTS
// ============================================================

const input =
    document.getElementById("message");

const chat =
    document.getElementById("chat");

const sendButton =
    document.getElementById("sendButton");

const micButton =
    document.getElementById("micButton");

const statusElement =
    document.getElementById("status");


// ============================================================
// VOICE MODE
// ============================================================

// false = typed command/question
// true = microphone command/question

let voiceMode = false;


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(sender, text, type) {

    const message =
        document.createElement("div");

    message.classList.add(
        "message"
    );


    if (type === "user") {

        message.classList.add(
            "user-message"
        );

    } else {

        message.classList.add(
            "jarvis-message"
        );

    }


    const senderElement =
        document.createElement("span");

    senderElement.className =
        "sender";

    senderElement.textContent =
        sender + ": ";


    const textElement =
        document.createElement("span");

    textElement.textContent =
        text;


    message.appendChild(
        senderElement
    );

    message.appendChild(
        textElement
    );

    chat.appendChild(
        message
    );


    chat.scrollTop =
        chat.scrollHeight;


    return message;
}


// ============================================================
// CLEAN COMMAND
// ============================================================

function cleanCommand(text) {

    return text
        .toLowerCase()
        .replace(/jarvis/g, "")
        .replace(/please/g, "")
        .replace(/[.,!?]/g, "")
        .trim();
}


// ============================================================
// WEBSITE COMMANDS
// ============================================================

function getWebsiteCommand(userMessage) {

    const command =
        cleanCommand(
            userMessage
        );


    const websites = {

        youtube: {
            url:
                "https://www.youtube.com",
            label:
                "YouTube"
        },

        google: {
            url:
                "https://www.google.com",
            label:
                "Google"
        },

        gmail: {
            url:
                "https://mail.google.com",
            label:
                "Gmail"
        },

        github: {
            url:
                "https://github.com",
            label:
                "GitHub"
        },

        linkedin: {
            url:
                "https://www.linkedin.com",
            label:
                "LinkedIn"
        },

        instagram: {
            url:
                "https://www.instagram.com",
            label:
                "Instagram"
        },

        facebook: {
            url:
                "https://www.facebook.com",
            label:
                "Facebook"
        },

        spotify: {
            url:
                "https://open.spotify.com",
            label:
                "Spotify"
        }

    };


    /*
        Handle possible speech recognition
        versions of YouTube.
    */

    let normalizedCommand =
        command
            .replace(
                /you tube/g,
                "youtube"
            )
            .replace(
                /u tube/g,
                "youtube"
            );


    for (
        const [name, website]
        of Object.entries(websites)
    ) {

        if (
            normalizedCommand.includes(
                "open " + name
            ) ||
            normalizedCommand.includes(
                "launch " + name
            )
        ) {

            return {

                handled: true,

                url:
                    website.url,

                label:
                    website.label,

                message:
                    "Opening " +
                    website.label

            };

        }

    }


    return {
        handled: false
    };
}


// ============================================================
// WEBSITE NAVIGATION
// ============================================================

function openWebsite(
    website,
    shouldSpeak
) {

    addMessage(
        "Jarvis",
        website.message + "...",
        "jarvis"
    );


    /*
        IMPORTANT:

        Same-tab navigation is used here.

        Browser popup blockers can block
        window.open() after microphone
        recognition.

        window.location.href is more
        reliable.
    */


    if (shouldSpeak) {

        /*
            User spoke the command.

            Jarvis first says:
            "Opening YouTube"

            Then browser navigates.
        */

        speakText(
            website.message,
            function() {

                window.location.href =
                    website.url;

            }
        );

    } else {

        /*
            User typed the command.

            No speech.
            Open immediately.
        */

        window.location.href =
            website.url;

    }
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {


    const userMessage =
        input.value.trim();


    if (!userMessage) {

        return;

    }


    /*
        Save current voice mode.
    */

    const shouldSpeak =
        voiceMode;


    /*
        Reset for next message.
    */

    voiceMode =
        false;


    // Show user's message.

    addMessage(
        "You",
        userMessage,
        "user"
    );


    input.value =
        "";


    // ========================================================
    // WEBSITE COMMAND CHECK
    // ========================================================

    const website =
        getWebsiteCommand(
            userMessage
        );


    if (website.handled) {

        openWebsite(
            website,
            shouldSpeak
        );

        return;
    }


    // ========================================================
    // NORMAL GEMINI QUESTION
    // ========================================================

    const thinkingMessage =
        addMessage(
            "Jarvis",
            "Thinking...",
            "jarvis"
        );


    sendButton.disabled =
        true;

    micButton.disabled =
        true;


    statusElement.textContent =
        "◌ Jarvis is thinking...";


    try {


        const response =
            await fetch(
                "/api/chat",
                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            {
                                message:
                                    userMessage
                            }
                        )

                }
            );


        let data;


        try {

            data =
                await response.json();

        }

        catch (error) {

            throw new Error(
                "Invalid response from Jarvis server."
            );

        }


        if (
            thinkingMessage &&
            thinkingMessage.isConnected
        ) {

            thinkingMessage.remove();

        }


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Jarvis could not process the request."
            );

        }


        const reply =
            data.reply ||
            "Sorry, I couldn't generate a response.";


        addMessage(
            "Jarvis",
            reply,
            "jarvis"
        );


        statusElement.textContent =
            "● Jarvis Online";


        /*
            SPEAK ONLY WHEN USER
            USED MICROPHONE.
        */

        if (shouldSpeak) {

            speakText(
                reply
            );

        }

    }

    catch (error) {


        if (
            thinkingMessage &&
            thinkingMessage.isConnected
        ) {

            thinkingMessage.remove();

        }


        addMessage(
            "Jarvis",
            "Error: " +
            error.message,
            "jarvis"
        );


        statusElement.textContent =
            "● Jarvis Online";


        console.error(
            "Jarvis Error:",
            error
        );

    }

    finally {


        sendButton.disabled =
            false;


        micButton.disabled =
            false;


        input.focus();

    }

}


// ============================================================
// TEXT TO SPEECH
// ============================================================

function speakText(
    text,
    onComplete = null
) {


    if (
        !("speechSynthesis" in window)
    ) {

        console.log(
            "Text-to-speech is not supported."
        );


        /*
            If speech isn't available,
            still continue the requested
            action.
        */

        if (onComplete) {

            onComplete();

        }


        return;

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.lang =
        "en-IN";


    speech.rate =
        1;


    speech.pitch =
        1;


    speech.volume =
        1;


    const voices =
        window.speechSynthesis.getVoices();


    const preferredVoice =

        voices.find(
            function(voice) {

                return (
                    voice.lang ===
                    "en-IN"
                );

            }
        )

        ||

        voices.find(
            function(voice) {

                return (
                    voice.lang &&
                    voice.lang.startsWith(
                        "en"
                    )
                );

            }
        );


    if (preferredVoice) {

        speech.voice =
            preferredVoice;

    }


    speech.onstart =
        function() {


            statusElement.textContent =
                "🔊 Jarvis is speaking...";

        };


    speech.onend =
        function() {


            statusElement.textContent =
                "● Jarvis Online";


            if (onComplete) {

                onComplete();

            }

        };


    speech.onerror =
        function(event) {


            console.error(
                "Speech Error:",
                event
            );


            statusElement.textContent =
                "● Jarvis Online";


            /*
                Continue action even if
                speech fails.
            */

            if (onComplete) {

                onComplete();

            }

        };


    window.speechSynthesis.speak(
        speech
    );

}


// ============================================================
// MICROPHONE
// ============================================================

function startListening() {


    const SpeechRecognition =

        window.SpeechRecognition ||

        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {


        alert(
            "Speech recognition is not supported in this browser. Please use Google Chrome."
        );


        return;

    }


    /*
        Stop previous speech before
        listening again.
    */

    if (
        "speechSynthesis" in window
    ) {

        window.speechSynthesis.cancel();

    }


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    // ========================================================
    // START
    // ========================================================

    recognition.onstart =
        function() {


            statusElement.textContent =
                "🎤 Listening...";


            micButton.classList.add(
                "listening"
            );

        };


    // ========================================================
    // RESULT
    // ========================================================

    recognition.onresult =
        function(event) {


            const transcript =

                event.results[0][0]
                    .transcript;


            input.value =
                transcript;


            /*
                This request came from
                microphone.
            */

            voiceMode =
                true;


            statusElement.textContent =
                "◌ Processing voice...";


            micButton.classList.remove(
                "listening"
            );


            sendMessage();

        };


    // ========================================================
    // ERROR
    // ========================================================

    recognition.onerror =
        function(event) {


            console.error(
                "Microphone Error:",
                event.error
            );


            voiceMode =
                false;


            micButton.classList.remove(
                "listening"
            );


            if (
                event.error ===
                "not-allowed"
            ) {


                statusElement.textContent =
                    "❌ Microphone permission denied";

            }

            else if (
                event.error ===
                "no-speech"
            ) {


                statusElement.textContent =
                    "🎤 No speech detected";

            }

            else if (
                event.error ===
                "audio-capture"
            ) {


                statusElement.textContent =
                    "❌ Microphone not available";

            }

            else {


                statusElement.textContent =
                    "● Jarvis Online";

            }

        };


    // ========================================================
    // END
    // ========================================================

    recognition.onend =
        function() {


            micButton.classList.remove(
                "listening"
            );


            if (
                statusElement.textContent ===
                "🎤 Listening..."
            ) {


                statusElement.textContent =
                    "● Jarvis Online";

            }

        };


    // ========================================================
    // START RECOGNITION
    // ========================================================

    try {


        recognition.start();


    }

    catch (error) {


        console.error(
            "Recognition Error:",
            error
        );


        voiceMode =
            false;


        statusElement.textContent =
            "● Jarvis Online";

    }

}


// ============================================================
// SEND BUTTON
// ============================================================

sendButton.addEventListener(
    "click",
    function() {


        /*
            Send button = typed mode.
        */

        voiceMode =
            false;


        sendMessage();

    }
);


// ============================================================
// MICROPHONE BUTTON
// ============================================================

micButton.addEventListener(
    "click",
    function() {


        startListening();

    }
);


// ============================================================
// ENTER KEY
// ============================================================

input.addEventListener(
    "keydown",
    function(event) {


        if (
            event.key === "Enter"
        ) {


            event.preventDefault();


            /*
                Enter = typed mode.
            */

            voiceMode =
                false;


            sendMessage();

        }

    }
);


// ============================================================
// PAGE LOAD
// ============================================================

window.addEventListener(
    "load",
    function() {


        input.focus();


        statusElement.textContent =
            "● Jarvis Online";

    }
);


</script>


</body>
</html>
"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML)


# ============================================================
# STATUS ROUTE
# ============================================================

@app.route("/api/status", methods=["GET"])
def status():

    return jsonify(
        {
            "success": True,
            "assistant": "Jarvis",
            "status": "online",
            "provider": "Google Gemini",
        }
    )


# ============================================================
# CHAT ROUTE
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        # ----------------------------------------------------
        # API KEY
        # ----------------------------------------------------

        api_key = os.environ.get(
            "GEMINI_API_KEY"
        )


        if not api_key:

            return jsonify(
                {
                    "success": False,
                    "error":
                        "GEMINI_API_KEY is not configured.",
                }
            ), 500


        # ----------------------------------------------------
        # REQUEST DATA
        # ----------------------------------------------------

        data = request.get_json(
            silent=True
        ) or {}


        message = str(
            data.get(
                "message",
                ""
            )
        ).strip()


        if not message:

            return jsonify(
                {
                    "success": False,
                    "error":
                        "Please enter a message.",
                }
            ), 400


        # ----------------------------------------------------
        # GEMINI CLIENT
        # ----------------------------------------------------

        client = genai.Client(
            api_key=api_key
        )


        # ----------------------------------------------------
        # JARVIS PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are Jarvis, an intelligent AI assistant.

Your name is Jarvis.

Instructions:
- Answer the user's question clearly.
- Be helpful, friendly, and professional.
- Keep simple questions concise.
- Give detailed explanations when necessary.
- If the user asks a programming question, provide useful code and explanation.
- Communicate naturally in English, Hindi, or Hinglish depending on the user's language.
- Format answers so they are easy to read.
- Do not claim that you physically control the user's computer or devices.

User:
{message}

Jarvis:
"""


        # ----------------------------------------------------
        # GEMINI REQUEST
        # ----------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        reply = response.text


        if not reply:

            reply = (
                "Sorry, I couldn't generate "
                "a response for that."
            )


        return jsonify(
            {
                "success": True,
                "reply": reply,
            }
        )


    except Exception as error:

        print(
            "Jarvis Gemini Error:",
            repr(error)
        )


        return jsonify(
            {
                "success": False,
                "error":
                    "Jarvis could not process the request.",
            }
        ), 500


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )