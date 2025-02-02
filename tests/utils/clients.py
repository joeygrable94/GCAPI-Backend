import json
from typing import List

from httpx import Client
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.client.crud import ClientRepository
from app.entities.client.schemas import ClientCreate, ClientRead
from app.entities.client_platform.crud import ClientPlatformRepository
from app.entities.client_platform.model import ClientPlatform
from app.entities.client_platform.schemas import ClientPlatformCreate
from app.entities.client_website.crud import ClientWebsiteRepository
from app.entities.client_website.model import ClientWebsite
from app.entities.client_website.schemas import ClientWebsiteCreate
from app.entities.user_client.crud import UserClientRepository
from app.entities.user_client.model import UserClient
from app.entities.user_client.schemas import UserClientCreate
from tests.utils.utils import random_lower_string


async def create_random_client(
    db_session: AsyncSession, is_active: bool = True
) -> ClientRead:
    repo: ClientRepository = ClientRepository(session=db_session)
    client: Client = await repo.create(
        schema=ClientCreate(
            slug=random_lower_string(8),
            title=random_lower_string(),
            description=random_lower_string(),
            is_active=is_active,
        )
    )
    return ClientRead.model_validate(client)


async def assign_user_to_client(
    db_session: AsyncSession, user_id: UUID4, client_id: UUID4
) -> UserClient:
    repo: UserClientRepository = UserClientRepository(session=db_session)
    user_client: UserClient = await repo.create(
        schema=UserClientCreate(user_id=user_id, client_id=client_id)
    )
    return user_client


async def assign_platform_to_client(
    db_session: AsyncSession,
    platform_id: UUID4,
    client_id: UUID4,
) -> ClientPlatform:
    repo: ClientPlatformRepository = ClientPlatformRepository(session=db_session)
    client_platform: ClientPlatform = await repo.create(
        schema=ClientPlatformCreate(client_id=client_id, platform_id=platform_id)
    )
    return client_platform


async def assign_website_to_client(
    db_session: AsyncSession,
    website_id: UUID4,
    client_id: UUID4,
) -> ClientWebsite:
    repo: ClientWebsiteRepository = ClientWebsiteRepository(session=db_session)
    client_website: ClientWebsite = await repo.create(
        schema=ClientWebsiteCreate(website_id=website_id, client_id=client_id)
    )
    return client_website


def create_random_client_style_guide(
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
