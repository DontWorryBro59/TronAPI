from fastapi import APIRouter, HTTPException
from tron_fastapi.repositories import TronRepo
from tron_fastapi.config.config import logger
tn_router = APIRouter(tags=['Tron'], prefix='/tron')



@tn_router.post('/{address}')
async def check_adress(address: str):
    if not TronRepo.check_address(address):
        logger.error(f'Кошелек не найден: {address}')
        return HTTPException(status_code=404, detail="Кошелек не найден")
    logger.info(f'Получение данных для кошелька {address}')
    result = TronRepo.get_date_by_address(address)
    logger.info(f'Данные получены для кошелька {address}')
    return result


@tn_router.get('/')
async def get_requests(page: int = 1, page_size: int = 10):
    # Здесь нужно реализовать логику получения списка запросов
    pass
