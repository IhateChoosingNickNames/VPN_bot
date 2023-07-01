import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

import settings
from db.queries import save_payment_info, get_current_rate
from . import messages
from .utils import get_menu, parse_message, get_outline_vpn_url

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)
rate_data = {}  # Убрать


def start_bot():
    """Инициализация бота."""
    executor.start_polling(dp, skip_updates=False)


@dp.message_handler(lambda message: message["text"] in ["/start", "◀️Назад"])
async def bot_start(message: types.Message):
    """Начало работы."""
    menu = get_menu(types.InlineKeyboardButton, settings.in_chat_commands)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for elem in menu:
        kb.add(*elem)
    await message.answer(messages.start_message, reply_markup=kb)


@dp.message_handler(regexp="⏳ Мой тариф")
async def bot_rate(message: types.Message):
    """Вывод текущего тарифа."""
    # TODO добавить запрос к БД, сформировать ответ на "мой тариф"
    rates = get_current_rate(message["from"]["id"])
    if rates:
        for rate in rates:
            await message.answer(rate, parse_mode="HTML")
    else:
        await message.answer(messages.no_rate_message, parse_mode="HTML")


@dp.message_handler(regexp="🆘 Поддержка")
async def bot_support(message: types.Message):
    """Вывод информации о поддержке."""
    await message.answer(messages.support_message, parse_mode="HTML")


@dp.message_handler(regexp="🤔 FAQ")
async def bot_faq(message: types.Message):
    """Вывод FAQ."""
    for msg in messages.faq_message:
        await message.answer(msg, parse_mode="HTML")


@dp.message_handler(regexp="📖 Подробная инструкция")
async def bot_info(message: types.Message):
    """Вывод подробной инструкции пользования."""
    for msg, pic_path in messages.info_messages_mapper.items():
        if pic_path is not None:
            with open(os.path.join(settings.INFO_DIR, pic_path), "rb") as file:
                await message.answer_photo(
                    photo=file, caption=msg, parse_mode="HTML"
                )
        else:
            await message.answer(msg, parse_mode="HTML")


# @dp.callback_query_handler(lambda call: call.data=="rates")
@dp.message_handler(lambda message: message["text"] in ["💵 Тарифы", "🔙 Назад"])
async def bot_rates(message: types.Message):
    """Дефолтные тарифы."""
    menu = get_menu(types.InlineKeyboardButton, settings.rates_commands)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for elem in menu:
        kb.add(*elem)
    kb.add(types.InlineKeyboardButton(text="◀️Назад"))
    await message.answer(
        messages.rates_start_message, reply_markup=kb, parse_mode="HTML"
    )


@dp.message_handler(regexp="Выбрать страну вручную 🇬🇧🇫🇮🇩🇪🇷🇺🇺🇸")
async def bot_manual_rate(message: types.Message):
    """Расширенный выбор тарифа."""
    menu = get_menu(types.InlineKeyboardButton, settings.manual_rates_commands)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for elem in menu:
        kb.add(*elem)
    kb.add(types.InlineKeyboardButton(text="🔙 Назад"))
    await message.answer(
        "Выберете страну сервера и тариф.", reply_markup=kb, parse_mode="HTML"
    )


@dp.message_handler(lambda message: message["text"] in settings.pay_commands)
async def buy(message: types.Message):
    """Вывод окна с оплатой."""
    # TODO убрать при деплое
    if settings.PAYMENTS_TOKEN.split(":")[1] == "TEST":
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    rate_data[message["from"]["id"]] = settings.RATES[message["text"]]

    # TODO вынести в настройки все поля
    await bot.send_invoice(
        message.chat.id,
        title="Подписка на бота",
        description="Активация подписки на бота на 1 месяц",
        provider_token=settings.PAYMENTS_TOKEN,
        currency="rub",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=settings.PRICES,
        start_parameter="one-month-subscription",
        payload="test-invoice-payload",
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    """Проверка перед оплатой."""
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    """Отправка сообщения и ссылки на Outline после успешной оплаты."""
    data = parse_message(message)
    save_payment_info(data)
    url = get_outline_vpn_url()
    await bot.send_message(
        message.chat.id,
        (
            f"Платеж на сумму {message.successful_payment.total_amount // 100}"
            f" {message.successful_payment.currency} прошел успешно!!!"
        ),
    )
    await bot.send_message(message.chat.id, "Ваша ссылка на Outline VPN:")
    await bot.send_message(message.chat.id, url)
