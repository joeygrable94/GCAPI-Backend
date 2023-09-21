from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.acls import GoCloudPropertyACL
from app.db.validators import (
    ValidateSchemaHashedApiKeyOptional,
    ValidateSchemaHashedApiKeyRequired,
    ValidateSchemaHashedProjectIdOptional,
    ValidateSchemaHashedProjectIdRequired,
    ValidateSchemaHashedProjectNumberOptional,
    ValidateSchemaHashedProjectNumberRequired,
    ValidateSchemaHashedServiceAccountOptional,
    ValidateSchemaHashedServiceAccountRequired,
    ValidateSchemaProjectNameRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class GoCloudPropertyBase(
    ValidateSchemaProjectNameRequired,
    ValidateSchemaHashedApiKeyRequired,
    ValidateSchemaHashedProjectIdRequired,
    ValidateSchemaHashedProjectNumberRequired,
    ValidateSchemaHashedServiceAccountRequired,
):
    project_name: str
    hashed_api_key: str
    hashed_project_id: str
    hashed_project_number: str
    hashed_service_account: str


class GoCloudPropertyCreate(GoCloudPropertyBase):
    pass


class GoCloudPropertyUpdate(
    ValidateSchemaHashedApiKeyOptional,
    ValidateSchemaHashedProjectIdOptional,
    ValidateSchemaHashedProjectNumberOptional,
    ValidateSchemaHashedServiceAccountOptional,
):
    project_name: Optional[str] = None
    hashed_api_key: Optional[str] = None
    hashed_project_id: Optional[str] = None
    hashed_project_number: Optional[str] = None
    hashed_service_account: Optional[str] = None


class GoCloudPropertyRead(GoCloudPropertyACL, GoCloudPropertyBase, BaseSchemaRead):
    id: UUID4
