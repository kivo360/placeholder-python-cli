import typer
from typing import Optional
from starboy import models, api, onboard
# from starboy import onboard
app = typer.Typer()


def get_long_lat():
    current_location: Optional[models.IsNowResponse] = None
    try:
        response = api.grab_notify('iss-now.json')
        current_location: models.IsNowResponse = models.IsNowResponse(
            **response
        )
        typer.secho(current_location.extract(), fg=typer.colors.BRIGHT_GREEN)
        return
    except Exception as e:
        typer.secho("Ran into an error.", err=True, fg=typer.colors.BRIGHT_RED)


@app.command('create')
def create_project():
    """
        Gets the root project level then traverses down src/python to be able to create a new project with poetry.
        
        Get the relative directory of this new project from the root poetry project this project will add it via poetry add.
    """
    traverser = models.PathTraversal()
    traverser.find_project_root()


@app.command('trial')
def get_location():
    """Gets the current logitiude and latitude of the spacecraft"""
    get_long_lat()


app.add_typer(onboard.app, name="onboard", help="Setup your dev environment")


def main():
    app()


if __name__ == "__main__":
    app()