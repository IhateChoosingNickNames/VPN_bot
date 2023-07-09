import json
import os
from datetime import datetime, timedelta

from aiogram import types

import settings
from db.queries import create_certificate_in_db, delete_expired_rates


def get_kb(buttons, columns=2):
    """Создание клавиатуры с переданными кнопками, коллбеками и шириной."""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=columns)
    tmp = []
    for index, data in enumerate(buttons.items()):
        text, callback_data = data
        tmp.append(
            types.InlineKeyboardButton(text=text, callback_data=callback_data)
        )
        if index != 0 and index % columns != 0:
            kb.add(*tmp)
            tmp.clear()
    if tmp:
        kb.add(*tmp)
    return kb


def parse_message(message, rate_data):
    """Разбивает входящее сообщение от ТГ по необходимым для БД ключам."""
    user_info = {
        "tg_user_id": message["from"]["id"],
        "first_name": message["from"]["first_name"],
        "last_name": message["from"]["last_name"],
        "username": message["from"]["username"],
        "language_code": message["from"]["language_code"],
        "date": message["date"],
    }

    payment_data = {
        "currency": message["successful_payment"]["currency"],
        "total_amount": message["successful_payment"]["total_amount"],
        "invoice_payload": message["successful_payment"]["invoice_payload"],
        "telegram_payment_charge_id": message["successful_payment"][
            "telegram_payment_charge_id"
        ],
        "provider_payment_charge_id": message["successful_payment"][
            "provider_payment_charge_id"
        ],
        "rate_name": rate_data["name"],
        "country": rate_data["country"],
        "devices_total": rate_data["devices"],
        "devices_left": rate_data["devices"],
        "end_date": get_end_date(rate_data["duration"])
    }
    return {"user": user_info, "payment_data": payment_data}


def get_end_date(duration):
    """Получение даты окончания подписки."""
    mins_per_hour = 60
    hours_per_day = 24
    days_per_month = 30
    return datetime.now() + timedelta(
        minutes=mins_per_hour * hours_per_day * days_per_month * duration
    )


def _get_filename(username, user_id, current_cert_count):
    """Создание валидного имени файла."""
    return f"a{str(user_id)}_{current_cert_count}.ovpn"


def remove_expired_certificates():
    file_names = delete_expired_rates()
    for file_name in file_names:
        _remove_certificate_on_server(file_name[:-5])
        _remove_certificate_local(file_name)
        # TODO add sending message to the chat


def _get_json_data(script_name, file_name):
    return json.dumps({"script_name": script_name, "file_name": file_name})


def _create_certificate_on_server(file_name):
    """Создание .ovpn на сервере."""
    command = settings.SERVER_REQUEST_COMMAND
    data = _get_json_data(settings.SERVER_CREATE_SCRIPT_NAME, file_name)
    os.system(f"{command} {data!r}")


def _remove_certificate_on_server(file_name):
    """Удаление сертификата на сервере."""
    command = settings.SERVER_REQUEST_COMMAND
    data = _get_json_data(settings.SERVER_REMOVE_SCRIPT_NAME, file_name)
    os.system(f"{command} {data!r}")


def _remove_certificate_local(file_name):
    """Удаление .ovpn локально."""
    os.remove(os.path.join(settings.CERTIFICATE_VOLUME, file_name))


def get_config_file(username, user_id, current_cert_count, payment_info_id):
    """Отправка файла."""
    file_name = _get_filename(username, user_id, current_cert_count)
    _create_certificate_on_server(file_name[:-5])  # без расширения
    create_certificate_in_db(file_name, payment_info_id)
    return file_name
