from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.init_db import load_initial_data
from app.db.session import session


def init() -> None:
    try:
        db: Session = session()
        db.execute("SELECT 1")
        load_initial_data(db)
    except Exception as e:
        logger.warning(e)
        raise e


def main() -> None:
    logger.info("Prestart creating initial data.")
    init()
    logger.info("Initial data created.")


if __name__ == "__main__":
    main()
