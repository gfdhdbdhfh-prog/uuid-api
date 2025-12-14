from flask import Flask, jsonify, render_template_string
import uuid
import string
import secrets
import os
from os import environ

app = Flask(__name__)

def generate_short_id(length=6):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Красивая неоновая страница с анимацией
NEON_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>UUID API</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            background-color: #0f0f1a;
            color: #fff;
            font-family: 'Courier New', monospace;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .container {
            z-index: 10;
        }

        .neon-text {
            font-size: 4rem;
            font-weight: bold;
            color: #0ff;
            text-shadow:
                0 0 5px #0ff,
                0 0 10px #0ff,
                0 0 20px #0ff,
                0 0 40px #0ff;
            animation: pulse 2s infinite, float 3s ease-in-out infinite;
            letter-spacing: 5px;
        }

        .sub-text {
            font-size: 1.5rem;
            color: #f0f;
            text-shadow:
                0 0 5px #f0f,
                0 0 10px #f0f;
            margin-top: 20px;
            animation: glow 1.5s ease-in-out infinite alternate;
        }

        .api-link {
            margin-top: 40px;
            font-size: 1.2rem;
        }

        .api-link a {
            color: #0ff;
            text-decoration: none;
            font-weight: bold;
            border-bottom: 2px solid #f0f;
            padding: 5px 10px;
            transition: all 0.3s;
            animation: blink 1.5s step-start infinite;
        }

        .api-link a:hover {
            color: #ff0;
            text-shadow: 0 0 10px #ff0;
            transform: scale(1.1);
            border-color: #0ff;
        }

        @keyframes pulse {
                    0%, 100% {
                text-shadow:
                    0 0 5px #0ff,
                    0 0 10px #0ff,
                    0 0 20px #0ff,
                    0 0 40px #0ff,
                    0 0 80px #0ff;
            }
            50% {
                text-shadow:
                    0 0 5px #0ff,
                    0 0 10px #0ff,
                    0 0 20px #0ff;
            }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        @keyframes glow {
            0% {
                text-shadow: 0 0 5px #f0f, 0 0 10px #f0f;
            }
            100% {
                text-shadow: 0 0 10px #f0f, 0 0 20px #f0f, 0 0 40px #f0f;
            }
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        /* Глитч-эффект при наведении */
        .glitch {
            position: relative;
            animation: glitch 2s infinite;
        }

        .glitch::before, .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0f0f1a;
            opacity: 0.8;
        }

        .glitch::before {
            left: 2px;
            text-shadow: -2px 0 #f0f;
            animation: glitch-anim 2s infinite linear;
            clip: rect(44px, 450px, 56px, 0);
            overflow: hidden;
        }

        .glitch::after {
            left: -2px;
            text-shadow: 2px 0 #0ff;
            animation: glitch-anim2 3s infinite linear;
            clip: rect(20px, 450px, 32px, 0);
            overflow: hidden;
        }

        @keyframes glitch-anim {
            0%, 100% { clip: rect(44px, 450px, 56px, 0); }
            20% { clip: rect(10px, 450px, 60px, 0); }
            40% { clip: rect(50px, 450px, 20px, 0); }
            60% { clip: rect(30px, 450px, 40px, 0); }
            80% { clip: rect(55px, 450px, 10px, 0); }
        }

        @keyframes glitch-anim2 {
            0%, 100% { clip: rect(20px, 450px, 32px, 0); }
            25% { clip: rect(55px, 450px, 15px, 0); }
            50% { clip: rect(10px, 450px, 50px, 0); }
            75% { clip: rect(40px, 450px, 25px, 0); }
        }

        /* Звёзды в фоне */
        .star {
            position: absolute;
            background-color: #fff;
            border-radius: 50%;
            animation: twinkle 2s infinite ease-in-out;
            opacity: 0.8;
        }

        @keyframes twinkle {
            0%, 100% { opacity: 0.2; }
            50% { opacity: 1; }
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="glitch" data-text="UUID API">UUID API</div>
        <p class="sub-text">Красиво. Неоново. Генерирует ID.</p>
        <div class="api-link">
            <a href="/api/uuid">Получить UUID →</a>
        </div>
    </div>

    <!-- Создаём звёзды на фоне -->
    <script>
        for (let i = 0; i < 100; i++) {
            const star = document.createElement("div");
            star.classList.add("star");
            star.style.width = Math.random() * 3 + "px";
            star.style.height = star.style.width;
            star.style.left = Math.random() * 100 + "vw";
            star.style.top = Math.random() * 100 + "vh";
            star.style.animationDelay = Math.random() * 2 + "s";
            document.body.appendChild(star);
        }
    </script>

</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(NEON_TEMPLATE)

@app.route("/api/uuid")
def api_uuid():
    return jsonify({
        "full_uuid": str(uuid.uuid4()),
        "short_id": generate_short_id(6),
        "message": "ID generated!"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))

            
