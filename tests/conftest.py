import asyncio
import json
from os import path
from typing import Any, AsyncGenerator, Dict, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.auth0 import get_auth0_access_token

from app.core.config import settings
from app.db.base import Base
from app.db.commands import create_init_data
from app.db.session import async_engine, async_session
from app.main import create_app

pytestmark = pytest.mark.asyncio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await create_init_data()

    session: AsyncSession
    async with async_session() as session:
        yield session
        await session.flush()
        await session.rollback()

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
async def app() -> AsyncGenerator[FastAPI, None]:
    _app: FastAPI = create_app()
    yield _app


@pytest.fixture(scope="module")
async def client(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=f"http://0.0.0.0:8888{settings.api.prefix}/v1",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="session")
def mock_fetch_psi() -> Dict[str, Any]:
    mocked_response = {}
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/utils/fetchpsi.json") as f:
        mocked_response = json.load(f)
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_sitemap() -> Dict[str, Any]:
    mocked_response = {}
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/utils/sitemap.json") as f:
        mocked_response = json.load(f)
    return mocked_response


@pytest.fixture(scope="session")
def admin_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_admin, settings.auth.first_admin_password
    )


@pytest.fixture(scope="session")
def manager_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_manager, settings.auth.first_manager_password
    )


@pytest.fixture(scope="session")
def employee_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_employee, settings.auth.first_employee_password
    )


@pytest.fixture(scope="session")
def client_a_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_client_a, settings.auth.first_client_a_password
    )


@pytest.fixture(scope="session")
def client_b_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_client_b, settings.auth.first_client_b_password
    )


@pytest.fixture(scope="session")
def user_verified_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_user_verified, settings.auth.first_user_verified_password
    )


@pytest.fixture(scope="session")
def user_unverified_token_headers() -> Dict[str, str]:
    return get_auth0_access_token(
        settings.auth.first_user_unverified,
        settings.auth.first_user_unverified_password,
    )
