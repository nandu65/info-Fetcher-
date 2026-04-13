from flask import Flask, request
import requests
import os
import re

app = Flask(__name__)

BOT_TOKEN = os.getenv("API_KEY")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def detect_type(text):
    text = text.strip()

    if re.match(r"[^@]+@[^@]+\.[^@]+", text):
        return "Email"
    elif re.match(r"^\+?\d{10,13}$", text):
        return "Phone"
    elif re.match(r"^\d{1,3}(\.\d{1,3}){3}$", text):
        return "IP"
    elif len(text.split()) >= 2:
        return "Full Name"
    else:
        return "Username"

def fake_result(text, t):
    if t == "Email":
        return "Checked email in system → No match found"
    elif t == "Phone":
        return "Phone lookup → Linked account: Demo_User_01"
    elif t == "IP":
        return "IP trace → Location: Unknown (demo)"
    else:
        return "User record → Basic profile found"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        t = detect_type(message)
        result = fake_result(message, t)

        reply = f"""
🔍 Input: {message}
📌 Type: {t}

📊 Result:
{result}
"""

        requests.get(f"{BASE_URL}/sendMessage", params={
            "chat_id": chat_id,
            "text": reply
        })

    except Exception as e:
        print(e)

    return "ok"
