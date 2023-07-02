from .base import engine, get_session
from .models import User, PaymentInfo


def get_info():
    """Получение всех платежей."""
    current_session = get_session(engine)
    return current_session.query(PaymentInfo).all()


def get_current_rate(tg_user_id):
    """Получение всех текущих тарифов."""
    current_session = get_session(engine)
    rates = (
        current_session.query(PaymentInfo).join(User)
        .filter_by(tg_user_id=tg_user_id)
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
