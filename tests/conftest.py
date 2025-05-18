import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from db.init_data import initial_test_database
from main import app
from models.role import Role
from models.user import User
from services.auth import auth_service
from settings import env_settings


@pytest.fixture
async def init_test_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()
    await initial_test_database()
    yield
    await Tortoise.close_connections()


@pytest.fixture
async def client():
    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app)
    ) as ac:
        yield ac


@pytest.fixture
async def auth_client(init_test_db):
    user = await User.get(id=uuid.UUID('00000000-0000-4000-a000-000000000000'))
    
    token = await auth_service.create_refresh_token(str(user.id))

    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
    ) as ac:
        ac.cookies.set(env_settings.refresh_cookie_name, token)
        yield ac
