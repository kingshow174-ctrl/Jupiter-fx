from flask import Flask, send_from_directory, request, jsonify
import os
import requests

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DERIV_CLIENT_ID = "34dOXKmoe0wMGmp2uin91"
DERIV_TOKEN_URL = "https://auth.deriv.com/oauth2/token"
REDIRECT_URI = "https://jupiter-fx.onrender.com/callback"

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/callback")
def callback():
    return send_from_directory(BASE_DIR, "callback.html")

@app.route("/api/exchange", methods=["POST"])
def exchange_token():
    data = request.get_json()
    code = data.get("code")
    code_verifier = data.get("code_verifier")

    if not code or not code_verifier:
        return jsonify({"error": "missing code or code_verifier"}), 400

    resp = requests.post(DERIV_TOKEN_URL, data={
        "grant_type": "authorization_code",
        "client_id": DERIV_CLIENT_ID,
        "code": code,
        "code_verifier": code_verifier,
        "redirect_uri": REDIRECT_URI
    })

    if resp.status_code != 200:
        return jsonify({"error": "token exchange failed", "detail": resp.text}), 400

    return jsonify(resp.json())

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
