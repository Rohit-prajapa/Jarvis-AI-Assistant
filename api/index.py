import os
import requests

from flask import Flask, jsonify, render_template_string, request


app = Flask(__name__)


# ============================================================
# FRONTEND
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Jarvis AI Assistant</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            background: radial-gradient(
                circle at top,
                #071c2c 0%,
                #02070d 45%,
                #000000 100%
            );
            color: white;
            font-family: Arial, Helvetica, sans-serif;
        }

        .container {
            width: 92%;
            max-width: 950px;
            min-height: 100vh;
            margin: auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 25px 0;
        }

        .header {
            text-align: center;
            margin-bottom: 15px;
        }

        h1 {
            color: #00eaff;
            font-size: 48px;
            letter-spacing: 8px;
            text-shadow: 0 0 12px #00eaff;
        }

        .subtitle {
            color: #8b9aaa;
            margin-top: 8px;
        }

        .jarvis-circle {
            width: 135px;
            height: 135px;
            margin: 20px auto;
            border-radius: 50%;
            border: 4px solid #00eaff;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 50px;

            background: radial-gradient(
                circle,
                rgba(0, 234, 255, 0.18),
                rgba(0, 0, 0, 0.6)
            );

            box-shadow:
                0 0 15px #00eaff,
                0 0 35px rgba(0, 234, 255, 0.45);

            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.05);
            }
        }

        #chat {
            height: 350px;
            overflow-y: auto;
            padding: 20px;
            background: rgba(4, 13, 22, 0.94);
            border: 1px solid rgba(0, 234, 255, 0.25);
            border-radius: 16px;
            scroll-behavior: smooth;
        }

        .message {
            padding: 14px 18px;
            margin-bottom: 15px;
            border-radius: 12px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .jarvis-message {
            color: #00eaff;
            background: rgba(0, 234, 255, 0.06);
            border-left: 4px solid #00eaff;
        }

        .user-message {
            color: white;
            background: rgba(255, 255, 255, 0.06);
            border-left: 4px solid white;
        }

        .sender {
            font-weight: bold;
        }

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
            border: 1px solid #00eaff;
            border-radius: 30px;
            background: #07111c;
            color: white;
            outline: none;
            font-size: 16px;
        }

        #message:focus {
            box-shadow: 0 0 15px rgba(0, 234, 255, 0.35);
        }

        #message::placeholder {
            color: #71808d;
        }

        button {
            border: none;
            border-radius: 30px;
            padding: 15px 22px;
            background: #00eaff;
            color: #001018;
            font-weight: bold;
            font-size: 15px;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 18px rgba(0, 234, 255, 0.6);
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
            animation: micPulse 0.8s infinite;
        }

        @keyframes micPulse {
            50% {
                transform: scale(1.15);
            }
        }

        #status {
            text-align: center;
            margin-top: 13px;
            color: #00ff88;
        }

        .footer {
            text-align: center;
            margin-top: 12px;
            color: #53616d;
            font-size: 12px;
        }

        @media (max-width: 650px) {
            .container {
                width: 95%;
            }

            h1 {
                font-size: 36px;
            }

            .jarvis-circle {
                width: 105px;
                height: 105px;
                font-size: 40px;
            }

            #chat {
                height: 390px;
                padding: 14px;
            }

            #message {
                padding: 14px;
            }

            button {
                padding: 14px;
            }
        }
    </style>
</head>


<body>

<div class="container">

    <div class="header">
        <h1>JARVIS</h1>

        <div class="subtitle">
            AI Assistant • Powered by OpenRouter
        </div>
    </div>


    <div class="jarvis-circle">
        🤖
    </div>


    <div id="chat">

        <div class="message jarvis-message">
            <span class="sender">Jarvis: </span>
            Hello! I am Jarvis, your AI assistant. How can I help you today?
        </div>

    </div>


    <div class="input-area">

        <input
            id="message"
            type="text"
            placeholder="Ask Jarvis anything..."
            autocomplete="off"
        >

        <button id="sendButton" type="button">
            Send
        </button>

        <button
            id="micButton"
            type="button"
            title="Speak to Jarvis"
        >
            🎤
        </button>

    </div>


    <div id="status">
        ● Jarvis Online
    </div>


    <div class="footer">
        Jarvis AI Assistant
    </div>

</div>


<script>

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


let voiceMode = false;


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(sender, text, type) {

    const box =
        document.createElement("div");


    if (type === "user") {

        box.className =
            "message user-message";

    } else {

        box.className =
            "message jarvis-message";
    }


    const senderSpan =
        document.createElement("span");

    senderSpan.className =
        "sender";

    senderSpan.textContent =
        sender + ": ";


    const textSpan =
        document.createElement("span");

    textSpan.textContent =
        text;


    box.appendChild(
        senderSpan
    );

    box.appendChild(
        textSpan
    );


    chat.appendChild(
        box
    );


    chat.scrollTop =
        chat.scrollHeight;


    return box;
}


// ============================================================
// NORMALIZE COMMAND
// ============================================================

function normalizeCommand(text) {

    return text
        .toLowerCase()
        .replace(/[.,!?]/g, "")
        .replace(/\bjarvis\b/g, "")
        .replace(/\bplease\b/g, "")
        .replace(/\byou tube\b/g, "youtube")
        .replace(/\bu tube\b/g, "youtube")
        .replace(/\blinked in\b/g, "linkedin")
        .replace(/\bface book\b/g, "facebook")
        .replace(/\binsta gram\b/g, "instagram")
        .replace(/\s+/g, " ")
        .trim();
}


// ============================================================
// WEBSITES
// ============================================================

const websites = {

    youtube: {
        label: "YouTube",
        url: "https://www.youtube.com"
    },

    google: {
        label: "Google",
        url: "https://www.google.com"
    },

    gmail: {
        label: "Gmail",
        url: "https://mail.google.com"
    },

    github: {
        label: "GitHub",
        url: "https://github.com"
    },

    linkedin: {
        label: "LinkedIn",
        url: "https://www.linkedin.com"
    },

    instagram: {
        label: "Instagram",
        url: "https://www.instagram.com"
    },

    facebook: {
        label: "Facebook",
        url: "https://www.facebook.com"
    },

    spotify: {
        label: "Spotify",
        url: "https://open.spotify.com"
    },

    wikipedia: {
        label: "Wikipedia",
        url: "https://www.wikipedia.org"
    },

    whatsapp: {
        label: "WhatsApp",
        url: "https://web.whatsapp.com"
    }
};


// ============================================================
// DETECT COMMAND
// ============================================================

function detectCommand(userMessage) {

    const command =
        normalizeCommand(userMessage);


    // ========================================================
    // OPEN WEBSITE
    // ========================================================

    for (
        const [name, website]
        of Object.entries(websites)
    ) {

        if (
            command === "open " + name ||
            command === "launch " + name ||
            command === "start " + name ||
            command.includes("open " + name)
        ) {

            return {
                handled: true,
                type: "navigate",
                url: website.url,
                response:
                    "Opening " +
                    website.label
            };
        }
    }


    // ========================================================
    // PLAY SONG / VIDEO
    // ========================================================

    if (
        command.startsWith("play ")
    ) {

        const query =
            command
                .substring(5)
                .trim();


        if (!query) {

            return {
                handled: true,
                type: "message",
                response:
                    "Tell me what you want me to play."
            };
        }


        return {
            handled: true,

            type: "navigate",

            url:
                "https://www.youtube.com/results?search_query=" +
                encodeURIComponent(query),

            response:
                "Searching YouTube for " +
                query
        };
    }


    // ========================================================
    // SEARCH YOUTUBE FOR
    // ========================================================

    if (
        command.startsWith(
            "search youtube for "
        )
    ) {

        const query =
            command
                .replace(
                    "search youtube for ",
                    ""
                )
                .trim();


        if (query) {

            return {
                handled: true,

                type: "navigate",

                url:
                    "https://www.youtube.com/results?search_query=" +
                    encodeURIComponent(query),

                response:
                    "Searching YouTube for " +
                    query
            };
        }
    }


    // ========================================================
    // SEARCH ON YOUTUBE
    // ========================================================

    if (
        command.startsWith(
            "search on youtube "
        )
    ) {

        const query =
            command
                .replace(
                    "search on youtube ",
                    ""
                )
                .trim();


        if (query) {

            return {
                handled: true,

                type: "navigate",

                url:
                    "https://www.youtube.com/results?search_query=" +
                    encodeURIComponent(query),

                response:
                    "Searching YouTube for " +
                    query
            };
        }
    }


    // ========================================================
    // SEARCH GOOGLE FOR
    // ========================================================

    if (
        command.startsWith(
            "search google for "
        )
    ) {

        const query =
            command
                .replace(
                    "search google for ",
                    ""
                )
                .trim();


        if (query) {

            return {
                handled: true,

                type: "navigate",

                url:
                    "https://www.google.com/search?q=" +
                    encodeURIComponent(query),

                response:
                    "Searching Google for " +
                    query
            };
        }
    }


    // ========================================================
    // SEARCH ON GOOGLE
    // ========================================================

    if (
        command.startsWith(
            "search on google "
        )
    ) {

        const query =
            command
                .replace(
                    "search on google ",
                    ""
                )
                .trim();


        if (query) {

            return {
                handled: true,

                type: "navigate",

                url:
                    "https://www.google.com/search?q=" +
                    encodeURIComponent(query),

                response:
                    "Searching Google for " +
                    query
            };
        }
    }


    // ========================================================
    // GOOGLE SOMETHING
    // ========================================================

    if (
        command.startsWith("google ")
    ) {

        const query =
            command
                .substring(7)
                .trim();


        if (query) {

            return {
                handled: true,

                type: "navigate",

                url:
                    "https://www.google.com/search?q=" +
                    encodeURIComponent(query),

                response:
                    "Searching Google for " +
                    query
            };
        }
    }


    return {
        handled: false
    };
}


// ============================================================
// SPEAK
// ============================================================

function speakText(
    text,
    onComplete = null
) {

    if (
        !("speechSynthesis" in window)
    ) {

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
        window.speechSynthesis
            .getVoices();


    const preferredVoice =
        voices.find(
            function(voice) {
                return (
                    voice.lang ===
                    "en-IN"
                );
            }
        ) ||
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
        function() {

            statusElement.textContent =
                "● Jarvis Online";


            if (onComplete) {
                onComplete();
            }
        };


    window.speechSynthesis.speak(
        speech
    );
}


// ============================================================
// EXECUTE COMMAND
// ============================================================

function executeCommand(
    command,
    shouldSpeak
) {

    addMessage(
        "Jarvis",
        command.response,
        "jarvis"
    );


    if (
        command.type === "message"
    ) {

        if (shouldSpeak) {

            speakText(
                command.response
            );
        }

        return;
    }


    if (
        command.type === "navigate"
    ) {

        if (shouldSpeak) {

            speakText(
                command.response,

                function() {

                    window.location.href =
                        command.url;
                }
            );

        } else {

            window.location.href =
                command.url;
        }
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


    const shouldSpeak =
        voiceMode;


    voiceMode =
        false;


    addMessage(
        "You",
        userMessage,
        "user"
    );


    input.value =
        "";


    // ========================================================
    // LOCAL COMMANDS
    // ========================================================

    const command =
        detectCommand(
            userMessage
        );


    if (
        command.handled
    ) {

        executeCommand(
            command,
            shouldSpeak
        );

        return;
    }


    // ========================================================
    // AI CHAT
    // ========================================================

    const thinking =
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
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message:
                                userMessage
                        })
                }
            );


        let data;


        try {

            data =
                await response.json();

        } catch (error) {

            throw new Error(
                "Invalid response from Jarvis server."
            );
        }


        if (
            thinking &&
            thinking.isConnected
        ) {

            thinking.remove();
        }


        if (
            !response.ok
        ) {

            throw new Error(
                data.error ||
                "Jarvis could not process the request."
            );
        }


        const reply =
            data.reply ||
            "Sorry, I could not generate an answer.";


        addMessage(
            "Jarvis",
            reply,
            "jarvis"
        );


        statusElement.textContent =
            "● Jarvis Online";


        // Speak only when microphone was used.

        if (shouldSpeak) {

            speakText(
                reply
            );
        }


    } catch (error) {

        if (
            thinking &&
            thinking.isConnected
        ) {

            thinking.remove();
        }


        console.error(
            "Jarvis Error:",
            error
        );


        addMessage(
            "Jarvis",
            "Error: " +
            error.message,
            "jarvis"
        );


        statusElement.textContent =
            "● Jarvis Online";


    } finally {

        sendButton.disabled =
            false;

        micButton.disabled =
            false;

        input.focus();
    }
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


    recognition.onstart =
        function() {

            micButton.classList.add(
                "listening"
            );

            statusElement.textContent =
                "🎤 Listening...";
        };


    recognition.onresult =
        function(event) {

            const transcript =
                event
                    .results[0][0]
                    .transcript;


            input.value =
                transcript;


            voiceMode =
                true;


            micButton.classList.remove(
                "listening"
            );


            statusElement.textContent =
                "◌ Processing voice...";


            sendMessage();
        };


    recognition.onerror =
        function(event) {

            console.error(
                "Speech recognition error:",
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

            } else if (
                event.error ===
                "no-speech"
            ) {

                statusElement.textContent =
                    "🎤 No speech detected";

            } else if (
                event.error ===
                "audio-capture"
            ) {

                statusElement.textContent =
                    "❌ Microphone not available";

            } else {

                statusElement.textContent =
                    "● Jarvis Online";
            }
        };


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


    try {

        recognition.start();

    } catch (error) {

        console.error(
            "Recognition error:",
            error
        );


        voiceMode =
            false;


        statusElement.textContent =
            "● Jarvis Online";
    }
}


// ============================================================
// EVENTS
// ============================================================

sendButton.addEventListener(
    "click",
    function() {

        voiceMode =
            false;

        sendMessage();
    }
);


micButton.addEventListener(
    "click",
    function() {

        startListening();
    }
);


input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            voiceMode =
                false;

            sendMessage();
        }
    }
);


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
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML)


# ============================================================
# STATUS
# ============================================================

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify(
        {
            "success": True,
            "assistant": "Jarvis",
            "status": "online",
            "provider": "OpenRouter",
        }
    )


# ============================================================
# OPENROUTER CHAT
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        api_key = os.environ.get("OPENROUTER_API_KEY")

        if not api_key:
            return jsonify(
                {
                    "success": False,
                    "error": "OPENROUTER_API_KEY is missing from Vercel.",
                }
            ), 500

        data = request.get_json(silent=True) or {}

        message = str(
            data.get("message", "")
        ).strip()

        if not message:
            return jsonify(
                {
                    "success": False,
                    "error": "Please enter a message.",
                }
            ), 400

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a smart and helpful AI assistant. "
                        "Your name is Jarvis. "
                        "Answer the user's actual question directly. "
                        "Give accurate and useful answers. "
                        "Keep simple answers concise. "
                        "Give detailed explanations when necessary. "
                        "For programming questions, provide correct code and explanations. "
                        "You can communicate naturally in English, Hindi, and Hinglish. "
                        "Match the user's language when appropriate. "
                        "Avoid unnecessary introductions. "
                        "Do not claim to physically control the user's computer."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=45,
        )

        try:
            result = response.json()

        except ValueError:
            print(
                "OpenRouter non-JSON response:",
                response.text,
            )

            return jsonify(
                {
                    "success": False,
                    "error": "OpenRouter returned an invalid response.",
                }
            ), 502

        if response.status_code != 200:
            print(
                "OpenRouter API Error:",
                result,
            )

            error_data = result.get(
                "error",
                {},
            )

            if isinstance(error_data, dict):
                error_message = error_data.get(
                    "message",
                    "OpenRouter request failed.",
                )
            else:
                error_message = str(
                    error_data
                )

            if response.status_code == 429:
                error_message = (
                    "Free AI limit reached. "
                    "Please wait and try again."
                )

            return jsonify(
                {
                    "success": False,
                    "error": error_message,
                }
            ), response.status_code

        choices = result.get(
            "choices",
            [],
        )

        if not choices:
            print(
                "OpenRouter empty choices:",
                result,
            )

            return jsonify(
                {
                    "success": False,
                    "error": "AI returned an empty response.",
                }
            ), 502

        first_choice = choices[0]

        message_data = first_choice.get(
            "message",
            {},
        )

        reply = message_data.get(
            "content",
            "",
        )

        if not reply:
            return jsonify(
                {
                    "success": False,
                    "error": "AI returned an empty answer.",
                }
            ), 502

        return jsonify(
            {
                "success": True,
                "reply": reply.strip(),
                "provider": "OpenRouter",
            }
        )

    except requests.exceptions.Timeout:
        return jsonify(
            {
                "success": False,
                "error": "AI request timed out. Please try again.",
            }
        ), 504

    except requests.exceptions.RequestException as error:
        print(
            "OpenRouter Network Error:",
            repr(error),
        )

        return jsonify(
            {
                "success": False,
                "error": "Could not connect to the AI service.",
            }
        ), 502

    except Exception as error:
        print(
            "Jarvis OpenRouter Error:",
            repr(error),
        )

        return jsonify(
            {
                "success": False,
                "error": "Jarvis could not process the request.",
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