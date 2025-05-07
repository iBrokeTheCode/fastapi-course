# Build a CRUD REST API (Response Models, Validation, And Exceptions)

This lesson details the process of building a **CRUD REST API** using the **FastAPI** framework, focusing on manipulating book data stored temporarily in a Python list acting as an **in-memory database**. Building upon previous knowledge of setting up a simple web server and API endpoints, this guide demonstrates how to implement the four core CRUD operations: **Create**, **Read**, **Update**, and **Delete**. It covers defining **API endpoints** and mapping them to appropriate **HTTP methods**, handling path parameters for specific resources, using **Pydantic models** for data validation and serialization for both request bodies and response models, and implementing basic error handling using **HTTP exceptions** with appropriate **status codes**. The objective is to provide a practical, hands-on guide to building a functional, though simple, CRUD API.

## 1. Core Concepts

- **CRUD:** An acronym representing the four basic operations used when manipulating data in a data storage application: **Create**, **Read**, **Update**, and **Delete**.
- **REST API:** An architectural style for designing networked applications. A **REST API** allows systems to communicate over HTTP using standard operations (CRUD) mapped to HTTP methods like GET, POST, PUT, PATCH, and DELETE.
- **Resource:** The data that an API provides or allows manipulation of. In this lesson, **book data** is the resource being manipulated.
- **API Endpoint:** A specific URL where an API receives requests. Examples in this lesson include `/books` and `/book/{book_id}`.
- **HTTP Methods:** Verbs used to indicate the desired action to be performed on a resource. The primary methods discussed for CRUD are **GET** (Read), **POST** (Create), **PATCH** (Update for partial updates), and **DELETE** (Delete).
- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **In-Memory Database:** Data storage that resides solely in the computer's RAM and is lost when the application stops. A simple Python list is used as a temporary **in-memory database** for book data in this lesson.
- **Persistent Data Store:** Data storage that persists beyond the life of the application, such as a traditional database like PostgreSQL.
- **Path Parameters:** Variables captured from the URL path, often used to identify a specific resource, such as `{book_id}` in `/book/{book_id}`.
- **Pydantic Models:** Data validation and settings management using Python type hints. In FastAPI, **Pydantic models** are used to define the structure and data types of **request bodies** (data sent from the client) and **response models** (data returned by the API). They provide automatic data validation.
- **Request Body:** The data sent by the client in the body of an HTTP request, typically in JSON format. Pydantic models define the expected structure of this data.
- **Response Model (`response_model`):** An attribute used in FastAPI endpoint decorators (`@app.get`, etc.) to define the expected structure of the data returned by the endpoint, validated by Pydantic.
- **`model_dump` method:** A method available on Pydantic model objects to convert the model data into a standard Python dictionary.
- **Status Codes:** Standard three-digit numerical codes in HTTP responses indicating the status of the request (e.g., 200 OK, 201 Created, 204 No Content, 404 Not Found).
- **`fastapi.status` module:** A module provided by FastAPI that contains constants for standard HTTP **status codes**, making them easier to use.
- **HTTP Exception (`HTTPException`):** A class in FastAPI (`fastapi.exceptions.HTTPException`) used to raise standard HTTP errors within API endpoints. When raised, FastAPI handles returning the appropriate status code and error details to the client.

## 2. Resources

- [Source Tutorial](https://youtu.be/W8D-crU5-Fc?si=NdkasvnGXs9A1P0H)

## 3. Practical Steps: Hands-on Guide

1.  **Set up FastAPI and In-Memory Data:**

    - Import the `FastAPI` class and create an instance.
    - Define a Python list to act as the in-memory book database.
    - Import `BaseModel` from `pydantic` and `List` from `typing`.

    ```python
    from fastapi import FastAPI, status, HTTPException # Import necessary classes
    from pydantic import BaseModel
    from typing import List

    app = FastAPI()

    # Simple in-memory database (Python List)
    books = [
        {"id": 1, "title": "Title One", "author": "Author One", "publisher": "Publisher One", "publish_date": "2021-01-01", "page_count": 100, "language": "English"},
        # ... other book dictionaries ...
    ]
    ```

2.  **Define Pydantic Models for Data Validation and Serialization:**

    - Create a `Book` class inheriting from `BaseModel` to define the structure and types of a complete book resource.

    ```python
    class Book(BaseModel):
        id: int
        title: str
        author: str
        publisher: str
        publish_date: str # Or potentially datetime later
        page_count: int
        language: str
    ```

    - Create a `BookUpdateModel` class inheriting from `BaseModel` for defining the structure of data accepted for updating a book, omitting fields like `id` and `publish_date` if they are not intended to be updated via this specific endpoint.

    ```python
    class BookUpdateModel(BaseModel):
        title: str
        author: str
        publisher: str
        page_count: int
        language: str
    ```

3.  **Implement the "Read All" (GET) Endpoint:**

    - Define an endpoint using `@app.get("/books")`.
    - Define a handler function (e.g., `get_all_books`).
    - Specify the `response_model` attribute using `List[Book]` to indicate that the endpoint returns a list of `Book` model objects.
    - Inside the function, simply return the `books` list.

    ```python
    @app.get("/books", response_model=List[Book])
    def get_all_books():
        return books
    ```

4.  **Implement the "Create" (POST) Endpoint:**

    - Define an endpoint using `@app.post("/books")`.
    - Define a handler function (e.g., `create_book`) that accepts the incoming book data as a parameter with a type hint of `Book` (this automatically handles validating the request body).
    - Add `status_code=status.HTTP_201_CREATED` to the decorator to indicate successful creation.
    - Convert the incoming `book_data` Pydantic model object to a dictionary using `.model_dump()`.
    - Append the resulting dictionary to the `books` list.
    - Return the newly created book dictionary.

    ```python
    @app.post("/books", status_code=status.HTTP_201_CREATED)
    def create_book(book_data: Book): # Pydantic model for request body validation
        new_book = book_data.model_dump() # Convert Pydantic model to dictionary
        books.append(new_book)
        return new_book
    ```

5.  **Implement the "Read Single" (GET by ID) Endpoint:**

    - Define an endpoint using `@app.get("/book/{book_id}")` with a **path parameter** `{book_id}`.
    - Define a handler function (e.g., `get_book`) that accepts `book_id` as an argument with a type hint (e.g., `int`).
    - Specify the `response_model` attribute using `Book` to indicate that the endpoint returns a single `Book` model object.
    - Loop through the `books` list.
    - Inside the loop, check if a book's `id` matches the provided `book_id`.
    - If a match is found, return the book dictionary.
    - If the loop finishes without finding a match, raise an `HTTPException` with `status_code=status.HTTP_404_NOT_FOUND` and a `detail` message (e.g., "Book not found").

    ```python
    @app.get("/book/{book_id}", response_model=Book)
    def get_book(book_id: int): # Path parameter
        for book in books:
            if book["id"] == book_id:
                return book
        # If book is not found after loop
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    ```

6.  **Implement the "Update" (PATCH) Endpoint:**

    - Define an endpoint using `@app.patch("/book/{book_id}")` with a **path parameter** `{book_id}`.
    - Define a handler function (e.g., `update_book`) that accepts `book_id` (int) and the update data with a type hint of `BookUpdateModel`.
    - Loop through the `books` list.
    - If a book's `id` matches the provided `book_id`:
      - Update the book's fields using the data from the `book_update_data` model (e.g., `book["title"] = book_update_data.title`).
      - Return the updated book dictionary.
    - If the loop finishes without finding a match, raise an `HTTPException` with `status_code=status.HTTP_404_NOT_FOUND` and a `detail` message ("Book not found").

    ```python
    @app.patch("/book/{book_id}")
    def update_book(book_id: int, book_update_data: BookUpdateModel):
        for book in books:
            if book["id"] == book_id:
                # Update fields from the update model
                book["title"] = book_update_data.title
                book["author"] = book_update_data.author
                book["publisher"] = book_update_data.publisher
                book["page_count"] = book_update_data.page_count
                book["language"] = book_update_data.language
                return book
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    ```

7.  **Implement the "Delete" (DELETE) Endpoint:**

    - Define an endpoint using `@app.delete("/book/{book_id}")` with a **path parameter** `{book_id}`.
    - Define a handler function (e.g., `delete_book`) that accepts `book_id` (int).
    - Add `status_code=status.HTTP_204_NO_CONTENT` to the decorator, as delete operations often return no content on success.
    - Loop through the `books` list.
    - If a book's `id` matches the provided `book_id`:
      - Remove the book dictionary from the `books` list using `books.remove(book)`.
      - Return an empty response or nothing explicitly, as the 204 status code signifies success with no content. The function can simply `pass` or `return` implicitly.
    - If the loop finishes without finding a match, raise an `HTTPException` with `status_code=status.HTTP_404_NOT_FOUND` and a `detail` message ("Book not found").

    ```python
    @app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_book(book_id: int):
        for book in books:
            if book["id"] == book_id:
                books.remove(book)
                return # Return implicitly for 204 status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    ```

8.  **Run the FastAPI Application:**

    - Save the code (e.g., as `main.py`).
    - Run the application from the terminal using `uvicorn main:app --reload` (assuming `uvicorn` is installed) or `fastapi dev main.py`. The lesson specifically uses `fastapi dev main.py`.

    ```bash
    fastapi dev main.py
    # or
    uvicorn main:app --reload
    ```

9.  **Test the Endpoints:**
    - Use a tool like Rest Fox (as shown in the lesson) or other API testing tools (like curl, Postman, Insomnia) to send requests to `http://localhost:8000/`.
    - Test GET requests to `/books` and `/book/{id}`.
    - Test POST requests to `/books` with a JSON request body.
    - Test PATCH requests to `/book/{id}` with a JSON request body containing update data.
    - Test DELETE requests to `/book/{id}`.
    - Observe the responses, including data returned, status codes (200, 201, 204), and error details (404). Note that data created/deleted is lost when the server restarts because the database is in-memory.
