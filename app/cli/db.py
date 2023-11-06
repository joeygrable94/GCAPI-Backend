import asyncio

import typer

from app.core.logger import logger
from app.db.commands import build_database, check_db_connected, create_init_data

app = typer.Typer()


@app.command()
def check_connection() -> None:
    logger.info("Check Database Connection")

    async def _check_db_connected() -> None:
        await check_db_connected()

    asyncio.run(_check_db_connected())


@app.command()
def create_db() -> None:
    logger.info("Create Database")

    async def _build_database() -> None:
        await build_database()

    asyncio.run(_build_database())


@app.command()
def add_initial_data() -> None:
    logger.info("Load Initial Data")

    async def _create_init_data() -> None:
        await create_init_data()

    asyncio.run(_create_init_data())


if __name__ == "__main__":
    app()
