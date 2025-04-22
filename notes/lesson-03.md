# FastAPI and Pydantic - Model Classes and Nested Models

## 1. Core Concepts

This lesson highlights that **Pydantic** is a widely used Python library for **data validation**. Pydantic enables the creation of **model classes** that inherit from its `BaseModel`. These classes define the **structure of data** by specifying fields with **Python type hints**. This is particularly useful for **validating data coming into an API**, such as the request body. FastAPI is identified as one of the most common use cases for Pydantic.

By using Pydantic models as return type hints in FastAPI endpoints, **automatic data validation** is performed on the returned data. If the data does not conform to the defined model, it will be rejected. Furthermore, Pydantic models enhance **API documentation** by providing the schema of the expected response, including field names, data types, and sample values. FastAPI seamlessly **converts Pydantic model instances to JSON** responses.

The lesson also explains **nested Pydantic models**, which allow for representing complex data structures where one model can contain other models as fields (e.g., a `Band` model containing a list of `Album` models). When working with nested models, any **validations defined in the child model are also applied** to the nested data within the parent model.

## 2. Resources

- [FastAPI + Pydantic](https://fastapi.tiangolo.com/python-types/#pydantic-models)
- [Pydanctic Documentation](https://docs.pydantic.dev/latest/)
- [Pydantic Tutorial](https://youtube.com/playlist?list=PL-2EBeDYMIbQQGc6kiBSm81XspmwVuk-t&si=-tzoVuCkJuR5uawr)

## 3. Practical Steps

1.  **Create a `schemas.py` file:** It is good practice to create a dedicated file, often named `schemas.py`, to house all the Pydantic schema (model) classes used in the FastAPI application.

2.  **Import `BaseModel` from Pydantic:** In your `schemas.py` file, import the `BaseModel` class from the `pydantic` library. This is the base class that your data models will inherit from.

    ```python
    from pydantic import BaseModel
    ```

3.  **Define a Pydantic model class:** Create a class that inherits from `BaseModel`. Within this class, define the fields your data structure will have, using Python type hints to specify the expected data type for each field.

    ```python
    class Band(BaseModel):
        id: int
        name: str
        genre: str
    ```

4.  **Import the Pydantic model in `main.py`:** In your main FastAPI application file (e.g., `main.py`), import the Pydantic model class that you defined in `schemas.py`.

    ```python
    from schemas import Band
    ```

5.  **Use the Pydantic model as a return type hint in FastAPI endpoints:** In your FastAPI route functions, specify the Pydantic model (or a list of models using `typing.List`) as the `response_model`. FastAPI will then automatically try to serialize the returned data into this model and validate it.

    ```python
    from typing import List
    from fastapi import FastAPI

    app = FastAPI()
    bands_data = [
        {"id": 1, "name": "Black Sabbath", "genre": "Heavy Metal"},
        {"id": 2, "name": "Led Zeppelin", "genre": "Hard Rock"}
    ]

    @app.get("/bands", response_model=List[Band])
    async def read_bands():
        return [Band(**band) for band in bands_data]

    @app.get("/bands/{band_id}", response_model=Band)
    async def read_band(band_id: int):
        band = next((band for band in bands_data if band["id"] == band_id), None)
        return Band(**band) if band else None
    ```

    **Explanation:** The `response_model=List[Band]` in the `/bands` endpoint tells FastAPI that this endpoint should return a list of `Band` objects. Similarly, `response_model=Band` in the `/bands/{band_id}` endpoint indicates that a single `Band` object should be returned. The `Band(**band)` syntax unpacks the dictionary `band` and passes its key-value pairs as arguments to the `Band` model's constructor, creating an instance of the `Band` Pydantic model.

6.  **Define nested Pydantic models:** To represent nested data, create separate Pydantic model classes for each level of nesting. For example, to represent albums within a band, you would create an `Album` model. Remember to import necessary types like `date` from the `datetime` module if needed.

    ```python
    from datetime import date
    from typing import List
    from pydantic import BaseModel

    class Album(BaseModel):
        title: str
        release_date: date

    class Band(BaseModel):
        id: int
        name: str
        genre: str
        albums: List[Album] = []
    ```

7.  **Include the nested model as a field in the parent model:** In the parent model, define a field whose type is a list (or a single instance) of the nested model. You may also set a default value for this field. Ensure that the nested model is defined before it is referenced in the parent model to avoid errors.

    ```python
    from datetime import date
    from typing import List
    from pydantic import BaseModel

    class Album(BaseModel):
        title: str
        release_date: date

    class Band(BaseModel):
        id: int
        name: str
        genre: str
        albums: List[Album] = []
    ```

8.  **Update the data to include nested structures:** Modify the data that your FastAPI application returns to match the structure defined by your nested Pydantic models.

    ```python
    bands_data_with_albums = [
        {
            "id": 1,
            "name": "Black Sabbath",
            "genre": "Heavy Metal",
            "albums": [{"title": "Master of Reality", "release_date": "1971-07-21"}]
        },
        {
            "id": 2,
            "name": "Led Zeppelin",
            "genre": "Hard Rock",
            "albums": []
        }
    ]

    @app.get("/bands", response_model=List[Band])
    async def read_bands_with_albums():
        return [Band(**band) for band in bands_data_with_albums]

    @app.get("/bands/{band_id}", response_model=Band)
    async def read_band_with_albums(band_id: int):
        band = next((band for band in bands_data_with_albums if band["id"] == band_id), None)
        return Band(**band) if band else None
    ```

    **Explanation:** The `bands_data_with_albums` now includes an "albums" key for each band, containing a list of dictionaries that conform to the structure defined in the `Album` Pydantic model. When the FastAPI endpoint returns this data with the `response_model` set to `Band`, Pydantic will automatically validate and serialize the nested album data as well. If the data within the "albums" list does not match the `Album` model's definition (e.g., incorrect field names or data types), a validation error will occur.
