import uvicorn
from fastapi import FastAPI, HTTPException
from tronpy import Tron
app = FastAPI()
tron = Tron()

@app.post('/tron/{address}')
async def root(address:str):
    # Здесь нужно реализовать логику получения информации о кошельке
    # и записи ее в базу данных
    pass

@app.get('/tron')
async def get_requests(page: int = 1, page_size: int = 10):
    # Здесь нужно реализовать логику получения списка запросов
    pass

if __name__ == '__main__':
    uvicorn.run('main:app')
