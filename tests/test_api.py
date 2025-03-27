import os
import sys
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# Добавляем корневую папку в путь поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tron_fastapi.main import app
from tron_fastapi.database.db_helper import DatabaseHelper, db_help
from tron_fastapi.config.config import settings


# Используем SQLite in-memory для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Используем автоматическое управление циклом событий через pytest-asyncio
@pytest_asyncio.fixture(scope="session", autouse=True)
async def event_loop():
    """Automatically manage the event loop"""
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope="session")
def test_db_helper():
    """Create a test database helper"""
    return DatabaseHelper(url=TEST_DATABASE_URL, echo=False)


@pytest.fixture(scope="session", autouse=True)
def override_database(test_db_helper):
    """Change the database settings and override the database session"""
    settings.DATABASE_URL = TEST_DATABASE_URL
    app.dependency_overrides[db_help.get_session] = test_db_helper.get_session
    yield
    # Очищаем зависимости после тестов
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db(test_db_helper):
    """Clean up the test database"""
    await test_db_helper._destroy_all_tables()
    await test_db_helper.create_all_tables()
    yield


@pytest_asyncio.fixture(scope="session")
async def async_client():
    """Create async_client for testing"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as as_client:
        yield as_client


@pytest.mark.asyncio
async def test_get_wallet(async_client):
    """
    Check that the API returns the correct data for a valid wallet address
    and post wallet's data in DB
    """
    response = await async_client.post("/tron/TYh6mgoMNZTCsgpYHBz7gttEfrQmDMABub")

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_wallet_error(async_client):
    """
    Check that the API returns the correct error message for an invalid wallet address.
    """
    test_wallet = "my_test_wallet"
    response = await async_client.post(f"/tron/{test_wallet}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Wallet not found with adress: {test_wallet}"


@pytest.mark.asyncio
async def test_get_all_wallets(async_client):
    """
    Test that the API returns a list of wallets.
    """
    test_wallet = "TYh6mgoMNZTCsgpYHBz7gttEfrQmDMABub"
    await async_client.post(f"/tron/{test_wallet}")
    response = await async_client.get("/tron/")

    assert response.status_code == 200
    assert response.json()[0].get("address") == test_wallet
