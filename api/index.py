"""
api/index.py
------------
Web version of Jarvis AI Assistant for Vercel.
Uses Google Gemini API.
"""

from flask import Flask, request, jsonify, render_template_string
from google import genai
import os


# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# JARVIS WEB UI
# --------------------------------------------------

HTML = """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
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

            display: flex;
            justify-content: center;
            align-items: center;

            background:
                radial-gradient(
                    circle at center,
                    #071c2c,
                    #02070d 60%
                );

            color: white;

            font-family:
                Arial,
                Helvetica,
                sans-serif;
        }


        .container {

            width: 90%;

            max-width: 750px;

            text-align: center;

            padding: 30px;
        }


        h1 {

            font-size: 50px;

            letter-spacing: 8px;

            color: #00eaff;

            text-shadow:
                0 0 10px #00eaff;

            margin-bottom: 5px;
        }


        .subtitle {

            color: #8496a5;

            margin-bottom: 20px;
        }


        /* JARVIS CIRCLE */

        .circle {

            width: 140px;
            height: 140px;

            margin: 20px auto;

            border-radius: 50%;

            border: 4px solid #00eaff;

            display: flex;
            justify-content: center;
            align-items: center;

            font-size: 50px;

            box-shadow:
                0 0 15px #00eaff,
                0 0 35px rgba(0, 234, 255, 0.5),
                inset 0 0 20px rgba(0, 234, 255, 0.5);

            animation: pulse 2s infinite;
        }


        @keyframes pulse {

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


        /* CHAT BOX */

        #chat {

            height: 320px;

            overflow-y: auto;

            text-align: left;

            padding: 20px;

            margin-top: 25px;
            margin-bottom: 15px;

            background: rgba(5, 14, 23, 0.9);

            border:
                1px solid rgba(0, 234, 255, 0.25);

            border-radius: 15px;

            box-shadow:
                0 0 20px rgba(0, 234, 255, 0.08);
        }


        .message {

            margin: 12px 0;

            padding: 10px 14px;

            border-radius: 10px;

            line-height: 1.5;
        }


        .user {

            color: white;

            background: rgba(255, 255, 255, 0.05);
        }


        .jarvis {

            color: #00eaff;

            background: rgba(0, 234, 255, 0.05);
        }


        /* INPUT */

        .input-area {

            display: flex;

            gap: 10px;

            width: 100%;
        }


        input {

            flex: 1;

            min-width: 0;

            padding: 15px 20px;

            border-radius: 30px;

            border: 1px solid #00eaff;

            background: #07111c;

            color: white;

            outline: none;

            font-size: 15px;
        }


        input:focus {

            box-shadow:
                0 0 10px rgba(0, 234, 255, 0.5);
        }


        button {

            border: none;

            padding: 12px 20px;

            border-radius: 30px;

            cursor: pointer;

            background: #00eaff;

            color: #001018;

            font-weight: bold;

            transition: 0.2s;
        }


        button:hover {

            transform: scale(1.05);

            box-shadow:
                0 0 15px rgba(0, 234, 255, 0.7);
        }


        #mic {

            width: 52px;

            font-size: 20px;

            padding: 10px;
        }


        #status {

            margin-top: 15px;

            color: #00ff88;

            font-size: 14px;
        }


        /* MOBILE */

        @media (max-width: 600px) {

            .container {

                width: 95%;

                padding: 15px;
            }


            h1 {

                font-size: 38px;

                letter-spacing: 5px;
            }


            .circle {

                width: 110px;
                height: 110px;

                font-size: 40px;
            }


            #chat {

                height: 300px;
            }


            button {

                padding: 10px 14px;
            }

        }

    </style>

</head>


<body>


<div class="container">


    <h1>JARVIS</h1>


    <p class="subtitle">

        AI Assistant • Powered by Gemini

    </p>


    <div class="circle">

        🤖

    </div>


    <!-- CHAT -->

    <div id="chat">

        <div class="message jarvis">

            <b>Jarvis:</b>

            Hello. I'm Jarvis.
            How can I help you?

        </div>

    </div>


    <!-- INPUT -->

    <div class="input-area">


        <input

            id="message"

            type="text"

            placeholder="Ask Jarvis anything..."

            autocomplete="off"

        >


        <button

            id="sendButton"

            onclick="sendMessage()"

        >

            Send

        </button>


        <button

            id="mic"

            onclick="startListening()"

            title="Speak to Jarvis"

        >

            🎤

        </button>


    </div>


    <div id="status">

        ● Jarvis Online

    </div>


</div>



<script>


const input =
    document.getElementById("message");


const chat =
    document.getElementById("chat");


const statusText =
    document.getElementById("status");


const sendButton =
    document.getElementById("sendButton");


// --------------------------------------------------
// ENTER KEY
// --------------------------------------------------

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


// --------------------------------------------------
// ESCAPE HTML
// --------------------------------------------------

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


// --------------------------------------------------
// ADD MESSAGE
// --------------------------------------------------

function addMessage(sender, text, className) {

    const message =
        document.createElement("div");

    message.className =
        "message " + className;


    const strong =
        document.createElement("b");

    strong.textContent =
        sender + ": ";


    const span =
        document.createElement("span");

    span.textContent = text;


    message.appendChild(strong);

    message.appendChild(span);

    chat.appendChild(message);


    chat.scrollTop =
        chat.scrollHeight;


    return message;
}


// --------------------------------------------------
// SEND MESSAGE
// --------------------------------------------------

async function sendMessage() {


    const message =
        input.value.trim();


    if (!message) {

        return;

    }


    addMessage(
        "You",
        message,
        "user"
    );


    input.value = "";


    const loading =
        addMessage(
            "Jarvis",
            "Thinking...",
            "jarvis"
        );


    sendButton.disabled = true;

    statusText.innerText =
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

                            message: message

                        })

                }
            );


        const data =
            await response.json();


        loading.remove();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );

        }


        addMessage(
            "Jarvis",
            data.reply,
            "jarvis"
        );


        statusText.innerText =
            "● Jarvis Online";


        speakText(
            data.reply
        );


    }

    catch (error) {


        loading.remove();


        addMessage(
            "Jarvis",
            "Error: " + error.message,
            "jarvis"
        );


        statusText.innerText =
            "● Jarvis Online";

    }

    finally {

        sendButton.disabled = false;

        input.focus();

    }

}


// --------------------------------------------------
// TEXT TO SPEECH
// --------------------------------------------------

function speakText(text) {


    if (
        !("speechSynthesis" in window)
    ) {

        return;

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.lang = "en-IN";

    speech.rate = 1;

    speech.pitch = 1;


    window.speechSynthesis.speak(
        speech
    );

}


// --------------------------------------------------
// SPEECH RECOGNITION
// --------------------------------------------------

function startListening() {


    const SpeechRecognition =

        window.SpeechRecognition ||

        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {


        alert(
            "Speech recognition is not supported by this browser. Please use Chrome or type your message."
        );


        return;

    }


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    recognition.interimResults =
        false;


    recognition.continuous =
        false;


    statusText.innerText =
        "🎤 Listening...";


    recognition.start();


    recognition.onresult =
        function(event) {


            const transcript =

                event.results[0][0]
                    .transcript;


            input.value =
                transcript;


            statusText.innerText =
                "● Jarvis Online";


            sendMessage();

        };


    recognition.onerror =
        function(event) {


            console.log(
                "Speech recognition error:",
                event.error
            );


            statusText.innerText =
                "● Jarvis Online";

        };


    recognition.onend =
        function() {


            if (
                statusText.innerText ===
                "🎤 Listening..."
            ) {

                statusText.innerText =
                    "● Jarvis Online";

            }

        };

}


</script>


</body>

</html>
"""


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():

    return render_template_string(
        HTML
    )


# --------------------------------------------------
# STATUS API
# --------------------------------------------------

@app.route("/api/status")
def status():

    return jsonify({

        "assistant": "Jarvis",

        "status": "online",

        "ai": "Gemini"

    })


# --------------------------------------------------
# GEMINI CHAT API
# --------------------------------------------------

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:


        # Check Gemini key

        if not GEMINI_API_KEY:

            return jsonify({

                "error":
                    "GEMINI_API_KEY is not configured."

            }), 500


        if client is None:

            return jsonify({

                "error":
                    "Gemini client could not be initialized."

            }), 500


        # Get request

        data =
            request.get_json(
                silent=True
            ) or {}


        message =
            data.get(
                "message",
                ""
            ).strip()


        if not message:

            return jsonify({

                "error":
                    "Please enter a message."

            }), 400


        # Send request to Gemini

        response =
            client.models.generate_content(

                model="gemini-2.5-flash",

                contents=f"""
You are Jarvis, a helpful AI assistant.

Rules:
- Answer clearly.
- Keep normal answers concise.
- Be friendly and professional.
- You are called Jarvis.
- Do not claim to control the user's computer.
- If the user asks a coding question, provide useful code when appropriate.

User message:
{message}
"""

            )


        # Get Gemini response

        reply =
            response.text


        if not reply:

            reply = (
                "I couldn't generate a response."
            )


        return jsonify({

            "success": True,

            "reply": reply

        })


    except Exception as e:


        print(
            "Jarvis Gemini API Error:",
            str(e)
        )


        return jsonify({

            "success": False,

            "error":
                "Jarvis could not process the request."

        }), 500


# --------------------------------------------------
# LOCAL TEST
# --------------------------------------------------

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )