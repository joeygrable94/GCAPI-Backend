from typing import Any, Callable, List, Optional

from sqlalchemy import Text, types
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.engine.interfaces import Dialect

from app.core.utilities import scope_regex
from app.db.constants import DB_STR_BLOB_MAX_LEN, DB_STR_LONGTEXT_MAX_LEN


class LongText(types.UserDefinedType):
    cache_ok = False

    def __init__(self, length: int = DB_STR_LONGTEXT_MAX_LEN):
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
            return dialect.type_descriptor(Text(length=DB_STR_LONGTEXT_MAX_LEN))

    def result_processor(
        self, dialect: Dialect, coltype: object
    ) -> Optional[Callable[[Any], Any]]:
        def process(value: Any) -> Any:
            return value

        return process


class Scopes(types.TypeDecorator):
    impl = types.BLOB(DB_STR_BLOB_MAX_LEN)

    def process_bind_param(self, value: List[str] | None, dialect: Dialect) -> bytes:
        if value is not None:
            for scope in value:
                if not scope_regex.fullmatch(scope.lower()):
                    raise ValueError("invalid scope format")
            return ",".join(value).encode("utf-8")
        return "".encode("utf-8")

    def process_result_value(self, value: Any | None, dialect: Dialect) -> List[str]:
        if value is not None:
            if isinstance(value, bytes) and len(value) > 0:
                return value.decode("utf-8").split(",")
        return []
