import typer

from .hello import app as hello_app
from .tokens import app as tokens_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)

app.add_typer(hello_app)
app.add_typer(tokens_app)


@app.callback()
def callback() -> None:
    """
    Something callback
    """
