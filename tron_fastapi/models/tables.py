from datetime import datetime
from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from tron_fastapi.models.base import Base


class Address_request(Base):
    """
    This is a class that represents a request for a TRON address.
    """

    address: Mapped[str]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    balance_trx: Mapped[int]
    request_date: Mapped[datetime] = mapped_column(
        DateTime, default=func.now().op("at time zone")("Europe/Moscow")
    )
