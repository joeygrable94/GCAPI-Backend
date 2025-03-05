import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.organization_website.crud import OrganizationWebsiteRepository
from app.entities.organization_website.model import OrganizationWebsite

pytestmark = pytest.mark.anyio


async def test_organization_websites_repo_table(db_session: AsyncSession) -> None:
    repo: OrganizationWebsiteRepository = OrganizationWebsiteRepository(
        session=db_session
    )
    assert repo._table is OrganizationWebsite
