from __future__ import annotations

from typing import Optional

from pydantic import UUID4

from app.db.acls import BdxFeedACL
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
    username: Optional[str]
    password: Optional[str]
    serverhost: Optional[str]


class BdxFeedRead(BdxFeedACL, BdxFeedBase, BaseSchemaRead):
    id: UUID4
