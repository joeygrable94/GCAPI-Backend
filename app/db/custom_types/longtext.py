from collections.abc import Callable
from typing import Any

from sqlalchemy import LargeBinary, types
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.interfaces import Dialect

from app.db.constants import DB_STR_LONGTEXT_MAXLEN_STORED


class LongText(types.UserDefinedType):
    cache_ok = True

    def __init__(self, length: int = DB_STR_LONGTEXT_MAXLEN_STORED):
        self.length = length

    def get_col_spec(self, **kw: dict) -> str:
        return "LONGBLOB"

    def bind_processor(
        self, dialect: Dialect
    ) -> Callable[[str], str] | None:  # pragma: no cover
        def process(value: str) -> str:
            return value

        return process

    def load_dialect_impl(
        self, dialect: Dialect
    ) -> types.TypeEngine[str]:  # pragma: no cover
        if dialect.name == "mysql":
            return dialect.type_descriptor(mysql.LONGBLOB())
        else:
            return dialect.type_descriptor(
                LargeBinary(length=DB_STR_LONGTEXT_MAXLEN_STORED)
            )

    def result_processor(
        self, dialect: Dialect, coltype: object
    ) -> Callable[[Any], Any] | None:  # pragma: no cover
        def process(value: Any) -> Any:
            return value

        return process
