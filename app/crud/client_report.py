from typing import Type

from app.crud.base import BaseRepository
from app.models import ClientReport
from app.schemas import ClientReportCreate, ClientReportRead, ClientReportUpdate


class ClientReportRepository(
    BaseRepository[
        ClientReportCreate, ClientReportRead, ClientReportUpdate, ClientReport
    ]
):
    @property
    def _table(self) -> Type[ClientReport]:  # type: ignore
        return ClientReport
