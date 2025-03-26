from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tron_fastapi.config.config import settings

from tron_fastapi.models.base import Base
from tron_fastapi.models.tables import Address_request # noqa
from tron_fastapi.config.config import logger

class DatabaseHelper:

    def __init__(self, url, echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bing=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False)

    async def create_all_tables(self):
        logger.info("Creating all tables")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _destroy_all_tables(self):
        logger.info("Destroying all tables")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db_help = DatabaseHelper(settings.DATABASE_URL, settings.DB_ECHO)