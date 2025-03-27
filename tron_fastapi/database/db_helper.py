from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tron_fastapi.config.config import logger
from tron_fastapi.config.config import settings
from tron_fastapi.models.base import Base
from tron_fastapi.models.tables import AddressRequestORM  # noqa


class DatabaseHelper:
    """
    DatabaseHelper is a class that handles the creation of all the tables, destroy them
    and create a new session
    """

    def __init__(self, url, echo):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_all_tables(self):
        logger.info("Creating all tables")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _destroy_all_tables(self):
        logger.info("Destroying all tables")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get_session(self):
        db = self.session()
        try:
            yield db
        finally:
            await db.close()


db_helper = DatabaseHelper(settings.DATABASE_URL, settings.DB_ECHO)
