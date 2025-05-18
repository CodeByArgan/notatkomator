from uuid import UUID
from models.medium import Medium
from models.notes import Note
from models.role import Role
from models.user import User


async def create_initial_database_data():
    for role_name in ["user", "admin"]:
        await Role.get_or_create(name=role_name)



async def initial_test_database():
    await create_initial_database_data()
    role_user, _ = await Role.get_or_create(name="user")
    role_admin, _ = await Role.get_or_create(name="admin")

    user = await User.create(
        id=UUID('00000000-0000-4000-a000-000000000000'),
        descope_user_id="a",
        email="user@system.com",
        is_banned=False,
        role=role_user
    )

    admin = await User.create(
        id=UUID('00000000-0000-4000-a000-000000000001'),
        descope_user_id="b",
        email="admin@system.com",
        is_banned=False,
        role=role_admin
    )

    medium1 = await Medium.create(
        id=UUID('00000000-0000-4000-a000-000000000000'),
        name="A",
        type="book",
        creator=user
    )

    medium2 = await Medium.create(
        id=UUID('00000000-0000-4000-a000-000000000001'),
        name="B",
        type="movie",
        creator=admin
    )


    await Medium.create(
        id=UUID('00000000-0000-4000-a000-000000000002'),
        name="D",
        type="game",
        creator=user
    )

    await Note.create(
        id=UUID('00000000-0000-4000-a000-000000000000'),
        user=user,
        medium=medium1
    )

    await Note.create(
        id=UUID('00000000-0000-4000-a000-000000000001'),
        user=user,
        medium=medium2
    )