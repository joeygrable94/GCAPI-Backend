import asyncio

import typer
from sqlalchemy_data_model_visualizer import (
    add_web_font_and_interactivity,
    generate_data_model_diagram,
)

from app.core.config import settings
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


@app.command()
def generate_schema_graph() -> None:
    logger.info("Generating Schema Graph")
    app_name = settings.api.name.lower()
    from app import models

    all_models = [getattr(models, m) for m in models.__all__]
    output_file_name = f"./docs/{app_name}_schema_graph"
    output_file_interactive = f"./docs/{output_file_name}_interactive.svg"
    generate_data_model_diagram(  # type: ignore
        all_models, output_file_name, view_diagram=False
    )
    add_web_font_and_interactivity(  # type: ignore
        output_file_name, output_file_interactive
    )


if __name__ == "__main__":
    app()
