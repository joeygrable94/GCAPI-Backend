import typer

app = typer.Typer()


@app.command()
def create(item: str) -> None:
    print(f"Creating item: {item}")


@app.command()
def delete(item: str) -> None:
    print(f"Deleting item: {item}")


@app.command()
def sell(item: str) -> None:
    print(f"Selling item: {item}")


if __name__ == "__main__":
    app()
