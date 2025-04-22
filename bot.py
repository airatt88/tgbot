import telebot
from flask import Flask, request
import requests
import random

# Токены
TELEGRAM_TOKEN = "8000909618:AAH9skOY44FOwjgWBFm9nm91jxf_HvpmIiY"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# GPT-функция
def ask_gpt(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://твоё-имя.railway.app"  # ОБЯЗАТЕЛЬНО замени на свой Railway домен!
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        data = response.json()
        if "choices" not in data:
            return f"⚠️ Ошибка с AI: {data.get('error', {}).get('message', 'Нет ответа')}"
        
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Ошибка: {e}"

# Хендлеры
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в Startup House! 🚀")

@bot.message_handler(commands=['ai'])
def ai(message):
    prompt = message.text.replace("/ai", "").strip()
    if not prompt:
        bot.reply_to(message, "Напиши вопрос после /ai, например `/ai как начать стартап?`")
    else:
        reply = ask_gpt(prompt)
        bot.send_message(message.chat.id, reply)

# Flask маршрут для вебхука
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

# Установка вебхука
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://твоё-имя.railway.app/{TELEGRAM_TOKEN}"  # Замени на свой Railway URL
    success = bot.set_webhook(url=webhook_url)
    return "Webhook set" if success else "Webhook failed", 200

# Запуск Flask-сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
