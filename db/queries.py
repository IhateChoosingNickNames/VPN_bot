from datetime import datetime

from .base import engine, get_session
from .models import Key, User, PaymentInfo


def get_info():
    """Получение всех платежей."""
    current_session = get_session(engine)
    return current_session.query(PaymentInfo).all()


def _get_expired_keys():
    """Удаление всех просроченных сертификатов из БД."""
    current_session = get_session(engine)
    keys = []
    expired_rates = (
        current_session.query(PaymentInfo)
        .join(Key)
        .filter(PaymentInfo.end_date > datetime.now())
        .all()
    )

    for rate in expired_rates:
        for key in rate.keys:
            keys.append((rate.country, key.key_id))
            key.is_active = False
        current_session.commit()
    return keys


def decrease_devices_left(payment_id):
    """Уменьшить кол-во оставшихся девайсов на 1."""
    current_session = get_session(engine)
    current_session.query(PaymentInfo).filter_by(id=payment_id).update(
        {"devices_left": PaymentInfo.devices_left - 1}
    )
    current_session.commit()


def increase_key_count(user_id):
    """Наращивание счетчика полученных пользователем сертификатов."""
    current_session = get_session(engine)
    current_session.query(User).filter_by(tg_user_id=user_id).update(
        {"key_count": User.key_count + 1}
    )
    current_session.commit()


def _save_key_in_db(key, key_name, key_id, payment_info_id):
    current_session = get_session(engine)
    new_key = Key(
        key=key,
        key_name=key_name,
        key_id=key_id,
        payment_info_id=payment_info_id,
    )
    current_session.add(new_key)
    current_session.commit()


def get_rate(id_):
    """Достать текущий тариф"""
    current_session = get_session(engine)
    return current_session.query(PaymentInfo).filter_by(id=id_).first()


def get_current_rates(tg_user_id):
    """Получение всех текущих тарифов."""
    current_session = get_session(engine)
    rates = (
        current_session.query(PaymentInfo)
        .join(User)
        .filter_by(tg_user_id=tg_user_id)
        .filter(PaymentInfo.end_date >= datetime.now())
        .filter(PaymentInfo.devices_left > 0)
        .all()
    )
    return rates


def get_or_create_user(current_session, data):
    """Достать пользователя из БД или создать нового."""
    instance = (
        current_session.query(User)
        .filter(User.tg_user_id == data["tg_user_id"])
        .first()
    )

    if not instance:
        instance = User(**data)
        current_session.add(instance)
        current_session.commit()

    return instance


def save_payment_info(data):
    """Добавление платежа в БД."""
    current_session = get_session(engine)
    user = get_or_create_user(current_session, data["user"])
    payment_data = data["payment_data"]
    new_payment = PaymentInfo(user_id=user.id, **payment_data)
    current_session.add(new_payment)
    current_session.commit()
