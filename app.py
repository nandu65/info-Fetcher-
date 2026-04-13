from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("API_KEY")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        # 🔹 Your logic (for now simple)
        reply = f"You searched: {message}"

        requests.get(f"{BASE_URL}/sendMessage", params={
            "chat_id": chat_id,
            "text": reply
        })

    except Exception as e:
        print(e)

    return "ok"
