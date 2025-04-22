from enum import Enum

from fastapi import FastAPI, HTTPException


bands_data = [
    {"id": 1, "name": "The Kinks", "genre": "Rock"},
    {"id": 2, "name": "FX Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal"},
    {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
]

app = FastAPI()


@app.get('/bands')
async def get_bands() -> list[dict]:
    return bands_data


@app.get('/bands/{band_id}')
async def get_band(band_id: int) -> dict:
    band = next((band for band in bands_data if band['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band


class GenreURLChoices(Enum):
    rock = 'rock'
    electronic = 'electronic'
    metal = 'metal'
    hip_hop = 'hip-hop'


# @app.get('/bands/genre/{genre}', status_code=200)
@app.get('/bands/genre/{genre}')
async def get_bands_by_genre(genre: GenreURLChoices) -> list[dict]:
    return [band for band in bands_data if band['genre'].lower() == genre.value.lower()]
