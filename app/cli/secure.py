import typer

from app.core.security.encryption.keys import load_api_keys

app = typer.Typer()


@app.command()
def load_keys() -> None:
    print("Loading Api Keys...")
    load_api_keys()


if __name__ == "__main__":
    app()
