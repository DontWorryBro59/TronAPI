import uvicorn
from fastapi import FastAPI

from tron_fastapi.routers.tron_routers import tn_router

app = FastAPI()
app.include_router(tn_router)

if __name__ == '__main__':
    uvicorn.run('main:app')
