from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WalletCreate(BaseModel):
    balance: float
    bandwidth: int
    energy: int

    model_config = ConfigDict(from_attributes=True)


class WalletBase(WalletCreate):
    address: str


class WalletFromDB(WalletBase):
    id: int
    request_date: datetime
