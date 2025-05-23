from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from contextlib import asynccontextmanager

from db.init_data import create_initial_database_data
from settings import env_settings
from endpoints.audit_log import audit_log_router
from endpoints.auth import auth_router
from endpoints.medium import medium_router
from endpoints.notes import notes_router

from db.config import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    await create_initial_database_data()
    yield
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=env_settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audit_log_router)
app.include_router(auth_router)
app.include_router(medium_router)
app.include_router(notes_router)
