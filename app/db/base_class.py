from typing import Any

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __tablename__: str
    __table_args__: Any = {"mysql_engine": "InnoDB"}
    __mapper_args__: Any = {"always_refresh": True}
