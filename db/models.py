from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """Модель юзеров."""

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(Integer)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=True)
    username = Column(String(100))
    language_code = Column(String(10), nullable=True)
    date = Column(DateTime)
    certificate_number = Column(Integer, default=1)
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
    rate_name = Column(String(50))
    country = Column(String(50))
    devices_total = Column(Integer)
    devices_left = Column(Integer)
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User", foreign_keys="PaymentInfo.user_id")
    certificate_id = relationship(
        "Certificate",
        cascade="all, delete-orphan",
        back_populates="payment_info",
    )

    def __repr__(self):
        return (
            f"id={self.id!r}, user_id={self.user_id}, "
            f"currency={self.currency}, total_amount={self.total_amount}"
        )


class Certificate(Base):
    """Модель сертификатов."""

    __tablename__ = "Certificate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(150))
    payment_info_id = Column(Integer, ForeignKey("PaymentInfo.id"))
    payment_info = relationship(
        "PaymentInfo", foreign_keys="Certificate.payment_info_id"
    )

    def __repr__(self):
        return f"id={self.id!r}, name={self.file_name}"
