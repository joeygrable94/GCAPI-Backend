import asyncio
from typing import AsyncGenerator, Callable, Dict, Generator, Tuple

# import alembic
import pytest

# from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.config import settings
from app.db.schemas import UserRead
from app.db.init_db import build_database, create_init_data
from app.db.repositories import AccessTokensRepository, UsersRepository
from app.db.schemas.user import UserReadAdmin
from app.db.session import async_engine, async_session
from app.main import create_app
from app.security import (
    AuthManager,
    DatabaseStrategy,
    JWTStrategy,
    bearer_transport,
    get_user_auth,
)
from tests.utils.users import get_current_user_tokens, get_current_user

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session", autouse=True)
async def prestart_database():
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    settings.DEBUG_MODE = True
    await build_database()
    await create_init_data()


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
async def get_jwt_strategy() -> AsyncGenerator:
    yield JWTStrategy(secret=settings.SECRET_KEY)


@pytest.fixture(scope="session")
async def get_token_db(db_session: AsyncSession) -> AsyncGenerator:
    token_repo: AccessTokensRepository = AccessTokensRepository(db_session)
    yield token_repo


@pytest.fixture(scope="session")
async def get_db_strategy(
    get_token_db: AccessTokensRepository,
) -> AsyncGenerator:
    yield DatabaseStrategy(token_db=get_token_db)


@pytest.fixture(scope="session")
async def get_user_db(db_session: AsyncSession) -> AsyncGenerator:
    user_repo: UsersRepository = UsersRepository(db_session)
    yield user_repo


@pytest.fixture(scope="session")
async def user_auth(
    get_jwt_strategy: JWTStrategy,
    get_db_strategy: DatabaseStrategy,
    get_user_db: UsersRepository,
) -> AsyncGenerator:
    yield AuthManager(
        bearer=bearer_transport,
        jwt=get_jwt_strategy,
        tokens=get_db_strategy,
        user_db=get_user_db,
    )


@pytest.fixture(scope="session")
async def override_get_user_auth(
    get_jwt_strategy: JWTStrategy,
    get_db_strategy: DatabaseStrategy,
    get_user_db: UsersRepository,
) -> Callable:
    async def _override_get_user_auth() -> AsyncGenerator[AuthManager, None]:
        yield AuthManager(
            bearer=bearer_transport,
            jwt=get_jwt_strategy,
            tokens=get_db_strategy,
            user_db=get_user_db,
        )

    return _override_get_user_auth


@pytest.fixture(scope="module")
def app(
    override_get_db: Callable,
    override_get_user_auth: Callable,
) -> Generator:
    app: FastAPI = create_app()
    app.dependency_overrides[get_async_db] = override_get_db
    app.dependency_overrides[get_user_auth] = override_get_user_auth
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


@pytest.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    auth_data: Dict[str, str] = await get_current_user_tokens(
        client=client,
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )
    auth_token: str = auth_data["access_token"]
    auth_header: Dict[str, str] = {"Authorization": f"Bearer {auth_token}"}
    return auth_header


@pytest.fixture(scope="module")
async def testuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    auth_data: Dict[str, str] = await get_current_user_tokens(
        client=client,
        username=settings.TEST_NORMAL_USER,
        password=settings.TEST_NORMAL_USER_PASSWORD,
    )
    auth_token: str = auth_data["access_token"]
    auth_header: Dict[str, str] = {"Authorization": f"Bearer {auth_token}"}
    return auth_header


@pytest.fixture(scope="module")
async def current_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> Tuple[UserReadAdmin, Dict[str, str]]:
    current_user: UserReadAdmin
    token_header: Dict[str, str]
    current_user, token_header = await get_current_user(
        client=client,
        auth_header=superuser_token_headers,
    )
    return current_user, token_header


@pytest.fixture(scope="module")
async def current_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
) -> Tuple[UserRead, Dict[str, str]]:
    current_user: UserRead
    token_header: Dict[str, str]
    current_user, token_header = await get_current_user(
        client=client,
        auth_header=testuser_token_headers,
    )
    return current_user, token_header
