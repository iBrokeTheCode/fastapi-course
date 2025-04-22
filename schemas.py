from enum import Enum

from pydantic import BaseModel


class GenreURLChoices(Enum):
    rock = 'rock'
    electronic = 'electronic'
    metal = 'metal'
    hip_hop = 'hip-hop'


class Band(BaseModel):
    id: int
    name: str
    genre: str
