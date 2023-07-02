import os

from aiogram import types
from dotenv import load_dotenv

load_dotenv()

# Database
DB_ENGINE = os.getenv("DB_ENGINE", default="postgresql+psycopg2")
DB_NAME = os.getenv("DB_NAME", default="postgres3")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="postgres3")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="adm")
DB_HOST = os.getenv("DB_HOST", default="db")
DB_PORT = os.getenv("DB_PORT", default="5432")

# admin
ADMIN_IDs = [
    os.getenv("ADMIN_ID_1"),
]

# bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENTS_TOKEN = os.getenv("PAYMENTS_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

# manage.py
commands_bot = ("start_bot",)
commands_bot_admin = ("start_admin_bot",)

# bot.py
in_chat_commands = {
    "💵 Тарифы": "rates",
    "⏳ Мой тариф": None,
    "🆘 Поддержка": None,
    "📖 Подробная инструкция": None,
    "🤔 FAQ": None,
}

rates_commands = {
    "Базовый, 1 месяц / 100 ₽ / 2 📱": None,
    "Семейный, 6 месяцев / 500 ₽ / 5 📱": None,
    "Семейный, год / 950 ₽ / 5 📱": None,
    "Премиум, год / 1800 ₽ / 10 📱": None,
    "Бизнес, год / 9800 ₽": None,
    "Yota, Tele2 / 1 месяц / 100 ₽ / 2 📱": None,
    "Выбрать страну вручную 🇬🇧🇫🇮🇩🇪🇷🇺🇺🇸": "manual_rates",
}

manual_rates_commands = {
    "Базовый, 1 месяц / 🇬🇧 / 2 📱": None,
    "Базовый, 1 месяц / 🇫🇮 / 2 📱": None,
    "Базовый, 1 месяц / 🇩🇪 / 2 📱": None,
    "Базовый, 1 месяц / 🇺🇸 / 2 📱": None,
    "Базовый, 1 месяц / 🇷🇺 / 2 📱": None,
    "Семейный, 6 месяцев / 🇬🇧 / 5 📱": None,
    "Семейный, 6 месяцев / 🇫🇮 / 5 📱": None,
    "Семейный, 6 месяцев / 🇩🇪 / 5 📱": None,
    "Семейный, 6 месяцев / 🇺🇸 / 5 📱": None,
    "Семейный, 6 месяцев / Yota и Tele2 / 5 📱": None,
}

pay_commands = list(manual_rates_commands.keys()) + list(
    filter(lambda x: rates_commands[x] is None, rates_commands)
)


RATES = {
    "Базовый, 1 месяц / 100 ₽ / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "GB",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Семейный, 6 месяцев / 500 ₽ / 5 📱": {
        "name": "Базовый",
        "duration": 6,
        "measurement": "month",
        "country": "GB",
        "devices": 5,
        "price": 500 * 100,
        "currency": "RUB",
    },
    "Семейный, год / 950 ₽ / 5 📱": {
        "name": "Базовый",
        "duration": 12,
        "measurement": "month",
        "country": "GB",
        "devices": 5,
        "price": 950 * 100,
        "currency": "RUB",
    },
    "Премиум, год / 1800 ₽ / 10 📱": {
        "name": "Базовый",
        "duration": 12,
        "measurement": "month",
        "country": "GB",
        "devices": 10,
        "price": 1800 * 100,
        "currency": "RUB",
    },
    "Бизнес, год / 9800 ₽": {
        "name": "Базовый",
        "duration": 12,
        "measurement": "month",
        "country": "GB",
        "devices": 10,
        "price": 9800 * 100,
        "currency": "RUB",
    },
    "Yota, Tele2 / 1 месяц / 100 ₽ / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "GB",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Базовый, 1 месяц / 🇬🇧 / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "GB",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Базовый, 1 месяц / 🇫🇮 / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "FI",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Базовый, 1 месяц / 🇩🇪 / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "DE",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Базовый, 1 месяц / 🇺🇸 / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "US",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Базовый, 1 месяц / 🇷🇺 / 2 📱": {
        "name": "Базовый",
        "duration": 1,
        "measurement": "month",
        "country": "RU",
        "devices": 2,
        "price": 100 * 100,
        "currency": "RUB",
    },
    "Семейный, 6 месяцев / 🇬🇧 / 5 📱": {
        "name": "Семейный",
        "duration": 6,
        "measurement": "month",
        "country": "GB",
        "devices": 5,
        "price": 500 * 100,
        "currency": "RUB",
    },
    "Семейный, 6 месяцев / 🇫🇮 / 5 📱": {
        "name": "Семейный",
        "duration": 6,
        "measurement": "month",
        "country": "FI",
        "devices": 5,
        "price": 500 * 100,
        "currency": "RUB",
    },
    "Семейный, 6 месяцев / 🇩🇪 / 5 📱": {
        "name": "Семейный",
        "duration": 6,
        "measurement": "month",
        "country": "DE",
        "devices": 5,
        "price": 500 * 100,
        "currency": "RUB",
    },
    "Семейный, 6 месяцев / 🇺🇸 / 5 📱": {
        "name": "Семейный",
        "duration": 6,
        "measurement": "month",
        "country": "GB",
        "devices": 5,
        "price": 500 * 100,
        "currency": "RUB",
    },
    "Семейный, 6 месяцев / Yota и Tele2 / 5 📱": {
        "name": "Семейный",
        "duration": 6,
        "measurement": "month",
        "country": "RU",
        "devices": 5,
        "price": 500 * 100,
        "currency": "RUB",
    },
}


MEDIA_DIR = os.path.join(os.getcwd(), "media")
INFO_DIR = os.path.join(MEDIA_DIR, "info")

PHOTO_URL = "https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg"