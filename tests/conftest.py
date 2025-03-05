import json
from collections.abc import AsyncGenerator
from os import environ, path
from typing import Any, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from lxml import etree
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.base import Base
from app.db.session import async_session, engine
from app.main import create_app
from app.services.clerk.settings import clerk_settings
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.users import create_core_user


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# @pytest.fixture(scope="session", autouse=True)
# async def init_db_session() -> AsyncGenerator[None, None]:
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    Base.metadata.create_all(bind=engine)

    # await create_init_data()

    session: AsyncSession
    async with async_session() as session:
        yield session
        await session.flush()
        await session.rollback()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    _app: FastAPI = create_app()
    yield _app


@pytest.fixture(scope="module")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=transport,
            base_url=f"http://0.0.0.0:8888{settings.api.prefix}/v1",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="module")
async def admin_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_ADMIN_TEST_TOKEN", None)
    if token is None:
        raise ValueError("admin test token is not set")
    await create_core_user(db_session, "admin")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_admin,
        auth_id=clerk_settings.first_admin_auth_id,
    )


@pytest.fixture(scope="module")
async def manager_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_MANAGER_TEST_TOKEN", None)
    if token is None:
        raise ValueError("manager test token is not set")
    await create_core_user(db_session, "manager")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_manager,
        auth_id=clerk_settings.first_manager_auth_id,
    )


@pytest.fixture(scope="module")
async def employee_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_EMPLOYEE_TEST_TOKEN", None)
    if token is None:
        raise ValueError("employee test token is not set")
    await create_core_user(db_session, "employee")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_employee,
        auth_id=clerk_settings.first_employee_auth_id,
    )


@pytest.fixture(scope="module")
async def client_a_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_CLIENT_A_TEST_TOKEN", None)
    if token is None:
        raise ValueError("client_a test token is not set")
    await create_core_user(db_session, "client_a")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_client_a,
        auth_id=clerk_settings.first_client_a_auth_id,
    )


@pytest.fixture(scope="module")
async def client_b_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_CLIENT_B_TEST_TOKEN", None)
    if token is None:
        raise ValueError("client_b test token is not set")
    await create_core_user(db_session, "client_b")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_client_b,
        auth_id=clerk_settings.first_client_b_auth_id,
    )


@pytest.fixture(scope="module")
async def verified_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_USER_VERIFIED_TEST_TOKEN", None)
    if token is None:
        raise ValueError("user_verified test token is not set")
    await create_core_user(db_session, "verified")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_user_verified,
        auth_id=clerk_settings.first_user_verified_auth_id,
    )


@pytest.fixture(scope="module")
async def unverified_user(
    db_session: AsyncSession,
) -> AsyncGenerator[ClientAuthorizedUser, None]:
    token = environ.get("CLERK_FIRST_USER_UNVERIFIED_TEST_TOKEN", None)
    if token is None:
        raise ValueError("user_unverified test token is not set")
    await create_core_user(db_session, "unverified")
    yield ClientAuthorizedUser(
        token_headers={"Authorization": f"Bearer {token}"},
        email=clerk_settings.first_user_unverified,
        auth_id=clerk_settings.first_user_unverified_auth_id,
    )


# Mock Data


@pytest.fixture(scope="module")
def mock_fetch_ipinfo() -> Generator[dict[str, Any], None, None]:
    mocked_response = {}
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "ipinfo-8.8.8.8.json")
    with open(file_path) as f:
        mocked_response = json.load(f)
    yield mocked_response


@pytest.fixture(scope="module")
def mock_fetch_psi() -> Generator[dict[str, Any], None, None]:
    mocked_response = {}
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "fetchpsi.json")
    with open(file_path) as f:
        mocked_response = json.load(f)
    yield mocked_response


@pytest.fixture(scope="module")
def mock_fetch_sitemap_index() -> Generator[str, None, None]:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-index.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    yield mocked_response


@pytest.fixture(scope="module")
def mock_fetch_sitemap_page() -> Generator[str, None, None]:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-page.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    yield mocked_response


@pytest.fixture(scope="module")
def mock_invalid_sitemap_xml() -> Generator[etree._Element, None, None]:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-invalid.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    yield etree.fromstring(mocked_response.encode())


@pytest.fixture(scope="module")
def mock_valid_sitemap_urlset_xml() -> Generator[etree._Element, None, None]:
    mocked_response = ""
    path_to_tests_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(path_to_tests_dir, "data", "sitemap-urlset.xml")
    with open(file_path) as f:
        mocked_response = f.read()
    yield etree.fromstring(mocked_response.encode())
