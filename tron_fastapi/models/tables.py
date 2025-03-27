from datetime import datetime
from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from tron_fastapi.models.base import Base


class AddressRequestORM(Base):
    """
    This is a class that represents a request for a TRON address.
    """

    __tablename__ = "address_requests"

    address: Mapped[str]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    balance: Mapped[int]
    request_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
