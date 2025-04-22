
import telebot
import os
import random
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_openrouter(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Добро пожаловать в Startup House! 🚀")

@bot.message_handler(commands=['ai'])
def ai_chat(message):
    question = message.text.replace('/ai', '').strip()
    if not question:
        bot.reply_to(message, "Напиши вопрос после команды /ai, например: `/ai как начать стартап?`")
    else:
        reply = ask_openrouter(question)
        bot.reply_to(message, reply)

@bot.message_handler(commands=['startup_idea'])
def startup_idea(message):
    prompt = "Придумай креативную идею стартапа, связанную с ИИ и технологиями. Ответ на русском языке:"
    idea = ask_openrouter(prompt)
    bot.reply_to(message, f"🚀 Идея: {idea}")

@bot.message_handler(commands=['name_gen'])
def name_gen(message):
    names = ["NeuroShift", "AIvatar", "BizMind AI", "InnovaCore", "CogniSpark"]
    name = random.choice(names)
    bot.reply_to(message, f"Как тебе название: {name}?")

@bot.message_handler(commands=['mentor'])
def mentor(message):
    tips = [
        "Начни с проблемы, а не с решения.",
        "Делай MVP и собирай фидбек.",
        "Сфокусируйся на одной аудитории сначала."
    ]
    tip = random.choice(tips)
    bot.reply_to(message, f"Совет от ментора: {tip}")

bot.infinity_polling()
