from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from tron_fastapi.database.db_helper import db_helper
from tron_fastapi.routers.tron_routers import tn_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_helper.create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tn_router)

if __name__ == "__main__":
    uvicorn.run("main:app")
