import json
from collections.abc import AsyncGenerator
from os import path, remove
from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from lxml import etree
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.base import Base
from app.db.commands import create_init_data
from app.db.session import async_engine, async_session
from app.main import create_app
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.auth0 import get_auth0_access_token


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def delete_test_db() -> None:
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


@pytest.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    _app: FastAPI = create_app()
    yield _app


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=transport,
            base_url=f"http://0.0.0.0:8888{settings.api.prefix}/v1",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="session")
def admin_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_admin, settings.auth.first_admin_password
        ),
        email=settings.auth.first_admin,
    )


@pytest.fixture(scope="session")
def manager_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_manager, settings.auth.first_manager_password
        ),
        email=settings.auth.first_manager,
    )


@pytest.fixture(scope="session")
def employee_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_employee, settings.auth.first_employee_password
        ),
        email=settings.auth.first_employee,
    )


@pytest.fixture(scope="session")
def client_a_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_client_a, settings.auth.first_client_a_password
        ),
        email=settings.auth.first_client_a,
    )


@pytest.fixture(scope="session")
def client_b_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_client_b, settings.auth.first_client_b_password
        ),
        email=settings.auth.first_client_b,
    )


@pytest.fixture(scope="session")
def verified_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_user_verified,
            settings.auth.first_user_verified_password,
        ),
        email=settings.auth.first_user_verified,
    )


@pytest.fixture(scope="session")
def unverified_user() -> ClientAuthorizedUser:
    return ClientAuthorizedUser(
        token_headers=get_auth0_access_token(
            settings.auth.first_user_unverified,
            settings.auth.first_user_unverified_password,
        ),
        email=settings.auth.first_user_unverified,
    )


# Mock Data


@pytest.fixture(scope="session")
def mock_fetch_ipinfo() -> dict[str, Any]:
    mocked_response = {}
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "ipinfo-8.8.8.8.json")
    with open(file_path) as f:
        mocked_response = json.load(f)
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_psi() -> dict[str, Any]:
    mocked_response = {}
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "fetchpsi.json")
    with open(file_path) as f:
        mocked_response = json.load(f)
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_sitemap_index() -> str:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-index.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    return mocked_response


@pytest.fixture(scope="session")
def mock_fetch_sitemap_page() -> str:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-page.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    return mocked_response


@pytest.fixture(scope="session")
def mock_invalid_sitemap_xml() -> etree._Element:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-invalid.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    return etree.fromstring(mocked_response.encode())


@pytest.fixture(scope="session")
def mock_valid_sitemap_urlset_xml() -> etree._Element:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-urlset.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    return etree.fromstring(mocked_response.encode())
