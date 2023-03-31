import asyncio
from os import environ
from typing import Any, AsyncGenerator, Callable, Dict, Generator

import pytest
import requests
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_async_db
from app.core.config import settings
from app.db.base import Base
from app.main import create_app

pytestmark = pytest.mark.asyncio


# test database setup
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)


def test_async_session_generator() -> async_sessionmaker:
    return test_async_session


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def celery_config() -> Any:
    return {"broker_url": "memory://", "result_backend": "rpc"}  # redis://


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    # create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # create new async session
    async_session = test_async_session_generator()
    session: AsyncSession
    async with async_session() as session:
        yield session
        await session.flush()
        await session.rollback()

    # drop all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    return _override_get_db


@pytest.fixture(scope="module")
async def app(
    override_get_db: Callable,
) -> AsyncGenerator[FastAPI, None]:
    _app: FastAPI = create_app()
    _app.dependency_overrides[get_async_db] = override_get_db
    yield _app


@pytest.fixture(scope="module")
async def client(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://0.0.0.0:8888{settings.API_PREFIX_V1}/",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="session")
def superuser_token_headers() -> Dict[str, str]:
    url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "password",
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "audience": settings.AUTH0_API_AUDIENCE,
        "scope": "openid profile email",
    }
    clid: str = environ.get("AUTH0_SPA_CLIENT_ID", "")
    clsh: str = environ.get("AUTH0_SPA_CLIENT_SECRET", "")
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=data, headers=headers, auth=(clid, clsh))
    data = response.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
