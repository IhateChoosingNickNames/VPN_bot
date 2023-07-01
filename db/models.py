from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """Моделька юзеров."""

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=True)
    username = Column(String(100))
    language_code = Column(String(10), nullable=True)
    date = Column(DateTime)
    payment_info_id = relationship("PaymentInfo", back_populates="user")

    def __repr__(self):
        return (
            f"id={self.id!r}, title={self.username[:15]!r}, "
            f"author={self.tg_user_id!r}"
        )


class PaymentInfo(Base):
    """Модель платежей."""

    __tablename__ = "PaymentInfo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(50))
    total_amount = Column(Integer)
    invoice_payload = Column(String(100))
    telegram_payment_charge_id = Column(String(200))
    provider_payment_charge_id = Column(String(200))
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", foreign_keys="PaymentInfo.user_id")
    # TODO добавить поля

    def __repr__(self):
        return (
            f"id={self.id!r}, username={self.user_id}, "
            f"currency={self.currency}, total_amount={self.total_amount}"
        )
