from anyio import run
from sqlalchemy_data_model_visualizer import (
    add_web_font_and_interactivity,
    generate_data_model_diagram,
)
from typer import Typer

from app.core.config import settings
from app.core.logger import logger
from app.db.commands import build_database, check_db_connected, create_init_data

app = Typer()


@app.command()
def check_db_connection() -> None:
    try:
        run(check_db_connected)
    except Exception as e:
        logger.warning(f"Error checking DB connection: {e}")


@app.command()
def create_db() -> None:
    try:
        logger.info("Create Database")
        run(build_database)
    except Exception as e:
        logger.warning(f"Error building database: {e}")


@app.command()
def add_initial_data() -> None:
    try:
        logger.info("Load Initial Data")
        count = run(create_init_data)
        logger.info(f"Data Inserted C[{count}]")
    except Exception as e:
        logger.warning(f"Error adding initial DB data: {e}")


@app.command()
def generate_schema_graph() -> None:
    try:
        logger.info("Generating Schema Graph")
        app_name = settings.api.name.lower()
        from app import models

        all_models = [getattr(models, m) for m in models.__all__]
        output_file_name = f"./docs/{app_name}_schema_graph"
        output_file_interactive = f"./docs/{output_file_name}_interactive.svg"
        generate_data_model_diagram(all_models, output_file_name)  # type: ignore
        add_web_font_and_interactivity(  # type: ignore
            output_file_name, output_file_interactive
        )
    except Exception as e:
        logger.warning(f"Error creating schema graph: {e}")


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        logger.warning("CLI Interrupted")
    except Exception as e:
        logger.warning(f"Error running CLI: {e}")
