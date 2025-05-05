import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from db.init_data import create_initial_database_data
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
    await create_initial_database_data()
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
    role, _ = await Role.get_or_create(name="user")
    user = await User.create(
        id=uuid.uuid4(),
        descope_user_id="mock-user-id",
        email="test@example.com",
        role=role,
    )
    token = await auth_service.create_refresh_token(str(user.id))

    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
    ) as ac:
        ac.cookies.set(env_settings.refresh_cookie_name, token)
        yield ac
