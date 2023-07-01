from datetime import datetime, timedelta


def get_menu(kb, items):
    """Создает меню с переданными кнопками и коллбеками."""
    result = []
    tmp = []
    for index, data in enumerate(items.items()):
        btn, clbk = data
        tmp.append(kb(text=btn, callback_data=clbk))
        if index != 0 and index % 2 != 0:
            result.append(tmp)
            tmp = []
    if tmp:
        result.append(tmp)
    return result


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
        "devices": rate_data["devices"],
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


def get_outline_vpn_url():
    """Получение урла для коннекта с Outline"""
    return "https://some_new_shiny_socker.org/12345678"
