import typer
import datetime
from typing import Optional
import requests
from pydantic import BaseModel, validate_arguments

app = typer.Typer()

CORE_URL = "http://api.open-notify.org/"


@validate_arguments
def grab_notify(location: str):
    return requests.get(f"{CORE_URL}/{location}").json()