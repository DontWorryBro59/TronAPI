from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from base import Base

class Address_request(Base):

    address: Mapped[str]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    balance_trx: Mapped[int]
    request_date: Mapped[DateTime] = mapped_column(default=func.now().op('at time zone')('Europe/Moscow'))
