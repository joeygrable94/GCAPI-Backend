from app.core.logger import logger
from app.core.db.init_db import init_db
from app.core.db.session import session_local


def init() -> None:
    db = session_local()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
