from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tron_fastapi.config.config import logger
from tron_fastapi.database.db_helper import db_helper
from tron_fastapi.models.tables import AddressRequestORM
from tron_fastapi.repositories.tron_repositories import TronRepo, TronDB
from tron_fastapi.schemas.TronSchemas import WalletFromDB, WalletCreate

tn_router = APIRouter(tags=["Tron"], prefix="/tron")


@tn_router.post("/{address}")
async def check_address(
    address: str, session: AsyncSession = Depends(db_helper.get_session)
) -> WalletCreate:
    if not await TronRepo.check_address(address):
        logger.error(f"Кошелек не найден: {address}")
        raise HTTPException(
            status_code=404, detail=f"Wallet not found with address: {address}"
        )
    # Получаем данные о кошельке и создаем экземпляр модели
    result = await TronRepo.get_data_by_address(address)
    new_wallet = AddressRequestORM(address=address, **result)
    ##Записываем данные в БД и получаем ответ
    await TronDB.post_new_wallet(wallet=new_wallet, session=session)
    result = WalletCreate.model_validate(result)
    return result


@tn_router.get("/")
async def get_requests(
    page: int = 1,
    page_size: int = 10,
    session: AsyncSession = Depends(db_helper.get_session),
) -> List[WalletFromDB]:
    result = await TronDB.get_last_data(page=page, page_size=page_size, session=session)
    return result
