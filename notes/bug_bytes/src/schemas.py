from enum import Enum
from datetime import date

from pydantic import BaseModel, field_validator


class GenreURLChoices(Enum):
    rock = 'rock'
    electronic = 'electronic'
    metal = 'metal'
    hip_hop = 'hip-hop'


class GenreChoices(Enum):
    rock = 'Rock'
    electronic = 'Electronic'
    metal = 'Metal'
    hip_hop = 'Hip-Hop'


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []


class BandCreate(BandBase):
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        return value.title()


class BandWithID(BandBase):
    id: int
