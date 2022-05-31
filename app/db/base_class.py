from datetime import datetime
from typing import Optional

from pydantic import UUID4, Field
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.db.utilities import _get_uuid


@as_declarative()
class Base:
    __name__: str
    id: UUID4 = Field(default_factory=_get_uuid)
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically"""
        return cls.__name__.lower()
