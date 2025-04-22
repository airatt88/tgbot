
# Startup AI Telegram Bot

Telegram-бот с идеями стартапов, AI-чатом и генератором названий для технологических проектов.

## Команды
- `/start` — Приветствие
- `/ai <вопрос>` — Задать вопрос ИИ
- `/startup_idea` — Получить стартап-идею
- `/name_gen` — Генерация названия
- `/mentor` — Советы от ментора

## Запуск
Создай файл `.env` или добавь переменные окружения:
- `TELEGRAM_TOKEN`
- `OPENROUTER_API_KEY`

Установи зависимости и запусти:
```bash
pip install -r requirements.txt
./start.sh
```
