import typer
# from typing_extensions import Annotated

import app.cli.items as items


app = typer.Typer()
app.add_typer(items.app, name="items")


if __name__ == "__main__":
    app()
