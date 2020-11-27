import os
import platform
import time
from contextlib import suppress

import sh
import typer
from sh import git, which
from starboy.commands import apt, apt_get, csh, curl
from starboy.statics import home
from typer import colors

SYSTEM = platform.system().upper()


def zsh_linux(password):
    with sh.contrib.sudo(password=password, _with=True):
        apt('update', '-y')
        apt(
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
        typer.echo("Installing zsh through apt-get")
        for line in apt_get("install", "zsh", _iter=True):
            typer.echo(line)
        typer.echo("Setting zsh as the default cli.")
        csh(which("-s", "zsh"))
        typer.secho(
            "You've successfully installed zsh.", fg=colors.BRIGHT_GREEN
        )


def zsh_windows(password):
    with sh.contrib.sudo(password=password, _with=True):
        typer.echo("Installing zsh through apt-get")
        for line in apt_get("install", "zsh", _iter=True):
            typer.echo(line)
        typer.echo("Setting zsh as the default cli.")
        csh(which("-s", "zsh"))
        typer.secho(
            "You've successfully installed zsh.", fg=colors.BRIGHT_GREEN
        )


def install_zsh_shell(password: str):
    linux_os = "Linux".upper()
    windows_os = "Windows".upper()
    {
        linux_os: zsh_linux, windows_os: zsh_windows
    }[SYSTEM](password=password)


def install_goodies(password: str):
    # git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    typer.echo("Installing oh-my-zsh")
    path = home(".oh-my-zsh",)
    # typer.secho(str(path), fg=colors.BLUE)

    if not path.exists():
        with suppress():
            sh.bash(
                "-c",
                curl(
                    "-fsSL",
                    "https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
                )
            )

    typer.secho(
        "You've successfully installed oh-my-zsh.", fg=colors.BRIGHT_GREEN
    )

    path = home(".oh-my-zsh", 'custom', 'plugins', 'zsh-syntax-highlighting')
    if not path.exists():
        typer.secho("Installing Zsh syntax highlighting")
        with suppress():
            git.clone(
                "https://github.com/zsh-users/zsh-syntax-highlighting.git",
                "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"
            )

    path = home(".oh-my-zsh", 'custom', 'plugins', 'zsh-autosuggestions')
    typer.echo("Installing zsh autosuggestions")
    if not path.exists():
        with suppress():
            git.clone(
                "https://github.com/zsh-users/zsh-autosuggestions",
                "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions",
            )
    typer.secho(
        "Successfully installed zsh autosuggestions", fg=colors.BRIGHT_GREEN
    )
    typer.secho(
        "Make sure to add zsh-completions zsh-syntax-highlighting zsh-autosuggestions to your plugins",
        fg=colors.YELLOW
    )

    typer.secho(
        "You've successfully installed zsh goodies", fg=colors.BRIGHT_YELLOW
    )


def install_pyenv(password: str):
    with sh.contrib.sudo(password=password, _with=True):

        updates = apt('update', '-y', _iter=True)
        with typer.progressbar(
            updates, label="Updating from APT Respository"
        ) as progress:
            for line in progress:
                typer.echo(line)
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
                typer.echo(line)

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
                    f.write(b'export PYENV_ROOT="$HOME/.pyenv"')
                    f.write(b'export PATH="$PYENV_ROOT/bin:$PATH"')
                    f.write(b'eval "$(pyenv init -)"')
                    f.write(b'eval "$(pyenv virtualenv-init -)"')
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

    time.sleep(5)
    typer.secho("Redircting you to instructions in 5 seconds ...")
    # typer.launch(
    #     "https://medium.com/@marine.ss/installing-pyenv-on-ubuntu-20-04-c3a609a20aa2"
    # )
