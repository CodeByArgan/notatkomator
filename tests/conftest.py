import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from tortoise import Tortoise
from main import app


@pytest.fixture
async def init_test_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture
async def client():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        yield ac
