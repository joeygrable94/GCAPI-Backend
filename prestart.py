from typing import Any  # pragma: no cover

import asyncio
from sqlalchemy.orm import Session  # pragma: no cover
from sqlalchemy.sql import text  # pragma: no cover
from sqlalchemy.ext.asyncio import AsyncSession  # pragma: no cover

from app.db.init_db import build_database
from app.core.logger import logger  # pragma: no cover
from app.db.session import async_session, session  # pragma: no cover


async def init() -> None:  # pragma: no cover
    try:
        await build_database()
    except Exception as e:
        logger.warning(e)
        raise e


async def main() -> None:  # pragma: no cover
    logger.info("Prestarting backend.")
    await init()
    logger.info("Backend ready.")


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
