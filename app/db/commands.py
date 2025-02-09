import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.logger import logger
from app.db.base import Base
from app.db.constants import DB_STR_USER_PICTURE_DEFAULT, MASTER_PLATFORM_INDEX
from app.db.session import async_session, engine
from app.entities.core_organization.crud import OrganizationRepository
from app.entities.core_organization.model import Organization
from app.entities.core_organization.schemas import OrganizationCreate
from app.entities.core_user.crud import UserRepository
from app.entities.core_user.model import User
from app.entities.core_user.schemas import UserCreate
from app.entities.core_user_organization.crud import UserOrganizationRepository
from app.entities.core_user_organization.model import UserOrganization
from app.entities.core_user_organization.schemas import UserOrganizationCreate
from app.entities.organization_platform.crud import OrganizationPlatformRepository
from app.entities.organization_platform.schemas import OrganizationPlatformCreate
from app.entities.platform.crud import PlatformRepository
from app.entities.platform.model import Platform
from app.entities.platform.schemas import PlatformCreate
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
    organization_a: User | None
    organization_b: User | None
    user_verified: User | None
    user_unverified: User | None
    c1: Organization | None
    c2: Organization | None
    c1_admin1: UserOrganization | None
    c1_manager1: UserOrganization | None
    c1_employee1: UserOrganization | None
    p_ga4: Platform | None
    p_gads: Platform | None
    p_spsp: Platform | None
    p_bdx: Platform | None
    user_repo: UserRepository
    organization_repo: OrganizationRepository
    user_organization_repo: UserOrganizationRepository
    platform_repo: PlatformRepository
    organization_platform_repo: OrganizationPlatformRepository

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

    # first users that is a business organization
    async with async_session() as session:
        user_repo = UserRepository(session)
        organization_a = await user_repo.read_by(
            "auth_id", auth_settings.first_client_a_auth_id
        )
        if not organization_a:
            organization_a = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_client_a,
                    email=auth_settings.first_client_a,
                    auth_id=auth_settings.first_client_a_auth_id,
                    picture=auth_settings.first_client_a_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[
                        AclPrivilege("role:user"),
                        AclPrivilege("role:organization"),
                    ],
                )
            )
            i_count += 1

        organization_b = await user_repo.read_by(
            "auth_id", auth_settings.first_client_b_auth_id
        )
        if not organization_b:
            organization_b = await user_repo.create(
                UserCreate(
                    username=auth_settings.first_client_b,
                    email=auth_settings.first_client_b,
                    auth_id=auth_settings.first_client_b_auth_id,
                    picture=auth_settings.first_client_b_picture,
                    is_active=True,
                    is_verified=True,
                    is_superuser=False,
                    scopes=[
                        AclPrivilege("role:user"),
                        AclPrivilege("role:organization"),
                    ],
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

    # first organizations
    async with async_session() as session:
        organization_repo = OrganizationRepository(session)
        c1 = await organization_repo.read_by("title", "Get Community, Inc.")
        if not c1:
            c1 = await organization_repo.create(
                OrganizationCreate(slug="gcinc", title="Get Community, Inc.")
            )
            i_count += 1

        c2 = await organization_repo.read_by("title", "The Grables")
        if not c2:
            c2 = await organization_repo.create(
                OrganizationCreate(slug="grable", title="The Grables")
            )
            i_count += 1

    # assign users to organization1: admin1
    async with async_session() as session:
        user_organization_repo = UserOrganizationRepository(session)
        c1_admin1 = await user_organization_repo.exists_by_fields(
            {"user_id": admin1.id, "organization_id": c1.id}
        )
        if not c1_admin1:
            await user_organization_repo.create(
                UserOrganizationCreate(user_id=admin1.id, organization_id=c1.id)
            )
            i_count += 1

        # assign users to organization1: manager1
        c1_manager1 = await user_organization_repo.exists_by_fields(
            {"user_id": manager1.id, "organization_id": c1.id}
        )
        if not c1_manager1:
            await user_organization_repo.create(
                UserOrganizationCreate(user_id=manager1.id, organization_id=c1.id)
            )
            i_count += 1

        # assign users to organization1: employee1
        c1_employee1 = await user_organization_repo.exists_by_fields(
            {"user_id": employee1.id, "organization_id": c1.id}
        )
        if not c1_employee1:
            await user_organization_repo.create(
                UserOrganizationCreate(user_id=employee1.id, organization_id=c1.id)
            )
            i_count += 1

        # assign users to organization2: admin1
        c1_admin1 = await user_organization_repo.exists_by_fields(
            {"user_id": admin1.id, "organization_id": c2.id}
        )
        if not c1_admin1:
            await user_organization_repo.create(
                UserOrganizationCreate(user_id=admin1.id, organization_id=c2.id)
            )
            i_count += 1

        # assign users to organization2: manager1
        c1_manager1 = await user_organization_repo.exists_by_fields(
            {"user_id": manager1.id, "organization_id": c2.id}
        )
        if not c1_manager1:
            await user_organization_repo.create(
                UserOrganizationCreate(user_id=manager1.id, organization_id=c2.id)
            )
            i_count += 1

    for slug, title in MASTER_PLATFORM_INDEX.items():
        async with async_session() as session:
            platform_repo = PlatformRepository(session)
            p1 = await platform_repo.exists_by_fields({"slug": slug, "title": title})
            if not p1:
                p1 = await platform_repo.create(PlatformCreate(slug=slug, title=title))
                i_count += 1

    # assign platforms to organizations
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
        organization_platform_repo = OrganizationPlatformRepository(session)
        c1_p_ga4 = await organization_platform_repo.exists_by_fields(
            {"organization_id": c1.id, "platform_id": p_ga4.id}
        )
        if not c1_p_ga4:
            await organization_platform_repo.create(
                OrganizationPlatformCreate(organization_id=c1.id, platform_id=p_ga4.id)
            )
            i_count += 1
        c1_p_gads = await organization_platform_repo.exists_by_fields(
            {"organization_id": c1.id, "platform_id": p_gads.id}
        )
        if not c1_p_gads:
            await organization_platform_repo.create(
                OrganizationPlatformCreate(organization_id=c1.id, platform_id=p_gads.id)
            )
            i_count += 1
        c1_p_spsp = await organization_platform_repo.exists_by_fields(
            {"organization_id": c1.id, "platform_id": p_spsp.id}
        )
        if not c1_p_spsp:
            await organization_platform_repo.create(
                OrganizationPlatformCreate(organization_id=c1.id, platform_id=p_spsp.id)
            )
            i_count += 1
        c2_p_ga4 = await organization_platform_repo.exists_by_fields(
            {"organization_id": c2.id, "platform_id": p_ga4.id}
        )
        if not c2_p_ga4:
            await organization_platform_repo.create(
                OrganizationPlatformCreate(organization_id=c2.id, platform_id=p_ga4.id)
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
