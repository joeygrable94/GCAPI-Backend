from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email, random_lower_string

from app.crud import GoCloudPropertyRepository
from app.models import GoCloudProperty
from app.schemas import GoCloudPropertyCreate, GoCloudPropertyRead


async def create_random_go_cloud(
    db_session: AsyncSession, client_id: UUID4, is_service_account: bool = False
) -> GoCloudPropertyRead:
    repo: GoCloudPropertyRepository = GoCloudPropertyRepository(session=db_session)
    go_cloud: GoCloudProperty = await repo.create(
        schema=GoCloudPropertyCreate(
            project_name=random_lower_string(chars=64),
            project_id=random_lower_string(chars=64),
            project_number=random_lower_string(chars=64),
            service_account=random_email() if is_service_account else None,
            client_id=client_id,
        )
    )
    return GoCloudPropertyRead.model_validate(go_cloud)
