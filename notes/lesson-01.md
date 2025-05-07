# Web Server Basics (Path & Query Params, Request Body, Headers)

This tutorial focuses on creating a simple web server using **FastAPI**. It covers fundamental concepts for building APIs, including defining endpoints for different **HTTP methods** like GET and POST. The tutorial explains how to send data to the server using **path parameters** and **query parameters**, including making query parameters optional. It also demonstrates handling complex data input using a **request body** with **Pydantic models**, accessing **request headers**, and setting **response status codes**. The aim is to equip learners with the basic building blocks for creating more sophisticated APIs beyond simple CRUD operations.

## 1. Core Concepts

- **FastAPI Application Instance:** Every FastAPI application needs a main `app` instance. This instance is created by calling the `FastAPI` class after importing it. The `app` variable serves as the entry point to the application and provides access to features like creating middleware, routes, and handling HTTP methods.
- **API Endpoint/Path:** An API endpoint is the specific path or URL on which a request is made to expect a response from the web server.
- **HTTP Methods:** These are actions performed on a resource, such as **GET** (retrieve data), **POST** (create data), **PATCH** (partially update data), **PUT** (update data), and **DELETE** (remove data). These methods are accessed on the `app` instance.
- **Async Functions (Coroutines):** Functions defined with `async def` are asynchronous and are called coroutines. These functions are triggered when a specific path or endpoint is accessed.
- **Web Server Running Modes:** FastAPI applications can be run in **development mode** using `fastapi dev` or **production mode** using `fastapi run`. Development mode includes features like server reloading when changes are made. Production mode runs without reloading and is similar to how the app would run in a production environment.
- **Path Parameters:** A **dynamic variable** passed within the URL path. They are defined using bracket syntax `{variable_name}` within the path string when defining the endpoint. They are useful for identifying specific resources or passing dynamic data required for an action.
- **Query Parameters:** **Key-value pairs** sent to the server, typically appearing after a question mark `?` in the URL, separated by ampersands `&`. In FastAPI, any parameter defined in the path handler function that is _not_ defined in the URL path is treated as a query parameter.
- **Mandatory vs. Optional Query Parameters:** By default, parameters in the path handler function are mandatory query parameters if not in the path. An `Unprocessable Entity` error may occur if a required query parameter is missing. Query parameters can be made optional and given default values.
- **Optional Query Parameters using `typing.Optional`:** To make a query parameter optional, you can use the `Optional` class imported from Python's built-in `typing` module. Combining `Optional[DataType]` with a default value (like `None` or a specific value) makes the parameter optional.
- **Request Body:** A way to send data to the server, often used for creating or updating resources. This is typically used with methods like POST, PUT, and PATCH. Data sent in the request body needs to be validated.
- **Serialization Model (Pydantic `BaseModel`):** A model, typically created using Pydantic's `BaseModel`, used for validating data sent to or from the server. It defines the expected fields and their types. By defining a parameter in the path handler function with a Pydantic model type, FastAPI automatically validates the incoming request body against this model.
- **Headers:** Information about the request or response, sent as key-value pairs. Request headers provide details about the client, data format, etc.. FastAPI allows accessing request headers using the `Header` function, typically using the lowercase name of the header.
- **Status Codes:** Standard three-digit codes returned by the server indicating the result of a request (e.g., 200 OK, 201 Created, 404 Not Found, 500 Internal Server Error). FastAPI allows customizing the status code returned by an endpoint.

## 2. Resources

- [Source Tutorial](https://youtu.be/7DQEQPlBNVM?si=9cYpSUZkR-LkRFNt)
- [FastAPI Installation and First Steps](./bug_bytes/lesson-01.md)
- [Lesson Source Code](../src/lesson-01/)

## 3. Practical Steps: Hands-on Guide

> [!IMPORTANT]
>
> - Install FastAPI: `poetry add "fastapi[standard]"`.
> - Run project: `fastapi dev main.py`.

1.  **Create the main application file:**

    - Create a new file named `main.py`.
    - Import the `FastAPI` class: `from fastapi import FastAPI`.
    - Create the FastAPI application instance: `app = FastAPI()`.

    ```python
    # main.py
    from fastapi import FastAPI

    app = FastAPI()
    ```

2.  **Define a simple GET endpoint for the root path:**

    - Use the `@app.get("/")` decorator, specifying the HTTP method (`get`) and the path (`/`).
    - Define an `async def` function (e.g., `read_root`) below the decorator.
    - This function will be triggered when a GET request is made to the root path.
    - Return a Python dictionary, which FastAPI automatically converts to JSON.

    ```python
    # main.py
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"message": "Hello World"}
    ```

3.  **Run the server in development mode:**

    - Open your terminal or command prompt.
    - Run the command: `fastapi dev main.py`.
    - FastAPI will scan for the `app` instance in `main.py` and start the server, typically on `Localhost 8000` or `127.0.0.1:8000`.

    ```bash
    fastapi dev main.py
    ```

    - Access the root endpoint in a web browser or HTTP client to see the "Hello World" message.

4.  **Define an endpoint with a Path Parameter:**

    - Define a new endpoint using a decorator like `@app.get("/greet/{name}")`. The `{name}` part defines a path parameter named `name`.
    - Define an `async def` function (e.g., `greet_name`) that accepts the path parameter (`name`) as an argument.
    - Use **type hints** to specify the expected data type for the parameter, e.g., `name: str`. You can also hint the return type, e.g., `-> dict`.
    - Use the parameter value in the function logic and return a response.

    ```python
    # main.py (add to existing code)
    @app.get("/greet/{name}")
    async def greet_name(name: str):
        return {"message": f"Hello {name}"}
    ```

    - Access this endpoint via a URL like `http://localhost:8000/greet/Jonathan`.

5.  **Define an endpoint with a Query Parameter:**

    - Define an endpoint without path parameters, e.g., `@app.get("/greet_query")` (using a different path to avoid conflict, or remove the path parameter from the previous example as shown in source). Let's use the path `/greet` as in source.
    - Define an `async def` function (e.g., `greet_user`).
    - Include parameters in the function definition that are _not_ in the path string, e.g., `name: str`. FastAPI will treat this as a mandatory query parameter.
    - If you make a request without the query parameter, FastAPI will return an **Unprocessable Entity error** indicating a missing parameter.

    ```python
    # main.py (modify the /greet endpoint)
    from fastapi import FastAPI

    # Modified greet endpoint to use query parameter 'name'
    @app.get("/greet")
    async def greet_user(name: str): # name is now a mandatory query parameter
        return {"message": f"Hello {name}"}
    ```

    - Access this endpoint via a URL like `http://localhost:8000/greet?name=Jonathan`.

6.  **Mix Path and Query Parameters:**

    ```python
    @app.get("/greet/{name}")
    async def greet_with_age(name: str, age: int): # name is path param, age is mandatory query param
        return {"message": f"Hello {name}, your age is {age}"}
    ```

    Access this endpoint via a URL like `http://localhost:8000/greet/Trevor?age=23`. Without the `age` query parameter, it would result in an Unprocessable Entity error.

7.  **Make a Query Parameter Optional with a Default Value:**

    - Import the `Optional` class: `from typing import Optional`.
    - In the function signature, use `Optional[DataType]` for the parameter and assign a default value using `=`.

    ```python
    # main.py (modify the /greet endpoint again)
    from fastapi import FastAPI
    from typing import Optional

    app = FastAPI()

    # Greet endpoint with optional query parameter 'name' and default value 'user'
    @app.get("/greet")
    async def greet_user(name: Optional[str] = "user", age: Optional[int] = 0): # Added age and made both optional with defaults
        return {"message": f"Hello {name}, your age is {age}"}
    ```

    - Now, requests to `/greet` will return "Hello user, your age is 0". Requests like `/greet?name=Trevor` will return "Hello Trevor, your age is 0". Requests like `/greet?name=Jonah&age=23` will return "Hello Jonah, your age is 23".

8.  **Define a POST endpoint with a Request Body:**

    - Import `BaseModel` from `pydantic`: `from pydantic import BaseModel`.
    - Define a Pydantic model class that inherits from `BaseModel`. Define the required fields and their types.

    ```python
    from fastapi import FastAPI, Header # Add Header later
    from typing import Optional
    from pydantic import BaseModel # Import BaseModel

    app = FastAPI()

    # Define the Pydantic model for the request body
    class BookCreateModel(BaseModel):
        title: str
        author: str
    ```

    - Define a new endpoint using `@app.post("/create-book")`.
    - Define an `async def` function (e.g., `create_book`) that accepts a parameter typed with the Pydantic model, e.g., `book_data: BookCreateModel`. This parameter represents the request body.
    - Access the data from the request body using dot notation, e.g., `book_data.title`, `book_data.author`.

    ```python
    @app.post("/create-book")
    async def create_book(book_data: BookCreateModel):
        # In a real app, you would save book_data to a database
        return {
            "title": book_data.title,
            "author": book_data.author
        }
    ```

    - To test this, use an HTTP client (like **Rest Fox** mentioned in source) or use the tool from docs in `http://127.0.0.1:8000/docs`. Set the request type to **POST**, the URL to `http://localhost:8000/create-book`, and provide a **JSON request body** matching the `BookCreateModel` structure. If the JSON is missing or incorrect, FastAPI/Pydantic will return validation errors. It also provide the code to use with `curl`.

    ```shell
    curl -X 'POST' \
    'http://127.0.0.1:8000/create-book' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "title": "string",
    "author": "string"
    }'
    ```

9.  **Access Request Headers:**

    - Import the `Header` function: `from fastapi import Header`.
    - Define an endpoint, e.g., `@app.get("/get-headers")`.
    - In the function definition, include parameters for the headers you want to access. Use the parameter name (typically lowercase) to match the header name.
    - Assign `Header()` as the default value for the parameter.
    - Optionally, provide a default value (like `None`) within the `Header()` function call if the header might not be present. E.g., `accept: Optional[str] = Header(None)`.

    ```python
    # main.py (add Header import if not already there, add endpoint)
    from fastapi import FastAPI, Header
    from typing import Optional
    from pydantic import BaseModel

    app = FastAPI()

    # ... (previous endpoints) ...

    @app.get("/get-headers")
    async def get_headers(
        accept: Optional[str] = Header(None),
        content_type: Optional[str] = Header(None),
        user_agent: Optional[str] = Header(None),
        host: Optional[str] = Header(None)
    ):
        request_headers = {
            "Accept": accept,
            "Content-Type": content_type,
            "User-Agent": user_agent,
            "Host": host
        }
        return request_headers
    ```

    - Make a GET request to `http://localhost:8000/get-headers` using an HTTP client. Observe the headers returned in the response, which reflect the headers sent by the client. You can manually add custom headers in the client to see them reflected in the response.

10. **Set Custom Status Codes:**

    - In the decorator for an endpoint, add the `status_code` parameter.
    - Provide the desired HTTP status code number.

    ```python
    # main.py (modify an existing endpoint, e.g., the POST endpoint)
    @app.post("/create-book", status_code=201) # Set status code to 201 Created
    async def create_book(book_data: BookCreateModel):
        # In a real app, you would save book_data to a database
        return {
            "title": book_data.title,
            "author": book_data.author
        }
    ```

    - When making a request to this endpoint, the response will now include the specified status code (e.g., 201) instead of the default 200 for a successful POST.
