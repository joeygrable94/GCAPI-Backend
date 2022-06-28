from typing import Any

from app.core.logger import logger
from app.db.init_db import init_db
from app.db.session import session


def init() -> None:
    db: Any = session()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
