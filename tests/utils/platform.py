from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.platform.crud import PlatformRepository
from app.entities.platform.model import Platform
from app.entities.platform.schemas import PlatformCreate, PlatformRead
from tests.utils.utils import random_lower_string


async def create_random_platform(
    db_session: AsyncSession,
    slug: str | None = None,
    title: str | None = None,
    is_active: bool = True,
) -> PlatformRead:
    repo: PlatformRepository = PlatformRepository(session=db_session)
    if title is None:
        title = random_lower_string()
    if slug is None:
        slug = random_lower_string()
    platform: Platform = await repo.create(
        PlatformCreate(slug=slug, title=title, is_active=is_active)
    )
    return PlatformRead.model_validate(platform)


async def get_platform_by_slug(db_session: AsyncSession, slug: str) -> PlatformRead:
    repo: PlatformRepository = PlatformRepository(session=db_session)
    platform: Platform | None = await repo.read_by(field_name="slug", field_value=slug)
    if platform is None:
        raise ValueError(f"Platform with slug {slug} not found")
    return PlatformRead.model_validate(platform)
