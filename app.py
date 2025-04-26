from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Путь к файлу с сообщениями
MESSAGES_FILE = 'messages.json'

# Если файл не существует — создаём пустой
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)

def load_messages():
    with open(MESSAGES_FILE, 'r') as f:
        return json.load(f)

def save_message(username, text):
    messages = load_messages()
    messages.append({'username': username, 'text': text})
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    username = request.form['username']
    text = request.form['text']
    save_message(username, text)
    return '', 204

@app.route('/messages')
def get_messages():
    return jsonify(load_messages())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
