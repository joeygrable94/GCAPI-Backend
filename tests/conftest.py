import asyncio
import json
from os import environ, path
from typing import Any, AsyncGenerator, Dict, Generator

import pytest
import requests
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.base import Base
from app.db.session import async_engine, async_session
from app.main import create_app

pytestmark = pytest.mark.asyncio


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
    return {"broker_url": "memory://", "result_backend": "rpc"}


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
            base_url=f"http://0.0.0.0:8888{settings.api.prefix}",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="session")
def superuser_token_headers() -> Dict[str, str]:
    url = f"https://{settings.auth.domain}/oauth/token"
    data = {
        "grant_type": "password",
        "username": settings.auth.first_superuser,
        "password": settings.auth.first_superuser_password,
        "audience": settings.auth.audience,
        "scope": "openid profile email",
    }
    clid: str | None = environ.get("AUTH0_SPA_CLIENT_ID", None)
    clsh: str | None = environ.get("AUTH0_SPA_CLIENT_SECRET", None)
    if clid is None:
        raise ValueError("AUTH0_SPA_CLIENT_ID is not set")
    if clsh is None:
        raise ValueError("AUTH0_SPA_CLIENT_SECRET is not set")
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=data, headers=headers, auth=(clid, clsh))
    data = response.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


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
