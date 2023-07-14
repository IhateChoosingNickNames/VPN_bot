import calendar
from datetime import datetime

import requests
from aiogram import types

import settings
from db.queries import _save_key_in_db, _get_expired_keys


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
        "end_date": _get_end_date(rate_data["duration"]),
    }
    return {"user": user_info, "payment_data": payment_data}


def _get_end_date(months):
    """Получение даты окончания подписки."""
    sourcedate = datetime.now()
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime(
        year=year,
        month=month,
        day=day,
        hour=sourcedate.hour,
        minute=sourcedate.minute,
        second=sourcedate.second,
    )


def _get_key_name(username, user_id, key_count):
    """Создание валидного имени файла."""
    return f"a{str(user_id)}_{key_count}"


def _get_request_data(key_name=None, create=True, key_id=None):
    return {"key_name": key_name, "create": create, "key_id": key_id}


def _create_key(server, key_name):
    """Создание .ovpn на сервере."""
    response = requests.post(server, json=_get_request_data(key_name)).json()
    return response["key"], response["key_id"]


def _delete_key(server, key_id):
    """Создание .ovpn на сервере."""
    requests.post(server, json=_get_request_data(create=False, key_id=key_id))


def _create_url(url):
    return settings.OUTLINE_URL + url


def _choose_server(server):
    return settings.SOCKETS[server]


def _is_subscribe_expired(current_rate):
    return current_rate.end_date < datetime.now()


def remove_expired_keys():
    keys = _get_expired_keys()
    for country_name, key_id in keys:
        _delete_key(_choose_server(country_name), key_id)
        # TODO add sending message to the chat


def get_outline_url(
    username, user_id, key_count, payment_info_id, choosen_rate
):
    """Отправка файла."""
    if _is_subscribe_expired(choosen_rate):
        return "Подписка закончилась =("
    server = _choose_server(choosen_rate.country)
    key_name = _get_key_name(username, user_id, key_count)
    key, key_id = _create_key(server, key_name)
    url = _create_url(key)
    _save_key_in_db(key, key_name, key_id, payment_info_id)
    return url
