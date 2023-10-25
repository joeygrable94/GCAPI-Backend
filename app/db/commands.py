import logging
from typing import Any  # pragma: no cover

from sqlalchemy import text  # pragma: no cover
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.core.logger import logger
from app.core.security import Scope
from app.crud import ClientRepository, UserClientRepository, UserRepository
from app.db.base import Base
from app.db.session import async_engine, async_session, engine
from app.models import Client, User, UserClient
from app.schemas import ClientCreate, UserClientCreate, UserCreate

max_tries = 60 * 5  # 5 minutes
wait_seconds = 3


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),  # type: ignore
    after=after_log(logger, logging.WARN),  # type: ignore
)
async def check_db_connected() -> None:  # pragma: no cover
    try:
        dburl: str = str(settings.db.uri_async)
        stmt: Any = text("select 1")
        if not dburl.__contains__("sqlite"):
            with engine.connect() as connection:
                result: Any = connection.execute(stmt)
                if result is not None:
                    logger.info("+ ASYCN F(X) --> MYSQL CONNECTED!")
        logger.info("Database is ready for connections. (^_^)")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> There was a problem connecting to DB...")
        raise e


async def check_db_disconnected() -> None:  # pragma: no cover
    try:
        dburl: str = str(settings.db.uri_async)
        stmt: Any = text("select 1")
        if not dburl.__contains__("sqlite"):
            with engine.connect() as connection:
                result: Any = connection.execute(stmt)
                if result is not None:
                    logger.info("+ ASYCN F(X) --> Disconnecting MYSQL...")
            logger.info("+ ASYNC F(X) --> MYSQL DISCONNECTED!")
        logger.info("+ ASYNC F(X) --> Database Disconnected. (-_-) Zzz")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> Failed to Disconnect Database! (@_@)")
        raise e


async def create_db_tables() -> None:  # pragma: no cover
    logger.info("Creating Database Tables")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database Tables Created")


async def drop_db_tables() -> None:  # pragma: no cover
    logger.info("Dropping Database Tables")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database Tables Dropped")


async def create_init_data() -> None:  # pragma: no cover
    logger.info("Inserting Initial Data")
    session: AsyncSession
    async with async_session() as session:
        user_repo = UserRepository(session)
        client_repo = ClientRepository(session)
        user_client_repo = UserClientRepository(session)

        # first users
        admin1: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_admin_auth_id
        )
        if not admin1:
            admin1 = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_admin,
                    email=settings.auth.first_admin,
                    auth_id=settings.auth.first_admin_auth_id,
                    is_active=True,
                    is_verified=True,
                    is_superuser=True,
                    scopes=[Scope("role:user"), Scope("role:admin")],
                )
            )  # noqa: E501
        manager1: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_manager_auth_id
        )
        if not manager1:
            manager1 = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_manager,
                    email=settings.auth.first_manager,
                    auth_id=settings.auth.first_manager_auth_id,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[Scope("role:user"), Scope("role:manager")],
                )
            )  # noqa: E501
        employee1: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_employee_auth_id
        )
        if not employee1:
            employee1 = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_employee,
                    email=settings.auth.first_employee,
                    auth_id=settings.auth.first_employee_auth_id,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[Scope("role:user"), Scope("role:employee")],
                )
            )  # noqa: E501
        client_a: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_client_a_auth_id
        )
        if not client_a:
            client_a = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_client_a,
                    email=settings.auth.first_client_a,
                    auth_id=settings.auth.first_client_a_auth_id,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[Scope("role:user"), Scope("role:client")],
                )
            )  # noqa: E501
        client_b: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_client_b_auth_id
        )
        if not client_b:
            client_b = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_client_b,
                    email=settings.auth.first_client_b,
                    auth_id=settings.auth.first_client_b_auth_id,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[Scope("role:user"), Scope("role:client")],
                )
            )  # noqa: E501
        user_verified: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_user_verified_auth_id
        )
        if not user_verified:
            user_verified = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_user_verified,
                    email=settings.auth.first_user_verified,
                    auth_id=settings.auth.first_user_verified_auth_id,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[Scope("role:user")],
                )
            )  # noqa: E501
        user_unverified: User | None = await user_repo.read_by(
            "auth_id", settings.auth.first_user_unverified_auth_id
        )
        if not user_unverified:
            user_unverified = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_user_unverified,
                    email=settings.auth.first_user_unverified,
                    auth_id=settings.auth.first_user_unverified_auth_id,
                    is_active=True,
                    is_verified=False,
                    is_superuser=False,
                    scopes=[Scope("role:user")],
                )
            )  # noqa: E501

        # first clients
        c1: Client | None = await client_repo.read_by("title", "Get Community, Inc.")
        if not c1:
            c1 = await client_repo.create(ClientCreate(title="Get Community, Inc."))

        c2: Client | None = await client_repo.read_by("title", "The Grables")
        if not c2:
            c2 = await client_repo.create(ClientCreate(title="The Grables"))

        # assign admin and manager to client 1
        c1_admin1: UserClient | None = await user_client_repo.exists_by_two(
            "user_id", admin1.id, "client_id", c1.id
        )
        if not c1_admin1:
            await user_client_repo.create(
                UserClientCreate(user_id=admin1.id, client_id=c1.id)
            )
        c1_manager1: UserClient | None = await user_client_repo.exists_by_two(
            "user_id", manager1.id, "client_id", c1.id
        )
        if not c1_manager1:
            await user_client_repo.create(
                UserClientCreate(user_id=manager1.id, client_id=c1.id)
            )

        # assign admin and manager to client 2
        c1_admin1: UserClient | None = await user_client_repo.exists_by_two(
            "user_id", admin1.id, "client_id", c2.id
        )
        if not c1_admin1:
            await user_client_repo.create(
                UserClientCreate(user_id=admin1.id, client_id=c2.id)
            )
        c1_manager1: UserClient | None = await user_client_repo.exists_by_two(
            "user_id", manager1.id, "client_id", c2.id
        )
        if not c1_manager1:
            await user_client_repo.create(
                UserClientCreate(user_id=manager1.id, client_id=c2.id)
            )

    logger.info("Data Inserted")


async def build_database() -> None:  # pragma: no cover
    logger.info("Building Database")
    await drop_db_tables()
    await create_db_tables()
    logger.info("Database Ready")
