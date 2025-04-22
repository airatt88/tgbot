import telebot
import random
import requests

TELEGRAM_TOKEN = "8000909618:AAH9skOY44FOwjgWBFm9nm91jxf_HvpmIiY"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# GPT-функция через OpenRouter
def ask_gpt(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://t.me/ytytyttybot",
            "X-Title": "Telegram Bot"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        data = response.json()

        print("Ответ от OpenRouter:", data)  # для логов Railway

        if response.status_code != 200 or "choices" not in data:
            error_msg = data.get("error", {}).get("message") or str(data)
            return f"⚠️ Ошибка с AI: {error_msg}"

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Ошибка: {e}"

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Добро пожаловать в Startup House! 🚀")

# Команда /ai
@bot.message_handler(commands=['ai'])
def ai_chat(message):
    question = message.text.replace('/ai', '').strip()
    if not question:
        bot.reply_to(message, "Напиши вопрос после /ai, например: `/ai как начать стартап?`")
    else:
        reply = ask_gpt(question)
        bot.reply_to(message, reply)

# Команда /startup_idea
@bot.message_handler(commands=['startup_idea'])
def startup_idea(message):
    prompt = "Придумай креативную идею стартапа, связанную с ИИ и технологиями. Ответ на русском языке:"
    idea = ask_gpt(prompt)
    bot.reply_to(message, f"🚀 Идея: {idea}")

# Команда /name_gen
@bot.message_handler(commands=['name_gen'])
def name_gen(message):
    names = ["NeuroShift", "AIvatar", "BizMind AI", "InnovaCore", "CogniSpark"]
    name = random.choice(names)
    bot.reply_to(message, f"Как тебе название: {name}?")

# Команда /mentor
@bot.message_handler(commands=['mentor'])
def mentor(message):
    tips = [
        "Начни с проблемы, а не с решения.",
        "Делай MVP и собирай фидбек.",
        "Сфокусируйся на одной аудитории сначала."
    ]
    tip = random.choice(tips)
    bot.reply_to(message, f"Совет от ментора: {tip}")

# Команда /help — показать все команды
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, """
📌 Доступные команды:
/start — Приветствие
/help — Все команды
/ai [вопрос] — Задать вопрос AI
/startup_idea — Генерация AI-стартапа
/name_gen — Придумать название
/mentor — Совет от ментора
""")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True, interval=0)

