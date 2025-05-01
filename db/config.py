from settings import env_settings


TORTOISE_ORM = {
    "connections": {"default": env_settings.db_url},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
