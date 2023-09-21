from __future__ import annotations

from typing import List, Optional

from pydantic import UUID4

from app.db.acls import GoSearchConsolePropertyACL
from app.db.validators import ValidateSchemaTitleOptional, ValidateSchemaTitleRequired
from app.schemas.base import BaseSchemaRead


# schemas
class GoSearchConsolePropertyBase(
    ValidateSchemaTitleRequired,
):
    title: str
    client_id: UUID4
    website_id: UUID4


class GoSearchConsolePropertyCreate(GoSearchConsolePropertyBase):
    pass


class GoSearchConsolePropertyUpdate(
    ValidateSchemaTitleOptional,
):
    title: Optional[str] = None
    client_id: Optional[UUID4] = None
    website_id: Optional[UUID4] = None


class GoSearchConsolePropertyRead(
    GoSearchConsolePropertyACL,
    GoSearchConsolePropertyBase,
    BaseSchemaRead,
):
    id: UUID4


# relationships
class GoSearchConsolePropertyReadRelations(GoSearchConsolePropertyRead):
    gsc_countries: Optional[List["GoSearchConsoleCountryRead"]] = []
    gsc_devices: Optional[List["GoSearchConsoleDeviceRead"]] = []
    gsc_pages: Optional[List["GoSearchConsolePageRead"]] = []
    gsc_queries: Optional[List["GoSearchConsoleQueryRead"]] = []
    gsc_searchappearances: Optional[List["GoSearchConsoleSearchappearanceRead"]] = []


from app.schemas.go_sc_country import GoSearchConsoleCountryRead  # noqa: E402
from app.schemas.go_sc_device import GoSearchConsoleDeviceRead  # noqa: E402
from app.schemas.go_sc_page import GoSearchConsolePageRead  # noqa: E402
from app.schemas.go_sc_query import GoSearchConsoleQueryRead  # noqa: E402
from app.schemas.go_sc_searchappearance import (  # noqa: E402
    GoSearchConsoleSearchappearanceRead,
)

GoSearchConsolePropertyReadRelations.model_rebuild()
