import typer

import app.cli.db as db
import app.cli.secure as secure


app = typer.Typer()
app.add_typer(db.app, name="db", help="Database operations")
app.add_typer(secure.app, name="secure", help="Security operations")


if __name__ == "__main__":
    app()
