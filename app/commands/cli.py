import typer
from .hello import app as hello_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)

app.add_typer(hello_app)


@app.callback()
def callback():
    """
    Something callback
    """
