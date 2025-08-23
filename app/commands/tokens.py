from typing import Annotated

import typer
from rich import print

from api.v1.auth.services.by_token import cache_token_storage

app = typer.Typer(
    name="tokens",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(
    help="Check token",
)
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check"),
    ],
):
    print(
        f"Token: [bold]{token}[/bold]",
        (
            "[green]exist[/green]"
            if cache_token_storage.token_exists(token)
            else "[red]dose not exist[/red]"
        ),
    )


@app.command(
    help="Gel all tokens",
    name="list",
)
def all_tokens():
    for token in cache_token_storage.gel_all():
        print(f"- [bold]{token}[/bold]")


@app.command(
    help="Create token",
    name="create",
)
def create_token():
    token = cache_token_storage.generate_and_save_token()
    print(f"- Create new token - [bold]{token}[/bold]")


@app.command(
    help="Add new token",
    name="add",
)
def add_new_token(
    token: Annotated[
        str,
        typer.Argument(help="Add token"),
    ],
):
    cache_token_storage.add_token(token)
    print(f"- Token [bold]{token}[/bold] was added ")


@app.command(
    help="Remove token",
    name="remove",
)
def remove_token(
    token: Annotated[
        str,
        typer.Argument(help="Token"),
    ],
):
    cache_token_storage.rm_token(token)
    print(f"- The token [bold]{token}[/bold] was deleted ")
