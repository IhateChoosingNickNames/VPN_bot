import asyncio
import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

import settings
from db.queries import (
    save_payment_info,
    get_current_rates,
    get_rate,
    decrease_devices_left,
    increase_certificate_number,
)
from . import messages
from .utils import get_kb, parse_message, get_config_file, remove_expired_certificates

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)
rate_data = {}  # Убрать

scheduler = AsyncIOScheduler()


async def search_expired_certificates():
    """Запуск поиска просроченных сертификатов."""
    remove_expired_certificates()


def start_bot():
    """Инициализация бота и планировщика."""
    # scheduler.add_job(search_expired_certificates, 'interval', hours=2)
    scheduler.add_job(search_expired_certificates, 'date', run_date=datetime(2023, 7, 9, 14, 3, 5))
    scheduler.start()
    executor.start_polling(dp, skip_updates=False)


@dp.message_handler(lambda message: message["text"] in ["/start", "◀️Назад"])
async def bot_start(message: types.Message):
    """Начало работы."""
    kb = get_kb(settings.in_chat_commands)
    await message.answer(messages.START_MESSAGE, reply_markup=kb)


@dp.message_handler(regexp="⏳ Мои тарифы")
async def bot_rate(message: types.Message):
    """Вывод текущего тарифа."""
    rates = get_current_rates(message["from"]["id"])
    if rates:
        buttons = {}
        for rate in rates:
            msg = f"🔛 Тариф: {rate.rate_name} // Устройства: {rate.devices_left} // Дата окончания: {rate.end_date} // Номер=={rate.id}"
            buttons[msg] = None
        kb = get_kb(buttons, 1)
        kb.add(types.InlineKeyboardButton(text="◀️Назад"))
        await message.answer("Выберите тариф:", reply_markup=kb)
    else:
        await message.answer(messages.NO_RATE_MESSAGE, parse_mode="HTML")


@dp.message_handler(regexp="🔛 Тариф.*")
async def bot_current_rate(message: types.Message):
    try:
        id_ = int(message.text.split("==")[-1])
        choosen_rate = get_rate(id_)
        if choosen_rate.end_date < datetime.now():
            await message.answer("Подписка закончилась =(", parse_mode="HTML")
        elif choosen_rate.devices_left == 0:
            await message.answer(
                "По этому тарифу вы больше не можете добавлять устройства."
            )
        else:
            await message.answer(messages.OPEN_VPN_MESSAGE, parse_mode="HTML")
            file_name = get_config_file(
                username=message["from"]["username"],
                user_id=message["from"]["id"],
                current_cert_count=choosen_rate.user.certificate_number,
                payment_info_id=choosen_rate.id
            )
            decrease_devices_left(id_)
            increase_certificate_number(message["from"]["id"])
            file_path = os.path.join(settings.CERTIFICATE_VOLUME, file_name)
            await message.answer_document(document=open(file_path, "rb"))
    except Exception:  # добавить нормальную обработку
        await message.answer("Что-то пошло не так.", parse_mode="HTML")


@dp.message_handler(regexp="🆘 Поддержка")
async def bot_support(message: types.Message):
    """Вывод информации о поддержке."""
    await message.answer(messages.SUPPORT_MESSAGE, parse_mode="HTML")


@dp.message_handler(regexp="🤔 FAQ")
async def bot_faq(message: types.Message):
    """Вывод FAQ."""
    for msg in messages.FAQ_MESSAGES:
        await message.answer(msg, parse_mode="HTML")


@dp.message_handler(regexp="📖 Подробная инструкция")
async def bot_info(message: types.Message):
    """Вывод подробной инструкции пользования."""
    for msg, pic_path in messages.INFO_MESSAGES_MAPPER.items():
        if pic_path is not None:
            with open(os.path.join(settings.INFO_DIR, pic_path), "rb") as file:
                await message.answer_photo(
                    photo=file, caption=msg, parse_mode="HTML"
                )
        else:
            await message.answer(msg, parse_mode="HTML")


@dp.message_handler(lambda message: message["text"] in ["💵 Тарифы", "🔙 Назад"])
async def bot_rates(message: types.Message):
    """Дефолтные тарифы."""
    kb = get_kb(settings.rates_commands)
    kb.add(types.InlineKeyboardButton(text="◀️Назад"))
    await message.answer(
        messages.RATES_START_MESSAGE, reply_markup=kb, parse_mode="HTML"
    )


@dp.message_handler(regexp="Выбрать страну вручную 🇬🇧🇫🇮🇩🇪🇷🇺🇺🇸")
async def bot_manual_rate(message: types.Message):
    """Расширенный выбор тарифа."""
    kb = get_kb(settings.manual_rates_commands)
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

    current_rate = settings.RATES[message["text"]]
    rate_data[message["from"]["id"]] = current_rate

    await bot.send_invoice(
        message.chat.id,
        title="Покупка подписки на ВПН",
        description=(
            f"Активация подписки на ВПН на {current_rate['duration']}"
            f" {current_rate['measurement']}"
        ),
        provider_token=settings.PAYMENTS_TOKEN,
        currency=f"{current_rate['currency']}",
        photo_url=settings.PHOTO_URL,
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[
            types.LabeledPrice(
                label="ВПН на {current_rate['duration']} месяц(-ев)",
                amount=current_rate["price"],
            )
        ],
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
    data = parse_message(message, rate_data[message["from"]["id"]])
    save_payment_info(data)
    await bot.send_message(
        message.chat.id,
        (
            f"Платеж на сумму {message.successful_payment.total_amount // 100}"
            f" {message.successful_payment.currency} прошел успешно!!!"
        ),
    )
    await bot.send_message(message.chat.id, "Выберите тариф:")
    await bot.send_message(
        message.chat.id,
        "Перейдите в раздел <b>Мои тарифы</b>, выберите нужный и следуйте инструкциям",
        parse_mode="HTML",
    )
    del rate_data[message["from"]["id"]]
