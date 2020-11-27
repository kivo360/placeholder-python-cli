from typing import List, Optional
import datetime
from pydantic import BaseModel, DirectoryPath
from toolz.itertoolz import groupby
from pathlib import Path


# The ISS will be overhead {LAT, LONG} at {time} for {duration}
class LocationModel(BaseModel):
    longitude: float
    latitude: float


class IsNowResponse(BaseModel):
    iss_position: LocationModel
    timestamp: datetime.datetime
    message: str

    def extract(self):
        return f"The ISS will be overhead  {{{self.iss_position.latitude}, {self.iss_position.longitude}}} at {self.timestamp} UTC"


class Person(BaseModel):
    name: str
    craft: str

    def extract(self):
        return f"name: {self.name} -- craft: {self.craft}"


class PersonGroup(BaseModel):
    craft: str
    number: int
    people: List[Person]

    def get_people(self) -> str:
        """
        get_people Get People

        Get a string list of people and join them.
        """
        return " ... ".join([x.extract() for x in self.people])

    def extract(self):
        return f"There are {self.number} people aboard the {self.craft}. They are {self.get_people()}"


class IssPersonResponse(BaseModel):
    number: int
    message: str
    people: List[Person]

    def get_people(self) -> str:
        """
        get_people Get People

        Get a string list of people and join them.
        """
        return " ... ".join([x.extract() for x in self.people])

    def grouped_craft(self) -> str:
        groups = groupby('craft', [x.dict() for x in self.people])
        person_groups: List[PersonGroup] = [
            PersonGroup(craft=craft, number=len(persons), people=persons)
            for craft,
            persons in groups.items()
        ]

        return "\n\n".join([x.extract() for x in person_groups])

    def extract(self) -> str:
        return self.grouped_craft()


class PathTraversal(BaseModel):
    current_dir: DirectoryPath = Path.cwd()

    def find_project_root(self):
        curr = self.current_dir

        filtration_list = ['poetry.lock', 'pants.toml', 'pants']
        for _ in range(6):
            x = curr.glob("*")
            y = filter(lambda a: a.is_file(), x)
            z = filter(lambda b: b.name in filtration_list, y)
            z = list(z)
            if len(z) >= 3:
                return curr
            curr = curr.parent
        raise AttributeError("Could not find the project root folder.")

    def find_sub_project_root(self) -> List[Path]:
        """
        Find Sub-Project Roots

        We take the pants project root folder then find all poetry subprojects and return a list of absolute paths.
        
        We use this list to get the relative paths to install the poetry projects into the super directory.
        """
        # 1. Do a recursive glob search.
        # 2. Start with project root folder.
        # 3. Find all poetry.lock and pyproject.toml files.
        # 4. Use set theory to find the intersections between sets of poetry.lock and pyproject.toml (common folders)
        # 5. Return the resulting sets
        return []


# {
#     message:
#     "success",
#     people: [{
#         name: "Sergey Ryzhikov",
#         craft: "ISS"
#     }, {
#         name: "Kate Rubins",
#         craft: "ISS"
#     }, {
#         name: "Sergey Kud-Sverchkov",
#         craft: "ISS"
#     }],
#     number:
#     3
# }
