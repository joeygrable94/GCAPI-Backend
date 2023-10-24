from __future__ import annotations

from typing import Optional

from pydantic import UUID4

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
    api_key: str
    secret_key: str


class SharpspringCreate(SharpspringBase):
    pass


class SharpspringUpdate(
    ValidateSchemaHashedApiKeyOptional,
    ValidateSchemaHashedSecretKeyOptional,
):
    api_key: Optional[str] = None
    secret_key: Optional[str] = None


class SharpspringRead(SharpspringBase, BaseSchemaRead):
    id: UUID4
