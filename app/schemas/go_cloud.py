from __future__ import annotations

from typing import Optional

from pydantic import UUID4

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
    api_key: str
    project_id: str
    project_number: str
    service_account: str


class GoCloudPropertyCreate(GoCloudPropertyBase):
    pass


class GoCloudPropertyUpdate(
    ValidateSchemaHashedApiKeyOptional,
    ValidateSchemaHashedProjectIdOptional,
    ValidateSchemaHashedProjectNumberOptional,
    ValidateSchemaHashedServiceAccountOptional,
):
    project_name: Optional[str] = None
    api_key: Optional[str] = None
    project_id: Optional[str] = None
    project_number: Optional[str] = None
    service_account: Optional[str] = None


class GoCloudPropertyRead(GoCloudPropertyBase, BaseSchemaRead):
    id: UUID4
