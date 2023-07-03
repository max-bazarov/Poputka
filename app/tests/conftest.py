import asyncio
import json

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert
from app.auth.security import hash_password

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.rides.bookings.models import Booking
from app.rides.models import Car, Ride
from app.users.models import User


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    # rides = open_mock_json('rides')
    users = open_mock_json('users')

    for user in users:
        user['password'] = hash_password(password=user['password'])

    async with async_session_maker() as session:
        for Model, values in [
            (User, users),
            # (Ride, rides),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


# Взято из документации к pytest-asyncio
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client():
    async with AsyncClient(
        app=fastapi_app, base_url='http://test'
    ) as async_client:
        yield async_client
