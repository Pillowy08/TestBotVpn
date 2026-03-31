import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMINS, TARIFFS, REFERRAL_PERCENT, GUIDE_URL, SUPPORT_USERNAME, PAYMENT_DETAILS
from keyboards import (
    get_main_keyboard, get_tariffs_keyboard, get_guide_keyboard,
    get_referral_keyboard, get_payment_keyboard, get_admin_keyboard, get_back_keyboard,
    get_support_keyboard
)
from database import (
    add_user, get_user, update_balance, add_purchase,
    get_promo_code, activate_promo_code, get_referrers_stats,
    get_all_users, add_promo_code
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# Машина состояний для промокодов
class PromoCodeState(StatesGroup):
    waiting_for_code = State()


class AdminPromoState(StatesGroup):
    waiting_for_code = State()
    waiting_for_discount = State()
    waiting_for_max_uses = State()


# ================== ХЕНДЛЕРЫ ==================

@dp.message(CommandStart(), F.args)
async def cmd_start_with_args(message: Message, command: CommandStart):
    """Обработчик команды /start с аргументами (реферал)"""
    user = message.from_user

    referrer_id = None
    try:
        referrer_id = int(command.args[0])
        if referrer_id == user.id:
            referrer_id = None
    except (ValueError, IndexError):
        referrer_id = None

    add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        referrer_id=referrer_id
    )

    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в VPN Store!

🔐 Надежный VPN для любых задач
⚡ Высокая скорость и стабильность
🌍 Серверы по всему миру

Выберите действие в меню:
"""

    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start без аргументов"""
    user = message.from_user

    add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        referrer_id=None
    )

    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в VPN Store!

🔐 Надежный VPN для любых задач
⚡ Высокая скорость и стабильность
🌍 Серверы по всему миру

Выберите действие в меню:
"""

    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@dp.message(F.text == "📦 Тарифы VPN")
async def show_tariffs(message: types.Message):
    """Показать тарифы"""
    text = """
📦 **ТАРИФЫ VPN**

Выберите подходящий тариф:

💎 Все тарифы включают:
• Безлимитный трафик
• Высокая скорость
• Поддержка 24/7
• Гарантия возврата 7 дней
"""
    await message.answer(text, reply_markup=get_tariffs_keyboard(), parse_mode="Markdown")


@dp.message(F.text == "📋 Правила")
async def show_rules(message: types.Message):
    """Показать правила"""
    text = """
📋 **ПРАВИЛА ИСПОЛЬЗОВАНИЯ**

1️⃣ **Общие положения**
• Сервис предоставляется на условиях подписки
• Один аккаунт = одно устройство одновременно

2️⃣ **Запрещено**
• Использовать VPN для незаконной деятельности
• Распространять доступ третьим лицам
• Обходить ограничения сервиса

3️⃣ **Возврат средств**
• Гарантия возврата в течение 7 дней
• При условии использования < 10 ГБ трафика

4️⃣ **Техническая поддержка**
• Поддержка 24/7 через бота
• Среднее время ответа: 15 минут

5️⃣ **Конфиденциальность**
• Мы не ведем логи вашей активности
• Данные шифруются по протоколу AES-256
"""
    await message.answer(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")


@dp.message(F.text == "📖 Гайд по подключению")
async def show_guide(message: types.Message):
    """Показать гайд"""
    text = f"""
📖 **ГАЙД ПО ПОДКЛЮЧЕНИЮ**

Подробная инструкция по настройке VPN доступна по кнопке ниже.

📱 Поддерживаемые платформы:
• Android
• iOS
• Windows
• macOS
• Linux

Нажмите кнопку, чтобы открыть гайд:
"""
    await message.answer(text, reply_markup=get_guide_keyboard(), parse_mode="Markdown")


@dp.message(F.text == "👥 Реферальная система")
async def show_referral(message: types.Message):
    """Показать реферальную систему"""
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("❌ Пользователь не найден. Нажмите /start")
        return

    stats = get_referrers_stats(message.from_user.id)
    referral_link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"

    text = f"""
👥 **РЕФЕРАЛЬНАЯ СИСТЕМА**

🎁 **Бонус за друга: 10₽**

Приглашайте друзей и получайте **10₽** за каждого!
Также получайте **{REFERRAL_PERCENT}%** с каждой их покупки!

📊 **Ваша статистика:**
• Приглашено друзей: {stats['total_referrals']}
• Заработано за друзей: {stats['total_earned']}₽

💰 **Ваш баланс:** {user['balance']}₽

🔗 **Ваша реферальная ссылка:**
`{referral_link}`

Отправьте ссылку друзьям и получайте 10₽ за каждого!
"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Копировать ссылку", url=referral_link)],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.message(F.text == "🎁 Промокод")
async def ask_promo_code(message: types.Message, state: FSMContext):
    """Запрос промокода"""
    await state.set_state(PromoCodeState.waiting_for_code)
    
    text = """
🎁 **АКТИВАЦИЯ ПРОМОКОДА**

Введите промокод для активации:

💡 Промокод можно получить:
• У партнеров сервиса
• В социальных сетях
• У друзей
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.message(PromoCodeState.waiting_for_code)
async def process_promo_code(message: types.Message, state: FSMContext):
    """Обработка промокода"""
    code = message.text.strip().upper()
    
    promo = get_promo_code(code)
    
    if not promo:
        await message.answer("❌ Промокод не найден или уже использован.")
        await state.clear()
        return
    
    # Проверяем, не активировал ли уже пользователь этот промокод
    user = get_user(message.from_user.id)
    
    # Активируем промокод
    if activate_promo_code(user['telegram_id'], promo['id']):
        # Начисляем бонус на баланс
        bonus = promo['discount']
        update_balance(user['telegram_id'], bonus)
        
        await message.answer(
            f"✅ **Промокод активирован!**\n\n"
            f"Вам начислено: **{bonus}₽**\n"
            f"Новый баланс: {user['balance'] + bonus}₽",
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Вы уже активировали этот промокод.")
    
    await state.clear()


@dp.message(F.text == "👤 Мой профиль")
async def show_profile(message: types.Message):
    """Показать профиль пользователя"""
    user = get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Пользователь не найден. Нажмите /start")
        return
    
    text = f"""
👤 **ВАШ ПРОФИЛЬ**

📛 Имя: {user['first_name']}
🆔 ID: `{user['telegram_id']}`
💰 Баланс: {user['balance']}₽
📅 Регистрация: {user['created_at']}

🔗 Для пополнения баланса обратитесь к администратору.
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="topup_balance")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.message(F.text == "💬 Поддержка")
async def show_support(message: types.Message):
    """Показать поддержку"""
    text = f"""
💬 **ПОДДЕРЖКА**

Если у вас возникли вопросы или проблемы, напишите в нашу службу поддержки.

📱 **Наша поддержка:** @{SUPPORT_USERNAME}

⏰ Среднее время ответа: 5-15 минут

Нажмите кнопку ниже, чтобы связаться с нами:
"""
    await message.answer(text, reply_markup=get_support_keyboard(), parse_mode="Markdown")


# ================== CALLBACK QUERY ==================

@dp.callback_query(F.data == "main_menu")
async def go_main(callback: types.CallbackQuery):
    """Вернуться в главное меню"""
    await callback.message.edit_reply_markup(reply_markup=get_main_keyboard())


@dp.callback_query(F.data.startswith("tariff_"))
async def select_tariff(callback: types.CallbackQuery):
    """Выбор тарифа"""
    tariff_key = callback.data.replace("tariff_", "")
    tariff = TARIFFS.get(tariff_key)
    
    if not tariff:
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return
    
    text = f"""
📦 **{tariff['name']}**

{tariff['description']}

💵 **Цена:** {tariff['price']}₽

✅ После оплаты вы получите:
• Ключ доступа
• Инструкцию по настройке
• Доступ в поддержку
"""
    
    await callback.message.edit_text(text, reply_markup=get_payment_keyboard(tariff_key, tariff['price']), parse_mode="Markdown")


@dp.callback_query(F.data == "tariffs")
async def back_to_tariffs(callback: types.CallbackQuery):
    """Назад к тарифам"""
    await callback.message.edit_text(
        "📦 Выберите тариф:",
        reply_markup=get_tariffs_keyboard()
    )


@dp.callback_query(F.data.startswith("pay_sbp_"))
async def process_payment_sbp(callback: types.CallbackQuery):
    """Обработка оплаты через СБП"""
    tariff_key = callback.data.replace("pay_sbp_", "")
    tariff = TARIFFS.get(tariff_key)

    if not tariff:
        await callback.answer("❌ Ошибка оплаты", show_alert=True)
        return

    text = f"""
💳 **ОПЛАТА ЧЕРЕЗ СБП**

📦 Тариф: **{tariff['name']}**
💵 К оплате: **{tariff['price']}₽**

**Реквизиты для оплаты:**
`{PAYMENT_DETAILS['sbp']}`

**Инструкция:**
1. Откройте приложение вашего банка
2. Выберите "Оплата по СБП"
3. Введите номер телефона
4. Укажите сумму: {tariff['price']}₽
5. После оплаты отправьте чек в поддержку: @{SUPPORT_USERNAME}

⏰ После подтверждения оплаты вы получите ключ доступа в течение 5 минут.
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать в поддержку", url=f"https://t.me/{SUPPORT_USERNAME}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="tariffs")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query(F.data.startswith("pay_card_"))
async def process_payment_card(callback: types.CallbackQuery):
    """Обработка оплаты картой"""
    tariff_key = callback.data.replace("pay_card_", "")
    tariff = TARIFFS.get(tariff_key)

    if not tariff:
        await callback.answer("❌ Ошибка оплаты", show_alert=True)
        return

    text = f"""
💳 **ОПЛАТА БАНКОВСКОЙ КАРТОЙ**

📦 Тариф: **{tariff['name']}**
💵 К оплате: **{tariff['price']}₽**

**Реквизиты для оплаты:**
`{PAYMENT_DETAILS['card']}`

**Инструкция:**
1. Откройте приложение вашего банка
2. Переведите сумму: {tariff['price']}₽
3. После оплаты отправьте чек в поддержку: @{SUPPORT_USERNAME}

⏰ После подтверждения оплаты вы получите ключ доступа в течение 5 минут.
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать в поддержку", url=f"https://t.me/{SUPPORT_USERNAME}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="tariffs")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query(F.data == "topup_balance")
async def topup_balance_handler(callback: types.CallbackQuery):
    """Пополнение баланса"""
    text = """
💳 **ПОПОЛНЕНИЕ БАЛАНСА**

Выберите способ оплаты:

💳 **СБП (Система Быстрых Платежей)**
• Мгновенно
• Без комиссии
• Номер: +7 (XXX) XXX-XX-XX

💳 **Банковская карта**
• Мгновенно
• Комиссия: 0%
• Номер: XXXX XXXX XXXX XXXX

**После оплаты:**
1. Отправьте чек в поддержку: @Pillowy08
2. Укажите ваш Telegram ID
3. Баланс будет пополнен в течение 5 минут
"""
    await callback.message.answer(text, reply_markup=get_payment_method_keyboard(), parse_mode="Markdown")


# ================== АДМИН ПАНЕЛЬ ==================

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Админ панель"""
    if message.from_user.id not in ADMINS:
        return
    
    text = "🔧 **АДМИН ПАНЕЛЬ**"
    await message.answer(text, reply_markup=get_admin_keyboard(), parse_mode="Markdown")


@dp.callback_query(F.data == "admin_users")
async def admin_users(callback: types.CallbackQuery):
    """Просмотр пользователей"""
    if callback.from_user.id not in ADMINS:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    users = get_all_users()
    
    text = "👥 **ПОЛЬЗОВАТЕЛИ**\n\n"
    for user in users:
        text += f"• {user['first_name']} (@{user['username'] or 'нет'}) - {user['balance']}₽\n"
    
    await callback.message.answer(text, parse_mode="Markdown")


@dp.callback_query(F.data == "admin_create_promo")
async def admin_create_promo_start(callback: types.CallbackQuery, state: FSMContext):
    """Создание промокода - шаг 1"""
    if callback.from_user.id not in ADMINS:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    await state.set_state(AdminPromoState.waiting_for_code)
    await callback.message.answer("Введите код промокода:")


@dp.message(AdminPromoState.waiting_for_code)
async def admin_promo_code_input(message: types.Message, state: FSMContext):
    """Создание промокода - шаг 2"""
    code = message.text.strip().upper()
    await state.update_data(code=code)
    await state.set_state(AdminPromoState.waiting_for_discount)
    await message.answer("Введите размер скидки (в рублях):")


@dp.message(AdminPromoState.waiting_for_discount)
async def admin_promo_discount_input(message: types.Message, state: FSMContext):
    """Создание промокода - шаг 3"""
    try:
        discount = float(message.text.strip())
    except ValueError:
        await message.answer("❌ Введите числовое значение:")
        return
    
    data = await state.get_data()
    await state.update_data(discount=discount)
    await state.set_state(AdminPromoState.waiting_for_max_uses)
    await message.answer("Введите максимальное количество использований:")


@dp.message(AdminPromoState.waiting_for_max_uses)
async def admin_promo_max_uses_input(message: types.Message, state: FSMContext):
    """Создание промокода - финал"""
    try:
        max_uses = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Введите целое число:")
        return
    
    data = await state.get_data()
    
    if add_promo_code(data['code'], data['discount'], max_uses):
        await message.answer(
            f"✅ Промокод создан!\n\n"
            f"Код: `{data['code']}`\n"
            f"Скидка: {data['discount']}₽\n"
            f"Использований: {max_uses}",
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Промокод с таким кодом уже существует.")
    
    await state.clear()


# ================== ЗАПУСК ==================

async def main():
    """Запуск бота"""
    logging.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
