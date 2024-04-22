from typing import Any, Callable, Optional

from sqlalchemy import Text, types
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.engine.interfaces import Dialect

from app.db.constants import DB_STR_LONGTEXT_MAXLEN_STORED


class LongText(types.UserDefinedType):
    cache_ok = True

    def __init__(self, length: int = DB_STR_LONGTEXT_MAXLEN_STORED):
        self.length = length

    def get_col_spec(self, **kw: Any) -> str:
        return "BLOB(%d)" % self.length

    def bind_processor(self, dialect: Dialect) -> Optional[Callable[[Any], Any]]:
        def process(value: Any) -> Any:
            return value

        return process

    def load_dialect_impl(
        self, dialect: Dialect
    ) -> types.TypeEngine[str]:  # pragma: no cover
        if dialect.name == "mysql":
            return dialect.type_descriptor(LONGTEXT())
        else:
            return dialect.type_descriptor(Text(length=DB_STR_LONGTEXT_MAXLEN_STORED))

    def result_processor(
        self, dialect: Dialect, coltype: object
    ) -> Optional[Callable[[Any], Any]]:
        def process(value: Any) -> Any:
            return value

        return process
