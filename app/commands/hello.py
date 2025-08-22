from typing import Annotated

import typer
from rich import print

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(
    help="Name",
)
def hello(name: Annotated[str, typer.Argument(help="Name to grate")]):
    print(f"[bold green]hello {name}[/bold green]")


@app.callback()
def callback():
    """
    Something callback
    """
