from flask import Flask, jsonify
import uuid
import string
import secrets
import os
from os import environ


app = Flask(__name__)

def generate_short_id(length=6):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route("/")
def home():
    return "<h1>UUID API</h1><p>Use /api/uuid to generate ID</p>"

@app.route("/api/uuid")
def api_uuid():
    return jsonify({
        "full_uuid": str(uuid.uuid4()),
        "short_id": generate_short_id(6),
        "message": "ID сгенерирован!"
    })

# Render требует, чтобы сервер слушал правильный порт
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
