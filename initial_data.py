import asyncio

from app.db.commands import check_db_connected
from app.db.init_db import create_init_data
from app.core.logger import logger  # pragma: no cover


async def main() -> None:  # pragma: no cover
    await check_db_connected()
    await create_init_data()


if __name__ == "__main__":  # pragma: no cover
    logger.info("Loading Inital Data")
    asyncio.run(main())
    logger.info("Inital Data Loaded")
