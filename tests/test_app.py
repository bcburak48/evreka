import os
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.main import app, get_db
from database.database import Base
from unittest.mock import patch

os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
test_engine = create_engine(
    os.environ['DATABASE_URL'], connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


app.router.lifespan_context = lifespan


@patch('app.main.process_data.delay')
@pytest.mark.asyncio
async def test_receive_data(mock_delay):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "device_id": "device123",
            "latitude": 12.3456,
            "longitude": 65.4321,
            "speed": 55.5
        }
        response = await ac.post("/data", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Data received"}

    mock_delay.assert_called_once()
    args, kwargs = mock_delay.call_args
    assert args[0] == payload
