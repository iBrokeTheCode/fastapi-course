# Modular Project Structure With FastAPI Routers

This tutorial focuses on restructuring a FastAPI project to make it more modular and scalable using **FastAPI routers**. Building upon a simple CRUD API developed in previous parts, the objective is to split API endpoints and related logic into separate modules based on functionality, such as books. This modular approach helps manage project growth by organizing code into logical units, enhancing maintainability and clarity. FastAPI routers facilitate this by allowing the grouping of related API endpoints which can then be included in the main application instance under a specific **prefix**.

## 1. Core Concepts

- **FastAPI Routers**: Objects provided by FastAPI that are similar to the main `FastAPI` app instance. They are used to group related API endpoints into separate modules. Routers can access HTTP methods and other features available on the main app instance.
- **Modular Project Structure**: An organizational strategy where a project's code is divided into independent and interchangeable modules. This improves the project's scalability, maintainability, and readability as it grows.
- **Packages and Modules**: In Python, a **package** is a directory containing a `__init__.py` file, used to organize related modules. A **module** is a single Python file. Grouping logic (like data models, schemas, and routes for a specific domain, e.g., books) into packages keeps the codebase organized.
- **Prefix**: A URL segment defined when including a router in the main app. All endpoints defined within that router will be accessed relative to this prefix. For example, a router with a prefix `/books` will make an endpoint defined as `/` within the router accessible at `/books/`. Prefixes can also include API version information, such as `/api/v1/books`.
- **App Instance**: The main `FastAPI()` object that represents the web application. Routers are **included** in the main app instance to make their endpoints part of the application's API. The app instance can also define global API metadata like **title**, **description**, and **version**.
- **`__init__.py`**: A special file that signals to Python that a directory should be treated as a package. Placing the main `FastAPI` app instance in `src/__init__.py` makes the `src` directory the main entry point for the application.
- **`requirements.txt`**: A standard file used to list the project's dependencies and their specific versions. This ensures that anyone setting up the project can install the exact same environment, making the project reproducible. It can be generated using `pip freeze > requirements.txt`.

## 2. Resources

- [Source Tutorial](https://youtu.be/_kNyYIFSOFU?si=XxqrbnobdraLKLu8)

## 3. Practical Steps: Hands-on Guide

1.  **Separate Data and Models**:

    - Create a new Python file `book_data.py`.
    - Cut the in-memory book data list from the main file and paste it into `book_data.py`.
    - Create a new Python file `schemas.py`.
    - Cut the Pydantic **BaseModel** definitions (e.g., `Book`, `BookUpdate`) and paste them into `schemas.py`.
    - Ensure necessary imports (e.g., `BaseModel` in `schemas.py`, the book data list in `book_data.py`, Pydantic models in `book_data.py` if needed) are present in their new files.

2.  **Create Source Directory and Packages**:

    - Create a new directory named `src` at the root of the project.
    - Create an `__init__.py` file inside `src` to mark it as a package.
    - Create a new directory named `books` inside `src` (e.g., `src/books`).
    - Create an `__init__.py` file inside `src/books` to mark it as a package.

3.  **Move Data and Schema Files into Package**:

    - Move `book_data.py` and `schemas.py` into the `src/books/` directory. The directory structure should start looking like this:
      ```
      .
      ├── src/
      │   ├── __init__.py
      │   └── books/
      │       ├── __init__.py
      │       ├── book_data.py
      │       └── schemas.py
      └── main.py (to be removed later)
      ```

4.  **Create Routes File and Move Endpoints**:

    - Create a new Python file named `routes.py` inside the `src/books/` directory.
    - Cut all the API endpoint functions (those decorated with `@app.`) from the original `main.py` file and paste them into `src/books/routes.py`.

5.  **Implement FastAPI Router**:

    - In `src/books/routes.py`, import `APIRouter` from `fastapi`.
    - Create an instance of `APIRouter`. The tutorial names it `book_router`:

      ```python
      from fastapi import APIRouter

      book_router = APIRouter()
      ```

    - Replace the `@app.` decorator with `@book_router.` for all endpoint functions in `src/books/routes.py`. For example, change `@app.get("/books")` to `@book_router.get("/")` (adjusting path relative to future prefix, see step 8).
    - Import necessary modules and objects used by the endpoints into `src/books/routes.py`, such as `List` from `typing`, `HTTPException` and `status` from `fastapi`, and the models (`Book`, `BookUpdate`) and data (`books`) from within the `books` package (e.g., `from .schemas import Book, BookUpdate`, `from .book_data import books`).

6.  **Move Main App Instance**:

    - Delete the original `main.py` file.
    - In `src/__init__.py`, import the `FastAPI` class and create the main app instance:

      ```python
      from fastapi import FastAPI

      app = FastAPI()
      ```

7.  **Include the Router in the App**:

    - In `src/__init__.py`, import the `book_router` from its location within the package structure:
      ```python
      from source.books.routes import book_router
      ```
    - Include the `book_router` in the main `app` instance using `app.include_router()`:
      ```python
      app.include_router(book_router)
      ```

8.  **Define Router Prefix and Adjust Endpoint Paths**:

    - When including the router, specify the `prefix` attribute to define the base path for all endpoints in the router. For example, to access book endpoints under `/books`, include the router like this:
      ```python
      app.include_router(book_router, prefix="/books")
      ```
    - Adjust the paths defined on the `@book_router.` decorators in `src/books/routes.py`. If the prefix is `/books`, an endpoint previously at `/books/{book_id}` should now be at `/{book_id}` within the router file. An endpoint previously at `/books` should now be at `/`.

9.  **Add API Versioning (Optional)**:

    - Define a version string, e.g., `version = "v1"`.
    - Include the version and a base API path in the prefix using an f-string when including the router:
      ```python
      version = "v1" # or defined elsewhere
      app.include_router(book_router, prefix=f"/api/{version}/books")
      ```
    - The book endpoints will now be accessible under paths like `/api/v1/books/` and `/api/v1/books/{book_id}`.

10. **Add API Metadata (Optional)**:

    - Pass arguments like `title`, `description`, and `version` to the `FastAPI` instance in `src/__init__.py`:
      ```python
      app = FastAPI(
          title="Bookly",
          description="A book review web service",
          version="v1"
      )
      # ... include_router calls below
      ```
    - Tags can also be added to the router inclusion:
      ```python
      app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
      ```
    - These details will be visible in the automatically generated API documentation (Swagger UI).

11. **Create `requirements.txt`**:

    - Open a terminal in the project's virtual environment.
    - Run the command to generate the file:
      ```bash
      pip freeze > requirements.txt
      ```

12. **Run the Application**:

    - Run the FastAPI development server, pointing to the main app instance within the `src` package:
      ```bash
      fastapi dev src.__init__:app
      # Or as shown in tutorial:
      # fastapi dev src
      ```
    - FastAPI will now use the `src` directory as the entry point and find the app instance in `src/__init__.py`.

13. **Test Endpoints**:
    - Access the API endpoints using the defined prefix and paths, e.g., make a GET request to `/api/v1/books/` to retrieve all books. Endpoints like get by ID, update, and delete will use paths like `/api/v1/books/{book_id}` relative to the new prefix.

The final project structure after these steps will resemble:

```
.
├── src/
│   ├── __init__.py  (Contains FastAPI app instance, router inclusions, global metadata)
│   └── books/
│       ├── __init__.py
│       ├── book_data.py (Contains book data)
│       ├── routes.py    (Contains FastAPI router instance and book-specific endpoints)
│       └── schemas.py   (Contains Pydantic models for books)
└── requirements.txt (Lists project dependencies)
```

This structure allows adding new features (e.g., users, authentication) by creating new packages (e.g., `src/users/`) alongside `src/books/`, maintaining organization and modularity.
