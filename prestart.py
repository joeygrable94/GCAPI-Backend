import asyncio

from app.db.init_db import create_init_data
from app.db.commands import check_db_connected
from app.core.logger import logger  # pragma: no cover


async def init() -> None:  # pragma: no cover
    try:
        await check_db_connected()
        await create_init_data()
    except Exception as e:
        logger.warning(e)
        raise e


async def main() -> None:  # pragma: no cover
    logger.info("Prestarting backend.")
    try:
        t1 = loop.create_task(init())
        await asyncio.wait([t1])
    except Exception as e:
        logger.info(f"Error: {e}")
    logger.info("Backend ready.")


if __name__ == "__main__":  # pragma: no cover
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except RuntimeError as r:
        logger.info(f"Runtime Error: {r}")
    except Exception as e:
        logger.info(f"Error: {e}")
    finally:
        loop.close()
