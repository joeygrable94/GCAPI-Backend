from typing import AsyncGenerator, Callable

import os
import warnings
import alembic
from alembic.config import Config
from asgi_lifespan import LifespanManager
import asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import pytest_asyncio

from app.core.config import settings
from app.db.session import async_engine, async_session
from app.api.deps import get_async_db
from app.main import create_app

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> AsyncGenerator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncSession:
    from app.db.base import Base
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(Base.metadata.drop_all)
        await async_conn.run_sync(Base.metadata.create_all)
        async with async_session(bind=async_conn) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture(scope="session")
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session
    return _override_get_db


@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest_asyncio.fixture
def app(override_get_db: Callable, apply_migrations: None) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_async_db] = override_get_db
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://0.0.0.0:8888{settings.API_PREFIX}",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client
