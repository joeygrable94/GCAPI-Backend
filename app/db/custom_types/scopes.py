from typing import Any

from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy_utils import ScalarListType  # type: ignore

from app.core.utilities import scope_regex
from app.db.constants import DB_STR_BLOB_MAXLEN_INPUT


class Scopes(ScalarListType):

    def process_bind_param(self, value: Any, dialect: Dialect) -> str:
        processed_value: str | None = None
        if value is not None:
            for scope in value:
                if not scope_regex.fullmatch(scope.lower()):
                    raise ValueError("invalid scope format")
            processed_value = super().process_bind_param(value, dialect)
            if processed_value and len(processed_value) > DB_STR_BLOB_MAXLEN_INPUT:
                raise ValueError("Scopes too long")
        return processed_value or ""

    def process_result_value(self, value: Any, dialect: Dialect) -> list[str]:
        processed_value = super().process_result_value(value, dialect)
        return processed_value if processed_value is not None else []
