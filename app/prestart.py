from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import session


def init() -> None:
    try:
        db: Session = session()
        db.execute("SELECT 1")
    except Exception as e:
        logger.warning(e)
        raise e


def main() -> None:
    logger.info("Prestarting backend tests.")
    init()
    logger.info("Backend tests ready to commence.")


if __name__ == "__main__":
    main()
