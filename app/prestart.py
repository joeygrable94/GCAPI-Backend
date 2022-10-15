from typing import Any  # pragma: no cover

from sqlalchemy.orm import Session  # pragma: no cover
from sqlalchemy.sql import text  # pragma: no cover

from app.core.logger import logger  # pragma: no cover
from app.db.session import session  # pragma: no cover


def init() -> None:  # pragma: no cover
    try:
        db: Session = session()
        stmt: Any = text("SELECT 1")
        db.execute(stmt)
    except Exception as e:
        logger.warning(e)
        raise e


def main() -> None:  # pragma: no cover
    logger.info("Prestarting backend.")
    init()


if __name__ == "__main__":  # pragma: no cover
    main()
