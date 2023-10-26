from typing import Any

from sqlalchemy.orm import declarative_base

declared_base: Any = declarative_base()


class Base(declared_base):
    pass
