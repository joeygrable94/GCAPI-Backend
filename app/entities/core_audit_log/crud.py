from app.core.crud import BaseRepository
from app.entities.core_audit_log.model import AuditLog
from app.entities.core_audit_log.schemas import (
    AuditLogCreate,
    AuditLogRead,
    AuditLogUpdate,
)


class AuditLogRepository(
    BaseRepository[AuditLogCreate, AuditLogRead, AuditLogUpdate, AuditLog]
):
    @property
    def _table(self) -> AuditLog:
        return AuditLog
