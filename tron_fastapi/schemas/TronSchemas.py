from datetime import datetime

from pydantic import BaseModel


class WalletBase(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: float


class WalletFromDB(WalletBase):
    id: int
    request_data: datetime
