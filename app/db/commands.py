import logging
from typing import Any  # pragma: no cover

from sqlalchemy import text  # pragma: no cover
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.core.logger import logger
from app.core.security.permissions import AclPrivilege
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
        print(dburl)
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
    i_count = 0
    session: AsyncSession
    admin1: User | None
    manager1: User | None
    employee1: User | None
    client_a: User | None
    client_b: User | None
    user_verified: User | None
    user_unverified: User | None
    c1: Client | None
    c2: Client | None
    c1_admin1: UserClient | None
    c1_manager1: UserClient | None
    c1_employee1: UserClient | None
    user_repo: UserRepository
    client_repo: ClientRepository
    user_client_repo: UserClientRepository

    # first admin
    async with async_session() as session:
        user_repo = UserRepository(session)
        admin1 = await user_repo.read_by("auth_id", settings.auth.first_admin_auth_id)
        if not admin1:
            admin1 = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_admin,
                    email=settings.auth.first_admin,
                    auth_id=settings.auth.first_admin_auth_id,
                    picture=settings.auth.first_admin_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=True,
                    scopes=[AclPrivilege("role:user"), AclPrivilege("role:admin")],
                )
            )
            i_count += 1

    # first manager
    async with async_session() as session:
        user_repo = UserRepository(session)
        manager1 = await user_repo.read_by(
            "auth_id", settings.auth.first_manager_auth_id
        )
        if not manager1:
            manager1 = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_manager,
                    email=settings.auth.first_manager,
                    auth_id=settings.auth.first_manager_auth_id,
                    picture=settings.auth.first_manager_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user"), AclPrivilege("role:manager")],
                )
            )
            i_count += 1

    # first employee
    async with async_session() as session:
        user_repo = UserRepository(session)
        employee1 = await user_repo.read_by(
            "auth_id", settings.auth.first_employee_auth_id
        )
        if not employee1:
            employee1 = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_employee,
                    email=settings.auth.first_employee,
                    auth_id=settings.auth.first_employee_auth_id,
                    picture=settings.auth.first_employee_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user"), AclPrivilege("role:employee")],
                )
            )
            i_count += 1

    # first users that is a business client
    async with async_session() as session:
        user_repo = UserRepository(session)
        client_a = await user_repo.read_by(
            "auth_id", settings.auth.first_client_a_auth_id
        )
        if not client_a:
            client_a = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_client_a,
                    email=settings.auth.first_client_a,
                    auth_id=settings.auth.first_client_a_auth_id,
                    picture=settings.auth.first_client_a_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user"), AclPrivilege("role:client")],
                )
            )
            i_count += 1

        client_b = await user_repo.read_by(
            "auth_id", settings.auth.first_client_b_auth_id
        )
        if not client_b:
            client_b = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_client_b,
                    email=settings.auth.first_client_b,
                    auth_id=settings.auth.first_client_b_auth_id,
                    picture=settings.auth.first_client_b_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user"), AclPrivilege("role:client")],
                )
            )
            i_count += 1

    # first user verified
    async with async_session() as session:
        user_repo = UserRepository(session)
        user_verified = await user_repo.read_by(
            "auth_id", settings.auth.first_user_verified_auth_id
        )
        if not user_verified:
            user_verified = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_user_verified,
                    email=settings.auth.first_user_verified,
                    auth_id=settings.auth.first_user_verified_auth_id,
                    picture="https://www.gravatar.com/avatar/?d=identicon",
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user")],
                )
            )
            i_count += 1

    # first user unverified
    async with async_session() as session:
        user_repo = UserRepository(session)
        user_unverified = await user_repo.read_by(
            "auth_id", settings.auth.first_user_unverified_auth_id
        )
        if not user_unverified:
            user_unverified = await user_repo.create(
                UserCreate(
                    username=settings.auth.first_user_unverified,
                    email=settings.auth.first_user_unverified,
                    auth_id=settings.auth.first_user_unverified_auth_id,
                    picture="https://www.gravatar.com/avatar/?d=identicon",
                    is_active=True,
                    is_verified=False,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user")],
                )
            )
            i_count += 1

    # first clients
    async with async_session() as session:
        client_repo = ClientRepository(session)
        c1 = await client_repo.read_by("title", "Get Community, Inc.")
        if not c1:
            c1 = await client_repo.create(ClientCreate(title="Get Community, Inc."))
            i_count += 1

        c2 = await client_repo.read_by("title", "The Grables")
        if not c2:
            c2 = await client_repo.create(ClientCreate(title="The Grables"))
            i_count += 1

    # assign users to client1: admin1
    async with async_session() as session:
        user_client_repo = UserClientRepository(session)
        c1_admin1 = await user_client_repo.exists_by_two(
            "user_id", admin1.id, "client_id", c1.id
        )
        if not c1_admin1:
            await user_client_repo.create(
                UserClientCreate(user_id=admin1.id, client_id=c1.id)
            )
            i_count += 1

    # assign users to client1: manager1
    async with async_session() as session:
        user_client_repo = UserClientRepository(session)
        c1_manager1 = await user_client_repo.exists_by_two(
            "user_id", manager1.id, "client_id", c1.id
        )
        if not c1_manager1:
            await user_client_repo.create(
                UserClientCreate(user_id=manager1.id, client_id=c1.id)
            )
            i_count += 1

    # assign users to client1: employee1
    async with async_session() as session:
        user_client_repo = UserClientRepository(session)
        c1_employee1 = await user_client_repo.exists_by_two(
            "user_id", employee1.id, "client_id", c1.id
        )
        if not c1_employee1:
            await user_client_repo.create(
                UserClientCreate(user_id=employee1.id, client_id=c1.id)
            )
            i_count += 1

    # assign users to client2: admin1
    async with async_session() as session:
        user_client_repo = UserClientRepository(session)
        c1_admin1 = await user_client_repo.exists_by_two(
            "user_id", admin1.id, "client_id", c2.id
        )
        if not c1_admin1:
            await user_client_repo.create(
                UserClientCreate(user_id=admin1.id, client_id=c2.id)
            )
            i_count += 1

    # assign users to client2: manager1
    async with async_session() as session:
        user_client_repo = UserClientRepository(session)
        c1_manager1 = await user_client_repo.exists_by_two(
            "user_id", manager1.id, "client_id", c2.id
        )
        if not c1_manager1:
            await user_client_repo.create(
                UserClientCreate(user_id=manager1.id, client_id=c2.id)
            )
            i_count += 1
    logger.info(f"Data Inserted C[{i_count}]")


async def build_database() -> None:  # pragma: no cover
    try:
        logger.info("Building Database")
        await drop_db_tables()
        await create_db_tables()
        logger.info("Database Ready")
    except Exception as e:
        logger.warning("Database threw an error", e)
