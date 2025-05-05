from models.role import Role


async def create_initial_database_data():
    for role_name in ["user", "admin"]:
        await Role.get_or_create(name=role_name)
