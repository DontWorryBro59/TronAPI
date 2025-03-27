import asyncio
import pytest, pytest_asyncio
from sqlalchemy.orm import sessionmaker

from tron_fastapi.repositories.repositories import TronDB
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from tron_fastapi.models.tables import AddressRequestORM

# Создаем фейковый движок и сессию для тестов
async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")

SessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def event_loop():
    """Automatically manage the event loop"""
    loop = asyncio.get_event_loop()
    yield loop


# Создание таблиц перед тестами
@pytest_asyncio.fixture(scope="module")
async def setup_test_db():
    """Create tables before tests and delete them after"""
    async with async_engine.begin() as conn:
        await conn.run_sync(AddressRequestORM.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(AddressRequestORM.metadata.drop_all)


# Фикстура для сессии
@pytest_asyncio.fixture
async def session(setup_test_db):
    """Create a session for tests"""
    async with SessionLocal() as session:
        yield session


@pytest.mark.asyncio
async def test_get_last_data(session: AsyncSession):
    """
    Test the `get_last_data` method of the `TronDB` class.
    """
    result = await TronDB.get_last_data(page=1, page_size=10, session=session)
    assert result == []


@pytest.mark.asyncio
async def test_post_new_wallet(session: AsyncSession):
    """
    Test the `post_new_wallet` method of the `TronDB` class.
    """
    test_wallet = AddressRequestORM(
        address="test_wallet", bandwidth=0, energy=0, balance=0
    )
    await TronDB.post_new_wallet(test_wallet, session)
    result = await TronDB.get_last_data(page=1, page_size=10, session=session)
    assert len(result) == 1
    assert result[0].address == "test_wallet"
    assert result[0].bandwidth == 0
    assert result[0].energy == 0
    assert result[0].balance == 0
