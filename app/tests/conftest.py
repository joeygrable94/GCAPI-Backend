import asyncio
from typing import AsyncGenerator, Callable, Generator

# import alembic
import pytest

# from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.config import settings
from app.db.init_db import build_database
from app.db.session import async_engine, async_session
from app.main import create_app

pytestmark = pytest.mark.anyio

settings.DEBUG_MODE = True
build_database()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator:
    async with async_engine.begin() as async_conn:
        async with async_session(bind=async_conn) as session:
            yield session
            await session.flush()
            await session.rollback()
        await async_conn.close()


@pytest.fixture(scope="session")
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db() -> AsyncGenerator:
        yield db_session  # pragma: no cover

    return _override_get_db


@pytest.fixture(scope="module")
def app(
    override_get_db: Callable,
) -> Generator:
    app: FastAPI = create_app()
    app.dependency_overrides[get_async_db] = override_get_db
    yield app


@pytest.fixture(scope="module")
async def client(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://0.0.0.0:8888{settings.API_PREFIX_V1}/",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
