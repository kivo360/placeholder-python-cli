import os
import platform
from contextlib import suppress

import sh
import typer
from sh import git, which
from starboy.commands import curl
from typer import colors, echo, secho

SYSTEM = platform.system().upper()


def install_poetry():
    secho("\nAttempting to install poetry", bold=True, fg=colors.BRIGHT_MAGENTA)

    with suppress():
        h = open("/tmp/get-poetry.py", '+wb')
        curl(
            "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py",
            _out=h
        )
        resp = sh.bash("python", "/tmp/get-poetry.py", "--preview")
        for res in resp:
            echo(res)
    # typer.launch(
    #     "https://medium.com/@marine.ss/installing-pyenv-on-ubuntu-20-04-c3a609a20aa2"
    # )
