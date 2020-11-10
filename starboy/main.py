import typer
from typing import Optional
from starboy import models, api

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


@app.command('loc')
def get_location():
    """Gets the current logitiude and latitude of the spacecraft"""
    get_long_lat()


@app.command('pass')
def pass_over():
    """To get the time when the ISS will pass over."""
    typer.echo("The ISS will be overhead")


@app.command('people')
def get_people():
    """Gets number of people inside of the Satellite."""
    try:
        response = api.grab_notify('astros.json')
        current_location: models.IsNowResponse = models.IssPersonResponse(
            **response
        )
        typer.secho(current_location.extract(), fg=typer.colors.BRIGHT_GREEN)
        return
    except Exception as e:
        typer.secho(
            f"Ran into an error. {str(e)}",
            err=True,
            fg=typer.colors.BRIGHT_RED
        )


def main():
    app()


if __name__ == "__main__":
    app()