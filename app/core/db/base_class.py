from typing import Optional
from datetime import datetime

from pydantic import UUID4, Field
from sqlalchemy.ext.declarative import (
    as_declarative,
)
from app.core.db.utilities import _get_uuid


@as_declarative()
class Base:
    id: UUID4 = Field(default_factory=_get_uuid)
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
