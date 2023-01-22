import asyncio

from app.core.config import settings
from app.db.init_db import build_database, create_init_data
from app.db.commands import check_db_connected
from app.core.logger import logger  # pragma: no cover


async def main() -> None:  # pragma: no cover
    await check_db_connected()
    if settings.DEBUG_MODE:
        await build_database()
    await create_init_data()


if __name__ == "__main__":  # pragma: no cover
    logger.info("Prestarting backend")
    asyncio.run(main())
    logger.info("Prestart Process Finished")
