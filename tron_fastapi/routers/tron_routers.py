from typing import List, Union

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.TronSchemas import WalletBase
from tron_fastapi.config.config import logger
from tron_fastapi.database.db_helper import db_help
from tron_fastapi.models.tables import AddressRequestORM
from tron_fastapi.repositories import TronRepo, TronDB
from tron_fastapi.schemas.TronSchemas import WalletFromDB, WalletCreate

tn_router = APIRouter(tags=["Tron"], prefix="/tron")


@tn_router.post("/{address}")
async def check_address(
    address: str, session: AsyncSession = Depends(db_help.get_session)
):
    if not TronRepo.check_address(address):
        logger.error(f"Кошелек не найден: {address}")
        return HTTPException(status_code=404, detail="Кошелек не найден")
    # Получаем данные о кошельке и создаем экземпляр модели
    result = TronRepo.get_date_by_address(address)
    new_wallet = AddressRequestORM(address=address, **result)
    ##Записываем данные в БД и получаем ответ
    await TronDB.post_new_wallet(wallet=new_wallet, session=session)
    result = WalletCreate.parse_obj(result)
    return result


@tn_router.get("/")
async def get_requests(
    page: int = 1,
    page_size: int = 10,
    session: AsyncSession = Depends(db_help.get_session),
) -> List[WalletFromDB]:
    result = await TronDB.get_last_data(page=page, page_size=page_size, session=session)
    return result
