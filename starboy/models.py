from typing import List, Optional
import datetime
from pydantic import BaseModel
from toolz.itertoolz import groupby


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
            for craft, persons in groups.items()
        ]

        return "\n\n".join([x.extract() for x in person_groups])

    def extract(self) -> str:
        return self.grouped_craft()


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
