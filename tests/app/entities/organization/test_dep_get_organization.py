import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.errors import InvalidID
from app.entities.core_organization.dependencies import get_organization_or_404
from app.entities.core_organization.errors import OrganizationNotFound
from app.entities.core_organization.model import Organization
from app.utilities import get_uuid_str
from tests.utils.organizations import create_random_organization

pytestmark = pytest.mark.asyncio


async def test_get_organization_or_404(db_session: AsyncSession) -> None:
    test_organization = await create_random_organization(db_session)
    result = await get_organization_or_404(db_session, test_organization.id)
    assert isinstance(result, Organization)
    assert result.id == test_organization.id

    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_organization_or_404(db_session, fake_clid)

    fake_clid = get_uuid_str()
    with pytest.raises(OrganizationNotFound):
        await get_organization_or_404(db_session, fake_clid)
