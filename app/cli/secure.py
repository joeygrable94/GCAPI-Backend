import base64
import os

from app.cli.app import AsyncTyper
from app.core.logger import logger
from app.core.security.encryption.keys import load_api_keys

app = AsyncTyper()


@app.command()
def load_keys() -> None:
    try:
        logger.info("Loading Api Keys...")
        load_api_keys()
    except Exception as e:
        logger.warning(f"Error loading API keys: {e}")


@app.command()
def generate_key(length: int = 32) -> None:
    try:
        logger.info(f"Generating API Key of length: {length}")
        key = os.urandom(length)
        key_str = base64.b64encode(key).decode("utf-8")
        logger.debug(key_str)
    except Exception as e:
        logger.warning(f"Error generating API keys: {e}")


if __name__ == "__main__":
    app()
