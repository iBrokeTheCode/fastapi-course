from enum import Enum
from datetime import date

from pydantic import BaseModel


class GenreURLChoices(Enum):
    rock = 'rock'
    electronic = 'electronic'
    metal = 'metal'
    hip_hop = 'hip-hop'


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: str
    albums: list[Album] = []


class BandCreate(BandBase):
    pass
    # @validator("genre", pre=True)
    # def title_case_genre(cls, value):
    #     return value.title()


class BandWithID(BandBase):
    id: int
