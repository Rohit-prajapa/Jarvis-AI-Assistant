from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Jarvis AI Assistant</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #02070d;
            color: white;
            font-family: Arial, sans-serif;

            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 90%;
            max-width: 700px;
            text-align: center;
        }

        h1 {
            color: #00eaff;
            font-size: 45px;
            margin-bottom: 5px;
        }

        .subtitle {
            color: #8d9ca8;
            margin-bottom: 25px;
        }

        .circle {
            width: 140px;
            height: 140px;

            margin: 20px auto;

            border-radius: 50%;

            border: 4px solid #00eaff;

            display: flex;
            align-items: center;
            justify-content: center;

            box-shadow:
                0 0 20px #00eaff,
                inset 0 0 20px #00eaff;

            font-size: 45px;
        }

        #chat {
            height: 300px;

            overflow-y: auto;

            text-align: left;

            border: 1px solid #123;

            border-radius: 12px;

            padding: 15px;

            margin-top: 25px;
            margin-bottom: 15px;

            background: #050c14;
        }

        .user {
            color: #ffffff;
            margin: 12px 0;
        }

        .jarvis {
            color: #00eaff;
            margin: 12px 0;
        }

        .input-area {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;

            padding: 15px;

            border-radius: 30px;

            border: 1px solid #00eaff;

            background: #07111c;
            color: white;

            outline: none;
        }

        button {
            border: none;

            padding: 12px 20px;

            border-radius: 30px;

            cursor: pointer;

            background: #00eaff;
            color: #001018;

            font-weight: bold;
        }

        #mic {
            font-size: 20px;
        }

        #status {
            margin-top: 15px;
            color: #00ff88;
        }

    </style>

</head>

<body>

<div class="container">

    <h1>JARVIS</h1>

    <p class="subtitle">
        AI Assistant
    </p>


    <div class="circle">
        🤖
    </div>


    <div id="chat">

        <div class="jarvis">
            <b>Jarvis:</b>
            Hello. I'm Jarvis. How can I help you?
        </div>

    </div>


    <div class="input-area">

        <input
            id="message"
            type="text"
            placeholder="Ask Jarvis anything..."
        >

        <button onclick="sendMessage()">
            Send
        </button>

        <button id="mic" onclick="startListening()">
            🎤
        </button>

    </div>


    <div id="status">
        ● Jarvis Online
    </div>

</div>


<script>

const input = document.getElementById("message");
const chat = document.getElementById("chat");


input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});


async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }


    chat.innerHTML += `
        <div class="user">
            <b>You:</b> ${escapeHTML(message)}
        </div>
    `;


    input.value = "";


    chat.innerHTML += `
        <div class="jarvis" id="loading">
            <b>Jarvis:</b> Thinking...
        </div>
    `;


    chat.scrollTop = chat.scrollHeight;


    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        const loading =
            document.getElementById("loading");

        if (loading) {
            loading.remove();
        }


        if (!response.ok) {

            throw new Error(
                data.error || "Something went wrong."
            );

        }


        chat.innerHTML += `
            <div class="jarvis">
                <b>Jarvis:</b>
                ${escapeHTML(data.reply)}
            </div>
        `;


        speakText(data.reply);


    } catch (error) {

        const loading =
            document.getElementById("loading");

        if (loading) {
            loading.remove();
        }


        chat.innerHTML += `
            <div class="jarvis">
                <b>Jarvis:</b>
                Error: ${escapeHTML(error.message)}
            </div>
        `;

    }


    chat.scrollTop = chat.scrollHeight;

}


function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


// --------------------------------
// TEXT TO SPEECH
// --------------------------------

function speakText(text) {

    if (!("speechSynthesis" in window)) {
        return;
    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);

}


// --------------------------------
// MICROPHONE
// --------------------------------

function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Speech recognition is not supported by this browser."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang = "en-IN";

    recognition.interimResults = false;


    document.getElementById("status").innerText =
        "🎤 Listening...";


    recognition.start();


    recognition.onresult = function(event) {

        const transcript =
            event.results[0][0].transcript;


        input.value = transcript;


        document.getElementById("status").innerText =
            "● Jarvis Online";


        sendMessage();

    };


    recognition.onerror = function() {

        document.getElementById("status").innerText =
            "● Jarvis Online";

    };


    recognition.onend = function() {

        document.getElementById("status").innerText =
            "● Jarvis Online";

    };

}

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/status")
def status():

    return jsonify({
        "assistant": "Jarvis",
        "status": "online"
    })


@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True) or {}

        message = data.get("message", "").strip()


        if not message:

            return jsonify({
                "error": "Please enter a message."
            }), 400


        if not os.environ.get("OPENAI_API_KEY"):

            return jsonify({
                "error": "OPENAI_API_KEY is not configured."
            }), 500


        response = client.responses.create(

            model="gpt-4.1-mini",

            instructions="""
            You are Jarvis, a helpful AI assistant.
            Keep answers clear, friendly and concise.
            """,

            input=message
        )


        return jsonify({
            "reply": response.output_text
        })


    except Exception as e:

        print("Jarvis API Error:", str(e))

        return jsonify({
            "error": "Jarvis could not process the request."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)