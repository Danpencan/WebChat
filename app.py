from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

# Файл для хранения сообщений
MESSAGES_FILE = "messages.json"

# Функция для загрузки сообщений из файла
def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Функция для сохранения сообщений в файл
def save_messages(messages):
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# Главная страница (чат)
@app.route("/")
def index():
    return render_template("index.html")

# Получить все сообщения (для скрипта)
@app.route("/messages")
def get_messages():
    messages = load_messages()
    return jsonify(messages)

# Отправить сообщение
@app.route("/send", methods=["POST"])
def send_message():
    username = request.form.get("username")
    text = request.form.get("text")
    
    if not username or not text:
        return "Ошибка: пустое сообщение!", 400
    
    messages = load_messages()
    messages.append({"username": username, "text": text})
    save_messages(messages)
    
    return "Сообщение отправлено!", 200

# Чтобы приложение знало порт на хостинге
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
