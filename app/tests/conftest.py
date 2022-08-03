import asyncio
from typing import AsyncGenerator, Callable, Dict, Generator

# import alembic
import pytest

# from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.config import settings
from app.core.security import get_user_manager
from app.core.security.manager import UserManager
from app.db.base import Base
from app.db.session import async_engine, async_session, engine
from app.main import create_app
from app.tests.utils.user import (
    authentication_token_from_email,
    get_superuser_token_headers,
    get_testuser_token_headers,
)

pytestmark = pytest.mark.asyncio


settings.DATABASE_URI = "sqlite:///./test.db"
settings.DATABASE_URI = "sqlite+aiosqlite:///./test.db"

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


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
        yield db_session

    return _override_get_db


@pytest.fixture(scope="session")
async def user_manager(db_session: AsyncSession) -> AsyncGenerator:
    yield UserManager(session=db_session)


@pytest.fixture(scope="session")
async def override_get_user_manager(db_session: AsyncSession) -> Callable:
    async def _override_get_user_manager() -> AsyncGenerator:
        yield UserManager(session=db_session)

    return _override_get_user_manager


@pytest.fixture(scope="module")
def app(
    override_get_db: Callable,
    override_get_user_manager: Callable,
) -> FastAPI:
    app: FastAPI = create_app()
    app.dependency_overrides[get_async_db] = override_get_db
    app.dependency_overrides[get_user_manager] = override_get_user_manager
    return app


@pytest.fixture(scope="module")
async def client(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://0.0.0.0:8888{settings.API_PREFIX_V1}",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client=client)


@pytest.fixture(scope="module")
async def testuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    return await get_testuser_token_headers(client=client)


@pytest.fixture(scope="module")
async def token_headers_from_email(
    client: AsyncClient, user_manager: UserManager
) -> Dict[str, str]:
    return await authentication_token_from_email(
        client=client, email=settings.TEST_NORMAL_USER, user_manager=user_manager
    )
