# FastAPI Path Parameters and Data Validation

## 1. Core Concepts

- **Path Parameters:** FastAPI allows you to define dynamic parts in your API endpoint paths, known as path parameters. These are declared by enclosing a variable name in curly braces within the path defined in the `@app.get()`, `@app.post()`, etc., decorator. For example, `/items/{item_id}` defines a path parameter named `item_id`.

- **Retrieving Single Resources:** A common REST API pattern for fetching a specific resource is to include its identifier as a path parameter after the entity name (e.g., `/bands/{band_id}`).

- **Type Hinting for Validation:** By providing Python type hints for the path parameter in the handler function, FastAPI automatically performs data validation. If the value passed in the URL does not match the expected type, FastAPI will return an HTTP 422 Unprocessable Entity error. This also adds type information to the generated Swagger documentation.

- **HTTPException for Error Handling:** FastAPI provides the `HTTPException` class, which allows you to raise custom HTTP error responses with specific status codes and details. This is useful for scenarios like returning a 404 Not Found error when a requested resource does not exist.

- **Customizing Response Status Codes:** The default successful response status code for a GET request is 200 OK. You can override this by passing a `status_code` argument to the decorator. This will also be reflected in the Swagger documentation.

- **Limiting Values with Python Enums:** To restrict the possible values of a path parameter to a predefined set, you can use Python's `enum` module. By type-hinting the path parameter with an Enum, FastAPI will automatically validate that the provided value is one of the allowed enum members, returning a 422 error if it's not. This also clearly documents the acceptable values in the Swagger UI.

- **Accessing Enum Values:** When using enums for path parameters, you can access the underlying value of an enum member within the handler function using the `.value` attribute.

- **Swagger Documentation Integration:** FastAPI seamlessly integrates with Swagger UI and automatically updates the API documentation based on the defined path parameters, type hints, and enums. This includes information about required path parameters, their expected types, and allowed values (for enums).

## 2. Resources

- [FastAPI Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Litestar for Python API Development / Pydantic Model Integration](https://youtu.be/lK234IODJ9A?si=V5aLmapAZIbxTa8M)

## 3. Practical Steps

1.  **Import `FastAPI`:** Begin by importing the `FastAPI` class from the `fastapi` library.

    ```python
    from fastapi import FastAPI

    app = FastAPI()
    ```

2.  **Create an endpoint to return a list of data:** Define a route using the `@app.get()` decorator and a handler function that returns a list (e.g., a list of dictionaries). Specify the return type using type hints.

    ```python
    from fastapi import FastAPI
    from typing import List

    app = FastAPI()

    bands_data = [
        {"id": 1, "name": "The Kinks", "genre": "Rock"},
        {"id": 2, "name": "FX Twin", "genre": "Electronic"},
        {"id": 3, "name": "Black Sabbath", "genre": "Metal"},
        {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
    ]

    @app.get("/bands")
    def get_bands() -> List[dict]:
        return bands_data
    ```

3.  **Create an endpoint with a path parameter:** Define a route where a part of the path is enclosed in curly braces `{}`. This denotes a path parameter. The name inside the braces will be used as an argument in your handler function.

    ```python
    @app.get("/bands/{band_id}")
    def get_band(band_id):
        # band_id will contain the value from the URL
        return {"band_id": band_id}
    ```

4.  **Use type hints for path parameter validation:** Add a type hint to the path parameter in the handler function. FastAPI will automatically attempt to convert and validate the input based on this type. If the validation fails, a 422 error is returned.

    ```python
    @app.get("/bands/{band_id}")
    def get_band(band_id: int):
        # band_id is now expected to be an integer
        # Logic to find the band by ID would go here
        return {"band_id": band_id}
    ```

5.  **Implement logic to return a single item or a 404 error:** Use the path parameter to identify and retrieve a specific item. If the item is not found, raise an `HTTPException` with a status code of 404. First, import `HTTPException`:

    ```python
    from fastapi import FastAPI, HTTPException
    from typing import List

    app = FastAPI()

    bands_data = [
        {"id": 1, "name": "The Kinks", "genre": "Rock"},
        {"id": 2, "name": "FX Twin", "genre": "Electronic"},
        {"id": 3, "name": "Black Sabbath", "genre": "Metal"},
        {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
    ]

    @app.get("/bands/{band_id}")
    def get_band(band_id: int):
        band = next((band for band in bands_data if band["id"] == band_id), None)
        if band is None:
            raise HTTPException(status_code=404, detail="Band not found")
        return band
    ```

6.  **Define an Enum for limiting path parameter values:** Import `Enum` from the `enum` module and create a class that inherits from `str` and `Enum`. Define the allowed values as members of this class.

    ```python
    from enum import Enum

    class GenreURLChoices(str, Enum):
        rock = "rock"
        electronic = "electronic"
        metal = "metal"
        hip_hop = "hip-hop"
    ```

7.  **Use the Enum as a type hint for a path parameter:** In your route definition, type-hint the path parameter with the Enum class you created. FastAPI will now only accept values that are members of this Enum.

    ```python
    from fastapi import FastAPI
    from typing import List
    from enum import Enum

    app = FastAPI()

    bands_data = [
        {"id": 1, "name": "The Kinks", "genre": "Rock"},
        {"id": 2, "name": "FX Twin", "genre": "Electronic"},
        {"id": 3, "name": "Black Sabbath", "genre": "Metal"},
        {"id": 4, "name": "Run-DMC", "genre": "Hip-Hop"},
    ]

    class GenreURLChoices(str, Enum):
        rock = "rock"
        electronic = "electronic"
        metal = "metal"
        hip_hop = "hip-hop"

    @app.get("/bands/genre/{genre}")
    def get_bands_by_genre(genre: GenreURLChoices) -> List[dict]:
        matching_bands = [band for band in bands_data if band["genre"].lower() == genre.value]
        return matching_bands
    ```

8.  **Run the FastAPI application:** Use a Uvicorn server to run your FastAPI application. The `-reload` flag allows for automatic reloading upon code changes.

    ```bash
    uvicorn main:app --reload
    ```

9.  **Explore the documentation:** Access the automatically generated Swagger UI at `/docs` to see your API endpoints, including the path parameters, their types, and the allowed values for enums.

By following these steps, you can effectively use path parameters in FastAPI, leverage type hints for automatic data validation, and enforce specific value constraints using Python enums, leading to more robust and well-documented APIs.
