import asyncio
import json
from os import path, remove
from typing import Any, AsyncGenerator, Dict, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from lxml import etree
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.auth0 import get_auth0_access_token

from app.core.config import settings
from app.db.base import Base
from app.db.commands import create_init_data
from app.db.session import async_engine, async_session
from app.main import create_app

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session", autouse=True)
def delete_test_db() -> None:
    # if test.db file exists,
    # delete it before running tests
    if path.exists("test.db"):
        try:
            remove("test.db")
        except Exception:
            pass


@pytest.fixture(scope="function")
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
    transport = ASGITransport(app=app)  # type: ignore
    async with LifespanManager(app):
        async with AsyncClient(
            transport=transport,
            base_url=f"http://0.0.0.0:8888{settings.api.prefix}/v1",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="session")
def mock_fetch_psi() -> Dict[str, Any]:
    mocked_response = {}
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/data/fetchpsi.json") as f:
        mocked_response = json.load(f)
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_ipinfo() -> Dict[str, Any]:
    mocked_response = {}
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/data/ipinfo-8.8.8.8.json") as f:
        mocked_response = json.load(f)
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_sitemap_index() -> str:
    mocked_response = ""
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/data/sitemap-index.xml") as f:
        mocked_response = f.read()
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_sitemap_page() -> str:
    mocked_response = ""
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/data/sitemap-page.xml") as f:
        mocked_response = f.read()
    return mocked_response


@pytest.fixture(scope="session")
def mock_invalid_sitemap_xml() -> etree._Element:
    mocked_response = ""
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/data/sitemap-invalid.xml") as f:
        mocked_response = f.read()
    return etree.fromstring(mocked_response.encode())


@pytest.fixture(scope="session")
def mock_valid_sitemap_urlset_xml() -> etree._Element:
    mocked_response = ""
    here = path.dirname(path.abspath(__file__))
    with open(f"{here}/data/sitemap-urlset.xml") as f:
        mocked_response = f.read()
    return etree.fromstring(mocked_response.encode())


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
