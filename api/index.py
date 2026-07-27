"""
api/index.py
------------
Vercel API entry point for Jarvis AI Assistant.

This file is separate from main.py so the desktop
Jarvis application can continue working normally.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


# -----------------------------------------
# HOME ROUTE
# -----------------------------------------

@app.route("/")
def home():
    return """
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

                background: #050505;

                color: white;

                font-family:
                    Arial,
                    Helvetica,
                    sans-serif;
            }

            .container {
                text-align: center;
            }

            h1 {
                font-size: 50px;

                color: #00e5ff;

                margin-bottom: 20px;
            }

            .subtitle {
                font-size: 20px;

                color: #aaaaaa;

                margin-bottom: 30px;
            }

            .status {
                display: inline-block;

                padding: 12px 25px;

                border: 1px solid #00ff88;

                border-radius: 30px;

                color: #00ff88;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>
                JARVIS
            </h1>

            <p class="subtitle">
                AI Assistant
            </p>

            <div class="status">
                ● Jarvis Server Online
            </div>

        </div>

    </body>

    </html>
    """


# -----------------------------------------
# STATUS API
# -----------------------------------------

@app.route("/api/status")
def status():

    return jsonify({

        "assistant": "Jarvis",

        "status": "online",

        "message":
            "Jarvis AI Assistant API is running."

    })


# -----------------------------------------
# SIMPLE JARVIS API
# -----------------------------------------

@app.route("/api/jarvis", methods=["POST"])
def jarvis():

    try:

        data = request.get_json(silent=True) or {}

        message = data.get(
            "message",
            ""
        ).strip()

        if not message:

            return jsonify({

                "success": False,

                "error":
                    "Please provide a message."

            }), 400


        # Temporary response logic
        # Later we can connect your
        # ConversationMode / AI model here.

        response = (
            f"Jarvis received your message: {message}"
        )


        return jsonify({

            "success": True,

            "message": message,

            "response": response

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# -----------------------------------------
# LOCAL TESTING
# -----------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )