# FastAPI Query Parameters for Filtering

## 1. Core Concepts

- **Query Parameters:** These are key-value pairs that appear after a question mark (`?`) in a URL. They are used to pass optional data to a server. Multiple query parameters are separated by the ampersand symbol (`&`).
- **FastAPI Handling:** In FastAPI, if you define a function parameter in a path operation function that is **not included in the path itself**, FastAPI automatically interprets it as a query parameter.
- **Type Hinting and Validation:** When you declare query parameters as arguments in your FastAPI handler functions with Python type hints, FastAPI will automatically **convert the incoming data to that type and validate it**. This includes leveraging Pydantic for data validation. You can even use Python's `enum` class to define a set of allowed values for a query parameter, providing built-in validation.
- **Optional Parameters:** By providing a **default value** to a query parameter in the function definition (e.g., `genre: GenreURLChoices | None = None`), you make it **optional**. If the parameter is not present in the URL, it will take its default value. If no default value is provided, FastAPI expects the query parameter to be present.
- **Accessing Query Parameters:** The values of the query parameters are directly passed as arguments to your FastAPI handler function.
- **Filtering Logic:** You can use the values of the query parameters within your handler function to **filter data** before returning a response.
- **Multiple Query Parameters:** You can define multiple query parameters in your FastAPI function. These parameters can be used in conjunction (acting as an "and" condition in the example) to further refine the filtering of data.
- **Swagger Documentation:** FastAPI automatically documents your query parameters in the interactive Swagger UI, including their names, types, and default values. This helps in understanding how to interact with your API.

## 2. Resources

- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)

## 3. Practical Steps:

1.  **Define a function parameter in your FastAPI path operation function that is not part of the path.** For example, instead of a path like `/bands/{genre}`, modify it to `/bands` and add a `genre` parameter to the function:

    ```python
    from typing import List, Optional
    from enum import Enum
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class GenreURLChoices(str, Enum):
        rock = "rock"
        electronic = "electronic"

    class Band(BaseModel):
        name: str
        genre: GenreURLChoices
        albums: List[str] = []

    bands = [
        {"name": "The Kinks", "genre": "rock", "albums": []},
        {"name": "New Order", "genre": "electronic", "albums": ["Power, Corruption & Lies"]},
        {"name": "The Cure", "genre": "rock", "albums": ["Disintegration"]},
    ]

    @app.get("/bands")
    async def list_bands(genre: Optional[GenreURLChoices] = None):
        if genre:
            return [band for band in bands if band["genre"] == genre]
        return bands
    ```

    In this lesson, the `/genres/{genre_name}` endpoint was removed, and the `genre` was added as a query parameter to the `/bands` endpoint.

2.  **FastAPI interprets function parameters not in the path as query parameters.** In the code above, `genre` is not part of the `/bands` path, so FastAPI understands that it should be passed as a query parameter in the URL (e.g., `/bands?genre=rock`).

3.  **Add type hints to enable automatic type conversion and validation.** In the `list_bands` function, `genre: Optional[GenreURLChoices] = None` specifies that the `genre` query parameter should be of the `GenreURLChoices` enum type or `None`. This ensures that if a value is provided for `genre` in the URL, it will be validated against the allowed values in the `GenreURLChoices` enum.

4.  **Make query parameters optional by providing a default value.** Setting `genre: Optional[GenreURLChoices] = None` makes the `genre` query parameter optional. If the user accesses `/bands` without any query parameters, the `genre` argument in the `list_bands` function will default to `None`, and all bands will be returned. Without a default value, accessing `/bands` would result in an error, as FastAPI would expect the `genre` parameter to be present.

5.  **Access the query parameter within the function to implement filtering logic.** Inside the `list_bands` function, the value of the `genre` query parameter is available through the `genre` argument. The code then checks if a `genre` was provided and filters the `bands` list accordingly.

6.  **Implement filtering based on the query parameter's value.**

    ```python
    @app.get("/bands")
    async def list_bands(genre: Optional[GenreURLChoices] = None):
        if genre:
            return [band for band in bands if band["genre"] == genre] # Filtering based on genre
        return bands
    ```

    This code snippet demonstrates how the `genre` query parameter is used to filter the list of bands.

7.  **Add multiple query parameters by defining additional parameters in the function signature with their respective types and optional default values.** For example, to filter bands by genre and whether they have albums:

    ```python
    from typing import List, Optional
    from enum import Enum
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class GenreURLChoices(str, Enum):
        rock = "rock"
        electronic = "electronic"

    class Band(BaseModel):
        name: str
        genre: GenreURLChoices
        albums: List[str] = []

    bands = [
        {"name": "The Kinks", "genre": "rock", "albums": []},
        {"name": "New Order", "genre": "electronic", "albums": ["Power, Corruption & Lies"]},
        {"name": "The Cure", "genre": "rock", "albums": ["Disintegration"]},
    ]

    @app.get("/bands")
    async def list_bands(genre: Optional[GenreURLChoices] = None, has_albums: bool = False):
        band_list = [Band(**band) for band in bands]
        if genre:
            band_list = [band for band in band_list if band.genre == genre]
        if has_albums:
            band_list = [band for band in band_list if len(band.albums) > 0]
        return band_list
    ```

    Here, `has_albums` is another query parameter of type `bool` with a default value of `False`. The filtering logic is then extended to consider this parameter as well. Requests like `/bands?genre=electronic&has_albums=true` would filter for electronic bands that have albums. This demonstrates an "and" condition as both criteria must be met after each filtering step.

8.  **Observe the automatic updates in the Swagger documentation.** When you run your FastAPI application and navigate to `/docs`, you will see that the `/bands` endpoint now lists `genre` and `has_albums` as query parameters, along with their types and default values. This documentation is automatically generated based on the type hints and default values defined in your function signature.
