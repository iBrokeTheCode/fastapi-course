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


class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Album] = []
