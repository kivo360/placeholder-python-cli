import pathlib

import typer
from typer import colors
from pydantic import validate_arguments
HOME_FOLDER = pathlib.Path().home()


@validate_arguments
def home(*args) -> pathlib.Path:
    larg = list(args)
    home_list = [HOME_FOLDER]
    zlist = home_list + larg
    return pathlib.Path(*zlist)
