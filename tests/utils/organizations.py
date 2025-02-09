import json
from typing import List

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_organization.crud import OrganizationRepository
from app.entities.core_organization.model import Organization
from app.entities.core_organization.schemas import OrganizationCreate, OrganizationRead
from app.entities.core_user_organization.crud import UserOrganizationRepository
from app.entities.core_user_organization.model import UserOrganization
from app.entities.core_user_organization.schemas import UserOrganizationCreate
from app.entities.organization_platform.crud import OrganizationPlatformRepository
from app.entities.organization_platform.model import OrganizationPlatform
from app.entities.organization_platform.schemas import OrganizationPlatformCreate
from app.entities.organization_website.crud import OrganizationWebsiteRepository
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.organization_website.schemas import OrganizationWebsiteCreate
from tests.utils.utils import random_lower_string


async def create_random_organization(
    db_session: AsyncSession, is_active: bool = True
) -> OrganizationRead:
    repo: OrganizationRepository = OrganizationRepository(session=db_session)
    organization: Organization = await repo.create(
        schema=OrganizationCreate(
            slug=random_lower_string(8),
            title=random_lower_string(),
            description=random_lower_string(),
            is_active=is_active,
        )
    )
    return OrganizationRead.model_validate(organization)


async def assign_user_to_organization(
    db_session: AsyncSession, user_id: UUID4, organization_id: UUID4
) -> UserOrganization:
    repo: UserOrganizationRepository = UserOrganizationRepository(session=db_session)
    user_organization: UserOrganization = await repo.create(
        schema=UserOrganizationCreate(user_id=user_id, organization_id=organization_id)
    )
    return user_organization


async def assign_platform_to_organization(
    db_session: AsyncSession,
    platform_id: UUID4,
    organization_id: UUID4,
) -> OrganizationPlatform:
    repo: OrganizationPlatformRepository = OrganizationPlatformRepository(
        session=db_session
    )
    organization_platform: OrganizationPlatform = await repo.create(
        schema=OrganizationPlatformCreate(
            organization_id=organization_id, platform_id=platform_id
        )
    )
    return organization_platform


async def assign_website_to_organization(
    db_session: AsyncSession,
    website_id: UUID4,
    organization_id: UUID4,
) -> OrganizationWebsite:
    repo: OrganizationWebsiteRepository = OrganizationWebsiteRepository(
        session=db_session
    )
    organization_website: OrganizationWebsite = await repo.create(
        schema=OrganizationWebsiteCreate(
            website_id=website_id, organization_id=organization_id
        )
    )
    return organization_website


def create_random_organization_style_guide(
    colors: List[dict[str, str]] = [
        {
            "label": "Test Color",
            "className": "bg-red-8000",
            "textClass": "text-white",
        }
    ],
    fonts: List[dict[str, str]] = [
        {
            "type": "primary",
            "label": "Noto Sans",
            "className": "font-gc-primary",
            "src": "https://getcommunityinc.com/mycommunityapps/fonts/NotoSans/noto-sans.css",
            "srcvar": "https://getcommunityinc.com/mycommunityapps/fonts/NotoSans/noto-sans-variable.css",
        }
    ],
    voice_tone: List[str] = ["test tone"],
    voice_communication: List[str] = ["test communication"],
    voice_elements: List[str] = ["test elements"],
    voice_goals: List[str] = ["test goals"],
) -> str:
    return json.dumps(
        {
            "colors": colors,
            "fonts": fonts,
            "voice": {
                "tone": voice_tone,
                "communication": voice_communication,
                "elements": voice_elements,
                "goals": voice_goals,
            },
        }
    )
