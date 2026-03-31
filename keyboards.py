from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import GUIDE_URL


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Тарифы VPN"), KeyboardButton(text="📋 Правила")],
            [KeyboardButton(text="📖 Гайд по подключению"), KeyboardButton(text="👥 Реферальная система")],
            [KeyboardButton(text="🎁 Промокод"), KeyboardButton(text="👤 Мой профиль")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_tariffs_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с тарифами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц - 99₽", callback_data="tariff_1_month")],
        [InlineKeyboardButton(text="3 месяца - 249₽", callback_data="tariff_3_months")],
        [InlineKeyboardButton(text="6 месяцев - 449₽", callback_data="tariff_6_months")],
        [InlineKeyboardButton(text="12 месяцев - 799₽", callback_data="tariff_12_months")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_guide_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой гайда"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Открыть гайд", url=GUIDE_URL)],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_referral_keyboard(referral_link: str) -> InlineKeyboardMarkup:
    """Клавиатура реферальной системы"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Копировать ссылку", callback_data="copy_referral_link")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_payment_keyboard(tariff: str, amount: int) -> InlineKeyboardMarkup:
    """Клавиатура оплаты"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", callback_data=f"pay_{tariff}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="tariffs")]
    ])
    return keyboard


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Админ панель"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🎁 Создать промокод", callback_data="admin_create_promo")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой назад"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard
