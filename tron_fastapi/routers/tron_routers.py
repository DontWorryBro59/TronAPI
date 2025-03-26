from fastapi import APIRouter

tn_router = APIRouter(tags=['Tron'], prefix='/tron')


@tn_router.post('/{address}')
async def check_adress(address: str):
    # Здесь нужно реализовать логику получения информации о кошельке
    # и записи ее в базу данных
    pass


@tn_router.get('/')
async def get_requests(page: int = 1, page_size: int = 10):
    # Здесь нужно реализовать логику получения списка запросов
    pass
