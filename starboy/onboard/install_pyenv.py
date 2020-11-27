import os
import platform
from contextlib import suppress

import sh
import typer
from sh import git, which
from starboy.commands import apt_get, csh, curl, apt
from starboy.statics import home
from typer import colors

SYSTEM = platform.system().upper()


def install_pyenv(password: str):
    with sh.contrib.sudo(password=password, _with=True):

        updates = apt('update', '-y', _iter=True)
        for line in updates:
            print(line)
        dependencies = apt(
            'install',
            '-y',
            'make',
            'build-essential',
            'libssl-dev',
            'zlib1g-dev',
            'libbz2-dev',
            'libreadline-dev',
            'libsqlite3-dev',
            'wget',
            'curl',
            'llvm',
            'libncurses5-dev',
            'libncursesw5-dev',
            'xz-utils',
            'tk-dev',
            'libffi-dev',
            'liblzma-dev',
            'python-openssl',
            'git',
        )
        with typer.progressbar(
            dependencies, label="Installing Dependencies"
        ) as progress:
            for line in progress:
                pass

        path = home(".pyenv",)
        if not path.exists():
            git.clone(
                "https://github.com/pyenv/pyenv.git",
                "~/.pyenv",
            )

        is_zsh = typer.confirm(
            "We just finished installing pyenv. Would you like us to add it to your zsh file?"
        )

        if is_zsh:
            path = home(".zshrc",)
            if path.exists():
                with open(path, 'wb') as f:
                    f.write('export PYENV_ROOT="$HOME/.pyenv"')
                    f.write('export PATH="$PYENV_ROOT/bin:$PATH"')
                    f.write('eval "$(pyenv init -)"')
                    f.write('eval "$(pyenv virtualenv-init -)"')
            else:
                typer.secho(
                    ".zshrc file doesn't exist.",
                    bg=colors.BRIGHT_RED,
                    bold=True
                )

        typer.secho("Finished installing PyEnv!", bg=colors.BLUE, bold=True)
        typer.secho(
            "You should should log out of your terminal then. We're openning a page for you. Install Python 3.8.5 with it.",
            bold=True
        )
    # typer.launch(
    #     "https://medium.com/@marine.ss/installing-pyenv-on-ubuntu-20-04-c3a609a20aa2"
    # )
