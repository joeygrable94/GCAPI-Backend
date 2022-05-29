from typing import AsyncGenerator, Callable, Dict

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
from app.api.deps import get_async_db, get_user_db
from app.main import create_app
from app.tests.utils.user import (
    authentication_token_from_email,
    get_superuser_token_headers,
)

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
async def user_db_session() -> AsyncSession:
    from app.core.user_crud import (
        get_async_db_context,
        get_user_db_context,
    )
    async with get_async_db_context() as session:
        async with get_user_db_context(session) as user_db:
            yield user_db


@pytest_asyncio.fixture(scope="session")
async def user_manager() -> AsyncSession:
    from app.core.user_crud import (
        get_async_db_context,
        get_user_db_context,
        get_user_manager_context,
    )
    async with get_async_db_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                yield user_manager


@pytest_asyncio.fixture(scope="session")
def override_get_user_db(user_db_session: AsyncSession) -> Callable:
    async def _override_get_user_db():
        yield user_db_session
    return _override_get_user_db


@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest_asyncio.fixture(scope="module")
def app(
    override_get_db: Callable,
    override_get_user_db: Callable,
    apply_migrations: None
    ) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_async_db] = override_get_db
    app.dependency_overrides[get_user_db] = override_get_user_db
    return app


@pytest_asyncio.fixture(scope="module")
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://0.0.0.0:8888{settings.API_PREFIX}",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="module")
def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest_asyncio.fixture(scope="module")
def normal_user_token_headers(client: AsyncClient, db_session: AsyncSession) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client,
        email=settings.EMAIL_TEST_USER,
        db=db_session
    )

