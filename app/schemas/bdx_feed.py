from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.validators import (
    ValidateSchemaPasswordOptional,
    ValidateSchemaPasswordRequired,
    ValidateSchemaServerhostOptional,
    ValidateSchemaServerhostRequired,
    ValidateSchemaUsernameOptional,
    ValidateSchemaUsernameRequired,
)
from app.schemas.base import BaseSchemaRead


# schemas
class BdxFeedBase(
    ValidateSchemaUsernameRequired,
    ValidateSchemaPasswordRequired,
    ValidateSchemaServerhostRequired,
):
    username: str
    password: str
    serverhost: str
    client_id: UUID4


class BdxFeedCreate(BdxFeedBase):
    pass


class BdxFeedUpdate(
    ValidateSchemaUsernameOptional,
    ValidateSchemaPasswordOptional,
    ValidateSchemaServerhostOptional,
):
    username: Optional[str] = None
    password: Optional[str] = None
    serverhost: Optional[str] = None


class BdxFeedRead(BdxFeedBase, BaseSchemaRead):
    id: UUID4
