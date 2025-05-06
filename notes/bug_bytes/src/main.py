from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Path

from schemas import GenreURLChoices, BandCreate, BandWithID


bands_data = [
    {"id": 1, "name": "The Kinks", "genre": "Rock"},
    {"id": 2, "name": "FX Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal", "albums": [
        {"title": "Master of Reality", "release_date": "1971-07-21"}]},
    {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
]

app = FastAPI()


@app.get('/bands', response_model=list[BandWithID])
async def get_bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None
) -> list[BandWithID]:
    bands_list = [BandWithID(**band) for band in bands_data]

    if genre:
        bands_list = [
            band for band in bands_list if band.genre.value.lower() == genre.value]

    if q:
        bands_list = [band for band in bands_list if q.lower()
                      in band.name.lower()]

    return bands_list


@app.post('/bands', response_model=BandWithID)
async def create_band(band_data: BandCreate):
    generated_id = bands_data[-1]['id'] + 1
    new_band = BandWithID(id=generated_id, **band_data.model_dump())
    bands_data.append(new_band.model_dump())

    return new_band


@app.get('/bands/{band_id}', response_model=BandWithID, status_code=200)
async def get_band(band_id: Annotated[int, Path(title='The band ID')]) -> BandWithID:
    band = next(
        (BandWithID(**band) for band in bands_data if band['id'] == band_id),
        None
    )

    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band


@app.get('/bands/genre/{genre}')
async def get_bands_by_genre(genre: GenreURLChoices) -> list[dict]:
    return [band for band in bands_data if band['genre'].lower() == genre.value.lower()]
