from fastapi import FastAPI, HTTPException


bands_data = [
    {"id": 1, "name": "The Kinks", "genre": "Rock"},
    {"id": 2, "name": "FX Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal"},
    {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
]

app = FastAPI()


@app.get('/bands')
async def bands() -> list[dict]:
    return bands_data


@app.get('/bands/{band_id}')
async def about(band_id: int) -> dict:
    band = next((band for band in bands_data if band['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band
