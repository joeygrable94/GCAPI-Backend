from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.acls import SharpspringACL
from app.db.validators import (
    ValidateSchemaHashedApiKeyOptional,
    ValidateSchemaHashedApiKeyRequired,
    ValidateSchemaHashedSecretKeyOptional,
    ValidateSchemaHashedSecretKeyRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class SharpspringBase(
    ValidateSchemaHashedApiKeyRequired,
    ValidateSchemaHashedSecretKeyRequired,
):
    hashed_api_key: str
    hashed_secret_key: str


class SharpspringCreate(SharpspringBase):
    pass


class SharpspringUpdate(
    ValidateSchemaHashedApiKeyOptional,
    ValidateSchemaHashedSecretKeyOptional,
):
    hashed_api_key: Optional[str] = None
    hashed_secret_key: Optional[str] = None


class SharpspringRead(SharpspringACL, SharpspringBase, BaseSchemaRead):
    id: UUID4
