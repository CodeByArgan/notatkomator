TORTOISE_ORM = {
    "connections": {"default": "postgres://root:root@localhost:5432/notatkomator"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
