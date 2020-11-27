import pathlib
import typer
import time

from typing import Optional
from starboy import models, api
from starboy.onboard import install_poetry
from starboy.onboard.zsh_shell import (
    install_zsh_shell, install_goodies, install_pyenv
)

app = typer.Typer()

# HOME_FOLDER = pathlib.Path().home()


@app.command('install')
def setup_computer(
    password: str = typer.Option(
        ...,
        prompt=True,
        hide_input=True,
        help='Enter your sudo password to install everything.'
    ),
):
    """A single command that aims to install everything on the computer."""
    is_zsh = typer.confirm(
        "Would you like to switch to ZSH? (would make things easier)"
    )
    if is_zsh:
        install_zsh_shell(password)
        is_zsh_goodies = typer.confirm(
            "Would you also like to install exta functionality into zsh (better dev experience)?"
        )
        if is_zsh_goodies:
            install_goodies(password=password)
    time.sleep(2)
    typer.secho("Installing PyEnv and Poetry", fg=typer.colors.MAGENTA)
    typer.echo("----------------------------------------------------")
    install_pyenv(password=password)
    install_poetry()
    # apt()
