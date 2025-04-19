from fastapi import FastAPI
from tortoise import Tortoise
from contextlib import asynccontextmanager

from endpoints.audit_log import audit_log_router

from db.config import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


app.include_router(audit_log_router)
