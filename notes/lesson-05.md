# FastAPI Request Body and POST Requests with Pydantic

## 1. Core Concepts

- **Handling Request Bodies in POST Requests:** FastAPI allows you to easily handle data sent by clients in the body of POST requests, which is a common way to create new resources on the server. This data can be in formats like JSON or form data.
- **Pydantic Models for Request Body Declaration:** To define the structure and expected data types of the request body, FastAPI utilizes Pydantic models. By declaring a parameter in your endpoint function with a Pydantic model as its type hint, FastAPI automatically handles the parsing and validation of the incoming data.
- **Distinction Between Request and Response Bodies:** The **request body** is the data sent from the client to the FastAPI server, and the **response body** is the data sent back from the server to the client after processing the request.
- **Refactoring Pydantic Models:** For better code organization and flexibility, we refactored a single Pydantic model into three:
  - **`BandBase`:** This base model contains common fields shared across different representations of a band (e.g., `name`, `genre`, `albums`). It acts like an abstract class holding shared properties.
  - **`BandCreate`:** This model inherits from `BandBase` and defines the fields expected when a new band is created via a POST request. It typically excludes fields that are auto-generated on the server, such as an ID.
  - **`BandWithID`:** This model also inherits from `BandBase` but includes additional fields like the `id`, which would be present when representing an existing band.
- **Inspiration from FastAPI Full-Stack Example:** The video mentions that this pattern of using base models and specific create/with-ID models is inspired by the structure found in the official FastAPI full-stack application example.
- **Creating POST Endpoints:** In FastAPI, you can define a POST request endpoint using the `@app.post()` decorator followed by the path of the endpoint. This decorator associates the defined function with handling incoming POST requests to that specific path.
- **Type Hinting the Request Body:** Within the function that handles the POST request, you can declare a parameter and type-hint it with the `BandCreate` Pydantic model. FastAPI will then automatically expect the incoming request body to conform to this model.
- **Automatic Data Extraction and Validation:** FastAPI, in conjunction with Pydantic, automatically extracts the data from the request body and validates it against the defined Pydantic model. If the data does not conform to the model, FastAPI will return an error response.
- **Returning Responses with Generated IDs:** When creating a new resource via a POST request, the server often generates a unique ID. The video shows how to return a response body that includes this newly generated ID, typically by using the `BandWithID` Pydantic model as the `response_model` for the POST endpoint.
- **Testing with HTTP Clients:** The video demonstrates using the **REST Client** extension in VS Code to send HTTP requests directly from the editor. This allows for easy testing of API endpoints, including sending POST requests with a JSON request body.
- **Automatic API Documentation:** FastAPI automatically generates API documentation (using Swagger UI or ReDoc) based on the defined routes and Pydantic models. This documentation includes the expected schema for the request body of POST endpoints and the structure of the response body.
- **Using Enums for Data Constraints:** Pydantic allows the use of Python `enum.Enum` to restrict the possible values for a field in a Pydantic model. This is useful for ensuring data integrity, for example, by limiting the allowed genres for a band.
- **Pydantic Pre-Validators for Data Transformation:** Pydantic's `@validator` decorator with `pre=True` can be used to define **pre-validators**. These functions are executed before the regular validation takes place and can be used to transform incoming data. The video demonstrates using a pre-validator to convert the `genre` field to title case, ensuring consistency regardless of the client's input format.

## 2. Resources

- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI sample app](https://github.com/fastapi/full-stack-fastapi-template)

## 3. Practical Steps

**Step 1: Refactor Pydantic Schemas**
Create `schemas.py` and define `BandBase`, `BandCreate`, and `BandWithID` Pydantic models.

```python
# schemas.py
from enum import Enum
from datetime import date
from typing import Optional

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
    albums: Optional[list[Album]] = []

class BandCreate(BandBase):
    pass

class BandWithID(BandBase):
    id: int
```

**Step 2: Update Imports in `main.py`**
Modify the import statement in your `main.py` file to include the new schema classes.

```python
# main.py
from fastapi import FastAPI, HTTPException

from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID

bands_data = [
    {"id": 1, "name": "The Kinks", "genre": "Rock"},
    {"id": 2, "name": "FX Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal", "albums": [
        {"title": "Master of Reality", "release_date": "1971-07-21"}]},
    {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
]

app = FastAPI()

# ... (existing GET endpoints)
```

**Step 3: Update GET Endpoints to Use `BandWithID`**
Modify your existing GET endpoints to use `BandWithID` as the `response_model`.

```python
# main.py
@app.get('/bands', response_model=list[BandWithID])
async def get_bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool = False
) -> list[BandWithID]:
    bands_list = [BandWithID(**band) for band in bands_data]

    if genre:
        bands_list = [
            band for band in bands_list if band.genre.lower() == genre.value]

    if has_albums:
        bands_list = [band for band in bands_list if len(band.albums) > 0]

    return bands_list


@app.get('/bands/{band_id}', response_model=BandWithID, status_code=200)
async def get_band(band_id: int) -> BandWithID:
    band = next(
        (BandWithID(**band) for band in bands_data if band['id'] == band_id),
        None
    )

    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band
```

---

**Step 4: Create a POST Endpoint**
Define a new POST endpoint at `/bands` that accepts `BandCreate` as the request body and returns `BandWithID`.

```python
# main.py
@app.post('/bands', response_model=BandWithID)
async def create_band(band_data: BandCreate):
    generated_id = bands_data[-1]['id'] + 1
    new_band = BandWithID(id=generated_id, **band_data.model_dump())
    bands_data.append(new_band.model_dump())

    return new_band
```

**Step 5: Test the POST Endpoint with REST Client**
Create a file named `api.http` (or any name with the `.http` extension) and define a POST request to test the new endpoint. Also can use `curl` or the Swagger documentation to test your endpoints.

```shell
curl -X 'POST' -i \
  'http://127.0.0.1:8000/bands' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Boards of Canada",
  "genre": "electronic",
  "albums": [
    {"title": "Tomorrows Harvest", "release_date": "1999-01-12"}
  ]
}'
```

**Step 6: Observe API Documentation**
Navigate to `/docs` on your FastAPI application URL (e.g., `http://localhost:8000/docs`) to see the automatically generated API documentation. The POST `/bands` endpoint will now be documented, showing the expected request body schema based on the `BandCreate` model and the response schema based on the `BandWithID` model.

**Step 7: Define an Enum for Genre Choices**
In `schemas.py`, create a `GenreChoices` enum to limit the possible values for the `genre` field. This was already included in the `schemas.py` code block in Step 1.

**Step 8: Implement a Pre-Validator for Genre**
In the `BandCreate` model within `schemas.py`, add a `@validator` with `pre=True` to convert the input `genre` to title case before validation. This was also included in the `schemas.py` code block in Step 1. This ensures that even if the client sends the genre in lowercase or uppercase, it will be converted to title case before being validated against the `GenreChoices` enum.
