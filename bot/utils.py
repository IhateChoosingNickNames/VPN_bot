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


def parse_message(message):
    """Разбивает входящее сообщение от ТГ по необходимым для БД ключам."""
    user_info = {
        "tg_user_id": message["from"]["id"],
        "first_name": message["from"]["first_name"],
        "last_name": message["from"]["last_name"],
        "username": message["from"]["username"],
        "language_code": message["from"]["language_code"],
        "date": message["date"],
    }

    payment_info = {
        "currency": message["successful_payment"]["currency"],
        "total_amount": message["successful_payment"]["total_amount"],
        "invoice_payload": message["successful_payment"]["invoice_payload"],
        "telegram_payment_charge_id": message["successful_payment"][
            "telegram_payment_charge_id"
        ],
        "provider_payment_charge_id": message["successful_payment"][
            "provider_payment_charge_id"
        ],
    }

    return {"user": user_info, "payment_info": payment_info}


def get_outline_vpn_url():
    """Получение урла для коннекта с Outline"""
    pass
