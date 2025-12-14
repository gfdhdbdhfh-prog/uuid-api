from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import uuid as uuid_module
import string
import secrets
import os

app = Flask(__name__)

# 🗃️ Временное хранилище пользователей (в реальности — база данных)
users_db = {}

def generate_short_id(length=6):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ✨ Главная страница — неоновая
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>🚀 UUID API</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            background: #0a0a1a;
            color: #0ff;
            font-family: 'Courier New', monospace;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .glitch {
            font-size: 3.5rem;
            font-weight: bold;
            color: #0ff;
            text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff;
            animation: glitch 2s infinite, float 3s ease-in-out infinite;
            position: relative;
        }
        .glitch::before, .glitch::after {
            content: "UUID API";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0a0a1a;
        }
        .glitch::before {
            left: 2px;
            text-shadow: -2px 0 #f0f;
            animation: glitch-anim 2s infinite linear;
            clip: rect(40px, 450px, 60px, 0);
            overflow: hidden;
        }
        .glitch::after {
            left: -2px;
            text-shadow: 2px 0 #0ff;
            animation: glitch-anim2 3s infinite linear;
            clip: rect(10px, 450px, 30px, 0);
            overflow: hidden;
        }
        .sub {
            color: #f0f;
            text-shadow: 0 0 5px #f0f;
            margin: 20px 0;
            font-size: 1.3rem;
        }
        .btn {
            background: transparent;
            border: 2px solid #0ff;
            color: #0ff;
            padding: 12px 24px;
            font-size: 1.2rem;
            cursor: pointer;
            border-radius: 5px;
            box-shadow: 0 0 10px #0ff;
            transition: 0.3s;
            margin: 10px;
        }
        .btn:hover {
            background: #0ff;
            color: #000;
            box-shadow: 0 0 20px #0ff, 0 0 40px #0ff;
            transform: scale(1.1);
        }
        @keyframes glitch { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
        @keyframes glitch-anim {
            0%, 100% { clip: rect(40px, 450px, 60px, 0); }
            20% { clip: rect(10px, 450px, 50px, 0); }
            40% { clip: rect(50px, 450px, 20px, 0); }
            60% { clip: rect(30px, 450px, 40px, 0); }
            80% { clip: rect(55px, 450px, 15px, 0); }
        }
        @keyframes glitch-anim2 {
            0%, 100% { clip: rect(10px, 450px, 30px, 0); }
            25% { clip: rect(55px, 450px, 12px, 0); }
            50% { clip: rect(5px, 450px, 55px, 0); }
            75% { clip: rect(40px, 450px, 25px, 0); }
        }
        .star {
            position: absolute;
            background: #fff;
            border-radius: 50%;
            opacity: 0.6;
            animation: twinkle 2s infinite;
        }
        @keyframes twinkle { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="glitch">UUID API</div>
    <p class="sub">Генерируй. Входи. Управляй.</p>
    <a href="/api/uuid"><button class="btn">Получить доступ →</button></a>
    <script>
        for (let i = 0; i < 50; i++) {
            const s = document.createElement('div');
            s.classList.add('star');
            s.style.width = s.style.height = Math.random()*3 + 'px';
            s.style.left = Math.random()*100 + 'vw';
            s.style.top = Math.random()*100 + 'vh';
            s.style.animationDelay = Math.random()*2 + 's';
            document.body.appendChild(s);
        }
    </script>
</body>
</html>
'''

LK_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8" />
    <title>🔐 Личный кабинет</title>
    <style>
        body {
            background: #0f0f20;
            color: #0ff;
            font-family: 'Courier New', monospace;
            text-align: center;
            padding: 50px;
            margin: 0;
            overflow: hidden;
        }
        .card {
            background: rgba(10, 10, 30, 0.6);
            border: 2px solid #0ff;
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            margin: 20px auto;
            box-shadow: 0 0 20px #0ff, 0 0 40px rgba(0, 255, 255, 0.3);
            animation: float 4s ease-in-out infinite;
        }
        h1 {
            color: #f0f;
            text-shadow: 0 0 10px #f0f;
        }
        input, select, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            font-family: inherit;
        }
        input {
            background: #0a0a1a;
            color: #0ff;
            border: 1px solid #0ff;
            box-shadow: 0 0 5px #0ff;
        }
        button {
            background: #f0f;
            color: white;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 0 10px #f0f;
            transition: 0.3s;
        }
        button:hover {
            background: #0ff;
            box-shadow: 0 0 20px #0ff;
            transform: scale(1.05);
        }
        .id {
            font-family: monospace;
            font-size: 0.9rem;
            color: #aaa;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔐 Личный кабинет</h1>
        <p><strong>ID:</strong> <span class="id">{{ user_id }}</span></p>

        <form method="POST">
            <input type="text" name="name" placeholder="Ваше имя" value="{{ name }}" required />
            <select name="neon_color">
                <option value="#0ff" {{ 'selected' if neon_color == '#0ff' else '' }}>Неон Синий</option>
                <option value="#f0f" {{ 'selected' if neon_color == '#f0f' else '' }}>Неон Розовый</option>
                <option value="#ff0" {{ 'selected' if neon_color == '#ff0' else '' }}>Неон Жёлтый</option>
                <option value="#0f0" {{ 'selected' if neon_color == '#0f0' else '' }}>Неон Зелёный</option>
            </select>
            <input type="text" name="status" placeholder="Статус" value="{{ status }}" />
            <button type="submit">💾 Сохранить</button>
        </form>

        <p><a href="/" style="color:#0ff; text-decoration:underline;">← Назад</a></p>
    </div>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route("/api/uuid")
def api_uuid():
    user_id = str(uuid_module.uuid4())
    # Создаём профиль по умолчанию
    users_db[user_id] = {
        "name": "Аноним",
        "status": "Активен",
        "neon_color": "#0ff"
    }
    return jsonify({
        "user_id": user_id,
        "full_uuid": user_id,
        "short_id": generate_short_id(6),
        "message": "Доступ создан! Перейдите в /lk?user_id=ваш_id",
        "login_url": f"/lk?user_id={user_id}"
    })

@app.route("/lk")
def lk_get():
    user_id = request.args.get("user_id")
    if not user_id or user_id not in users_db:
        return jsonify({"error": "Пользователь не найден или ID неверен."}), 404

    user = users_db[user_id]
    return render_template_string(
        LK_TEMPLATE,
        user_id=user_id,
        name=user["name"],
        status=user["status"],
        neon_color=user["neon_color"]
    )

@app.route("/lk", methods=["POST"])
def lk_post():
    user_id = request.args.get("user_id")
    if not user_id or user_id not in users_db:
        return jsonify({"error": "Сессия устарела."}), 404

    name = request.form.get("name", "").strip()
    status = request.form.get("status", "").strip()
    neon_color = request.form.get("neon_color", "#0ff")

    # Валидация цвета
    valid_colors = ["#0ff", "#f0f", "#ff0", "#0f0"]
    if neon_color not in valid_colors:
        neon_color = "#0ff"

    users_db[user_id].update({
        "name": name or "Аноним",
        "status": status or "Без статуса",
        "neon_color": neon_color
    })

    user = users_db[user_id]
    return render_template_string(
        LK_TEMPLATE,
        user_id=user_id,
        name=user["name"],
        status=user["status"],
        neon_color=user["neon_color"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
