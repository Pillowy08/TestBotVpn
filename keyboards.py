from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import GUIDE_URL, SUPPORT_USERNAME


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Тарифы VPN"), KeyboardButton(text="📋 Правила")],
            [KeyboardButton(text="📖 Гайд по подключению"), KeyboardButton(text="👥 Реферальная система")],
            [KeyboardButton(text="🎁 Промокод"), KeyboardButton(text="👤 Мой профиль")],
            [KeyboardButton(text="💬 Поддержка")]
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
        [InlineKeyboardButton(text="🔗 Копировать ссылку", url=referral_link)],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_referral_keyboard_callback() -> InlineKeyboardMarkup:
    """Клавиатура реферальной системы (с callback)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Показать ссылку", callback_data="show_referral_link")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_payment_keyboard(tariff: str, amount: int) -> InlineKeyboardMarkup:
    """Клавиатура оплаты"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 SBP (СБП)", callback_data=f"pay_sbp_{tariff}")],
        [InlineKeyboardButton(text="💳 Банковская карта", callback_data=f"pay_card_{tariff}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="tariffs")]
    ])
    return keyboard


def get_payment_method_keyboard() -> InlineKeyboardMarkup:
    """Выбор способа оплаты"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 SBP (СБП)", callback_data="pay_sbp")],
        [InlineKeyboardButton(text="💳 Банковская карта", callback_data="pay_card")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ])
    return keyboard


def get_support_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура поддержки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать в поддержку", url=f"https://t.me/{SUPPORT_USERNAME}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    return keyboard


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Админ панель"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="💰 Промокоды", callback_data="admin_promos")],
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
