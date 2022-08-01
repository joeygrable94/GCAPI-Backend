from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.init_db import build_database
from app.db.session import session


def init() -> None:
    try:
        db: Session = session()
        db.execute("SELECT 1")
        build_database()
    except Exception as e:
        logger.warning(e)
        raise e


def main() -> None:
    logger.info("Prestarting backend.")
    init()


if __name__ == "__main__":
    main()
