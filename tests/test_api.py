import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from tron_fastapi.main import app

client = TestClient(app)


def test_get_wallet():
    response = client.post("/tron/TYh6mgoMNZTCsgpYHBz7gttEfrQmDMABub")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_wallet_error():
    response = client.post("/tron/mytestvalue")
    assert response.status_code == 200
    assert response.json()["status_code"] == 404
    assert response.json()["detail"] == "Кошелек не найден"
