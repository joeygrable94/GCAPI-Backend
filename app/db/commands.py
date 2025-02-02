import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.logger import logger
from app.db.base import Base
from app.db.constants import DB_STR_USER_PICTURE_DEFAULT, MASTER_PLATFORM_INDEX
from app.db.session import async_session, engine
from app.entities.client.crud import ClientRepository
from app.entities.client.model import Client
from app.entities.client.schemas import ClientCreate
from app.entities.client_platform.crud import ClientPlatformRepository
from app.entities.client_platform.schemas import ClientPlatformCreate
from app.entities.platform.crud import PlatformRepository
from app.entities.platform.model import Platform
from app.entities.platform.schemas import PlatformCreate
from app.entities.user.crud import UserRepository
from app.entities.user.model import User
from app.entities.user.schemas import UserCreate
from app.entities.user_client.crud import UserClientRepository
from app.entities.user_client.model import UserClient
from app.entities.user_client.schemas import UserClientCreate
from app.services.auth0 import auth_settings
from app.services.permission import AclPrivilege

max_tries = 60 * 5  # 5 minutes
wait_seconds = 3


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def check_db_connected() -> None:  # pragma: no cover
    try:
        logger.info("ATTEMPTING TO CONNECT TO DATABASE...")
        stmt: Any = text("select 1")
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
        stmt: Any = text("select 1")
        with engine.connect() as connection:
            result: Any = connection.execute(stmt)
            if result is not None:
                logger.info("+ ASYCN F(X) --> Disconnecting MYSQL...")
        logger.info("+ ASYNC F(X) --> Database Disconnected. (-_-) Zzz")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> Failed to Disconnect Database! (@_@)")
        raise e


async def create_db_tables() -> None:  # pragma: no cover
    logger.info("Creating Database Tables")
    with engine.begin() as conn:
        Base.metadata.create_all(conn, checkfirst=True)
    logger.info("Database Tables Created")


async def drop_db_tables() -> None:  # pragma: no cover
    logger.info("Dropping Database Tables")
    with engine.begin() as conn:
        Base.metadata.drop_all(conn, checkfirst=True)
    logger.info("Database Tables Dropped")


async def create_init_data() -> int:  # pragma: no cover
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
    p_ga4: Platform | None
    p_gads: Platform | None
    p_spsp: Platform | None
    p_bdx: Platform | None
    user_repo: UserRepository
    client_repo: ClientRepository
    user_client_repo: UserClientRepository
    platform_repo: PlatformRepository
    client_platform_repo: ClientPlatformRepository

    # first admin
    async with async_session() as session:
        user_repo = UserRepository(session)
        admin1 = await user_repo.read_by("auth_id", auth_settings.first_admin_auth_id)
        if not admin1:
            admin1 = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_admin,
                    email=auth_settings.first_admin,
                    auth_id=auth_settings.first_admin_auth_id,
                    picture=auth_settings.first_admin_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=True,
                    scopes=[
                        AclPrivilege("role:user"),
                        AclPrivilege("role:admin"),
                        AclPrivilege("access:test"),
                    ],
                )
            )
            i_count += 1

    # first manager
    async with async_session() as session:
        user_repo = UserRepository(session)
        manager1 = await user_repo.read_by(
            "auth_id", auth_settings.first_manager_auth_id
        )
        if not manager1:
            manager1 = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_manager,
                    email=auth_settings.first_manager,
                    auth_id=auth_settings.first_manager_auth_id,
                    picture=auth_settings.first_manager_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[
                        AclPrivilege("role:user"),
                        AclPrivilege("role:manager"),
                        AclPrivilege("access:test"),
                    ],
                )
            )
            i_count += 1

    # first employee
    async with async_session() as session:
        user_repo = UserRepository(session)
        employee1 = await user_repo.read_by(
            "auth_id", auth_settings.first_employee_auth_id
        )
        if not employee1:
            employee1 = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_employee,
                    email=auth_settings.first_employee,
                    auth_id=auth_settings.first_employee_auth_id,
                    picture=auth_settings.first_employee_picture,
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
            "auth_id", auth_settings.first_client_a_auth_id
        )
        if not client_a:
            client_a = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_client_a,
                    email=auth_settings.first_client_a,
                    auth_id=auth_settings.first_client_a_auth_id,
                    picture=auth_settings.first_client_a_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[AclPrivilege("role:user"), AclPrivilege("role:client")],
                )
            )
            i_count += 1

        client_b = await user_repo.read_by(
            "auth_id", auth_settings.first_client_b_auth_id
        )
        if not client_b:
            client_b = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_client_b,
                    email=auth_settings.first_client_b,
                    auth_id=auth_settings.first_client_b_auth_id,
                    picture=auth_settings.first_client_b_picture,
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
            "auth_id", auth_settings.first_user_verified_auth_id
        )
        if not user_verified:
            user_verified = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_user_verified,
                    email=auth_settings.first_user_verified,
                    auth_id=auth_settings.first_user_verified_auth_id,
                    picture=DB_STR_USER_PICTURE_DEFAULT,
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
            "auth_id", auth_settings.first_user_unverified_auth_id
        )
        if not user_unverified:
            user_unverified = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_user_unverified,
                    email=auth_settings.first_user_unverified,
                    auth_id=auth_settings.first_user_unverified_auth_id,
                    picture=DB_STR_USER_PICTURE_DEFAULT,
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
            c1 = await client_repo.create(
                ClientCreate(slug="gcinc", title="Get Community, Inc.")
            )
            i_count += 1

        c2 = await client_repo.read_by("title", "The Grables")
        if not c2:
            c2 = await client_repo.create(
                ClientCreate(slug="grable", title="The Grables")
            )
            i_count += 1

    # assign users to client1: admin1
    async with async_session() as session:
        user_client_repo = UserClientRepository(session)
        c1_admin1 = await user_client_repo.exists_by_fields(
            {"user_id": admin1.id, "client_id": c1.id}
        )
        if not c1_admin1:
            await user_client_repo.create(
                UserClientCreate(user_id=admin1.id, client_id=c1.id)
            )
            i_count += 1

        # assign users to client1: manager1
        c1_manager1 = await user_client_repo.exists_by_fields(
            {"user_id": manager1.id, "client_id": c1.id}
        )
        if not c1_manager1:
            await user_client_repo.create(
                UserClientCreate(user_id=manager1.id, client_id=c1.id)
            )
            i_count += 1

        # assign users to client1: employee1
        c1_employee1 = await user_client_repo.exists_by_fields(
            {"user_id": employee1.id, "client_id": c1.id}
        )
        if not c1_employee1:
            await user_client_repo.create(
                UserClientCreate(user_id=employee1.id, client_id=c1.id)
            )
            i_count += 1

        # assign users to client2: admin1
        c1_admin1 = await user_client_repo.exists_by_fields(
            {"user_id": admin1.id, "client_id": c2.id}
        )
        if not c1_admin1:
            await user_client_repo.create(
                UserClientCreate(user_id=admin1.id, client_id=c2.id)
            )
            i_count += 1

        # assign users to client2: manager1
        c1_manager1 = await user_client_repo.exists_by_fields(
            {"user_id": manager1.id, "client_id": c2.id}
        )
        if not c1_manager1:
            await user_client_repo.create(
                UserClientCreate(user_id=manager1.id, client_id=c2.id)
            )
            i_count += 1

    for slug, title in MASTER_PLATFORM_INDEX.items():
        async with async_session() as session:
            platform_repo = PlatformRepository(session)
            p1 = await platform_repo.exists_by_fields({"slug": slug, "title": title})
            if not p1:
                p1 = await platform_repo.create(PlatformCreate(slug=slug, title=title))
                i_count += 1

    # assign platforms to clients
    async with async_session() as session:
        platform_repo = PlatformRepository(session)
        p_ga4 = await platform_repo.read_by(field_name="slug", field_value="ga4")
        assert p_ga4
        p_gads = await platform_repo.read_by(field_name="slug", field_value="gads")
        assert p_gads
        p_spsp = await platform_repo.read_by(field_name="slug", field_value="spsp")
        assert p_spsp
        p_bdx = await platform_repo.read_by(field_name="slug", field_value="bdx")
        assert p_bdx
        client_platform_repo = ClientPlatformRepository(session)
        c1_p_ga4 = await client_platform_repo.exists_by_fields(
            {"client_id": c1.id, "platform_id": p_ga4.id}
        )
        if not c1_p_ga4:
            await client_platform_repo.create(
                ClientPlatformCreate(client_id=c1.id, platform_id=p_ga4.id)
            )
            i_count += 1
        c1_p_gads = await client_platform_repo.exists_by_fields(
            {"client_id": c1.id, "platform_id": p_gads.id}
        )
        if not c1_p_gads:
            await client_platform_repo.create(
                ClientPlatformCreate(client_id=c1.id, platform_id=p_gads.id)
            )
            i_count += 1
        c1_p_spsp = await client_platform_repo.exists_by_fields(
            {"client_id": c1.id, "platform_id": p_spsp.id}
        )
        if not c1_p_spsp:
            await client_platform_repo.create(
                ClientPlatformCreate(client_id=c1.id, platform_id=p_spsp.id)
            )
            i_count += 1
        c2_p_ga4 = await client_platform_repo.exists_by_fields(
            {"client_id": c2.id, "platform_id": p_ga4.id}
        )
        if not c2_p_ga4:
            await client_platform_repo.create(
                ClientPlatformCreate(client_id=c2.id, platform_id=p_ga4.id)
            )
            i_count += 1

    return i_count


async def build_database() -> None:  # pragma: no cover
    try:
        logger.info("Building Database")
        await drop_db_tables()
        await create_db_tables()
        logger.info("Database Ready")
    except Exception as e:
        logger.warning("Database threw an error", e)
