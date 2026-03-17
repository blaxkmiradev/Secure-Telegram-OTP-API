import os
import random
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Credits: Made by Rikixz (t.me/yunaonthetp)


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 2. Silence Flask/Werkzeug Networking Logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)


otp_store = {}

def send_telegram_otp(otp):
    """Internal helper to send OTP via Telegram Bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    text = (
        "🔐 *Secure Auth System*\n"
        f"Your Code: `{otp}`\n\n"
        "Powered by: @yunaonthetp"
    )
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "MarkdownV2"
    }
    try:
        requests.post(url, json=payload, timeout=5)
        return True
    except Exception:
        return False

@app.route('/request-otp', methods=['POST'])
def request_otp():
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"msg": "Identification required"}), 400

    otp = str(random.randint(100000, 999999))
    otp_store[user_id] = otp
    
    if send_telegram_otp(otp):
        return jsonify({"msg": "OTP dispatched via Telegram"}), 200
    return jsonify({"msg": "Dispatch error"}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    uid, code = data.get("user_id"), data.get("otp")

    if uid in otp_store and otp_store[uid] == str(code):
        del otp_store[uid]
        return jsonify({"msg": "Access Authorized", "dev": "Rikixz"}), 200
    
    return jsonify({"msg": "Access Denied"}), 401

if __name__ == '__main__':
    print("\n" + "="*40)
    print(" SECURE OTP API BY RIKIXZ")
    print("  Host: http://localhost:5000")
    print("  Mode:simple")
    print("="*40 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
