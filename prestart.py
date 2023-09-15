import asyncio

from app.db.commands import check_db_connected
from app.core.logger import logger


async def main() -> None:  # pragma: no cover
    await check_db_connected()


if __name__ == "__main__":  # pragma: no cover
    logger.info("Prestarting backend")
    asyncio.run(main())
    logger.info("Prestart Process Finished")
