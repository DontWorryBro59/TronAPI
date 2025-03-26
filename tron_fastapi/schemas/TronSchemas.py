from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WalletBase(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: float

    model_config = ConfigDict(from_attributes=True)


class WalletFromDB(WalletBase):
    id: int
    request_data: datetime
