import base64
import os

import typer

from app.core.logger import logger
from app.core.security.encryption.keys import load_api_keys

app = typer.Typer()


@app.command()
def load_keys() -> None:
    logger.info("Loading Api Keys...")
    load_api_keys()


@app.command()
def generate_key(length: int = 32) -> None:
    logger.info(f"Generating API Key of length: {length}")
    key = os.urandom(length)
    key_str = base64.b64encode(key).decode("utf-8")
    logger.debug(key_str)


if __name__ == "__main__":
    app()
