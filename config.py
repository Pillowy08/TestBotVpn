import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Администраторы бота (список ID Telegram)
ADMINS = [
    int(os.getenv("ADMIN_ID", 0))  # Замените на ваш Telegram ID
]

# Тарифы VPN
TARIFFS = {
    "1_month": {
        "name": "1 месяц",
        "price": 99,
        "description": "Базовый тариф на 1 месяц"
    },
    "3_months": {
        "name": "3 месяца",
        "price": 249,
        "description": "Тариф на 3 месяца со скидкой 15%"
    },
    "6_months": {
        "name": "6 месяцев",
        "price": 449,
        "description": "Тариф на 6 месяцев с выгодой 25%"
    },
    "12_months": {
        "name": "12 месяцев",
        "price": 799,
        "description": "Годовой тариф с максимальной скидкой 35%"
    }
}

# Реферальная система
REFERRAL_PERCENT = 10  # Процент от покупки реферала

# Ссылка на гайд
GUIDE_URL = "https://telegra.ph/Kak-postavit-vpn-03-31"  # Замените на вашу ссылку

# Поддержка (username без @)
SUPPORT_USERNAME = "Pillowy08"

# Реквизиты для оплаты
PAYMENT_DETAILS = {
    "sbp": "+7 (XXX) XXX-XX-XX",  # Номер телефона для СБП
    "card": "XXXX XXXX XXXX XXXX"  # Номер карты (замените на свой)
}

# База данных
DATABASE_PATH = "database.db"
