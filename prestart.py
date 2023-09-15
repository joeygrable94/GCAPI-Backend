import asyncio

from app.db.commands import check_db_connected
from app.core.logger import logger
from app.db.init_db import create_db_tables, drop_db_tables  # pragma: no cover


async def main() -> None:  # pragma: no cover
    await check_db_connected()
    drop_db_tables()
    create_db_tables()


if __name__ == "__main__":  # pragma: no cover
    logger.info("Prestarting backend")
    asyncio.run(main())
    logger.info("Prestart Process Finished")
