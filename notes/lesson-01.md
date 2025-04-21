# FastAPI Fundamentals: Building Your First API

## 1. Core Concepts

- **FastAPI is a modern, high-performance API framework for Python**. It is gaining popularity in the Python API development space.
- FastAPI leverages **modern Python features** such as **async capabilities** and **type hints**.
- It achieves **high performance** comparable to Node.js and Go, thanks to the underlying functionalities provided by **Starlette and Pydantic**.
- FastAPI allows for the creation of **function-based routes** using **decorators** associated with HTTP methods (e.g., GET, POST, PUT, DELETE, PATCH).
- The `@app.get()` decorator is used to define routes that handle HTTP GET requests. The path for the route is specified as an argument to the decorator.
- **Request handlers are defined as Python functions**, which can be asynchronous (`async def`). These functions can return various Python data types, which FastAPI automatically converts into appropriate HTTP responses, such as JSON for dictionaries and plain text for strings.
- **Type hinting** in the function signatures allows FastAPI to perform data validation and automatic data serialization/deserialization using Pydantic. Incorrect return types can lead to server errors. Type hints also contribute to type safety and can help in finding errors.
- FastAPI provides **automatic API documentation** out of the box using **Swagger UI** accessible at the `/docs` endpoint and **Redoc** accessible at the `/redoc` endpoint. This documentation is interactive and shows the defined endpoints, their paths, request/response details, and schemas. This is based on the **OpenAPI** specification.

## 2. Resources

- [FastAPI](https://fastapi.tiangolo.com/)
- [Install FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI Swagger Docs](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs)

## 3. Practical Steps

- **Create a Python virtual environment:** This isolates the project dependencies from the global Python installation.
  ```bash
  python -m venv venv_fastapi
  ```
- **Activate the virtual environment:** This ensures that subsequent package installations are within the created environment.
  - On Windows, navigate to the `venv_fastapi\Scripts` directory and run `activate`.
- **Install FastAPI using pip:** This command downloads and installs the core FastAPI library.
  ```bash
  pip install fastapi
  ```
- **Upgrade pip (optional but recommended):** It's a best practice to upgrade pip after creating a virtual environment.
  ```bash
  pip install --upgrade pip
  ```
- **Install Uvicorn:** Uvicorn is an **ASGI server** that is used to run the FastAPI application.
  ```bash
  pip install uvicorn
  ```
- **Create a `main.py` file:** This file will contain the FastAPI application code.
- **Import the `FastAPI` class:** This is the base object for creating a FastAPI application.
  ```python
  from fastapi import FastAPI
  ```
- **Create an instance of the `FastAPI` class:** This initializes the FastAPI application.
  ```python
  app = FastAPI()
  ```
- **Define an API route using a decorator:** Use the `@app.get()` decorator (for GET requests) followed by the route path and the function that will handle requests to that path.
  ```python
  @app.get("/")
  async def index():
      return {"hello": "world"}
  ```
- **Define another API route (example):** Demonstrating a different path and return type.
  ```python
  @app.get("/about")
  async def about():
      return "an exceptional company"
  ```
- **Run the FastAPI application using Uvicorn:** This command starts the development server. Replace `main:app` with the actual filename and the name of your FastAPI application instance if they are different. The `--reload` flag enables automatic server restarts upon code changes, which is useful for development but should not be used in production.
  ```bash
  uvicorn main:app --reload
  ```
- **Access the API endpoints in a browser:** Once the server is running, you can access the defined routes (e.g., `http://localhost:8000/` and `http://localhost:8000/about`). The responses will be automatically formatted (e.g., as JSON for dictionaries).
- **View the automatic API documentation:** Access the Swagger UI at `http://localhost:8000/docs` or the Redoc documentation at `http://localhost:8000/redoc` to explore the API.
