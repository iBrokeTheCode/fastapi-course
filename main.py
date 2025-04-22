from fastapi import FastAPI, HTTPException

from schemas import GenreURLChoices, Band


bands_data = [
    {"id": 1, "name": "The Kinks", "genre": "Rock"},
    {"id": 2, "name": "FX Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal", "albums": [
        {"title": "Master of Reality", "release_date": "1971-07-21"}]},
    {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
]

app = FastAPI()


@app.get('/bands', response_model=list[Band])
async def get_bands() -> list[Band]:
    return [Band(**band) for band in bands_data]


@app.get('/bands/{band_id}', response_model=Band, status_code=200)
async def get_band(band_id: int) -> Band:
    band = next(
        (Band(**band) for band in bands_data if band['id'] == band_id),
        None
    )

    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band


@app.get('/bands/genre/{genre}')
async def get_bands_by_genre(genre: GenreURLChoices) -> list[dict]:
    return [band for band in bands_data if band['genre'].lower() == genre.value.lower()]
