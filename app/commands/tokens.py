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
    help="Name",
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
