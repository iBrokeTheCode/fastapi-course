# Databases With SQLModel (Connection, Lifespan Events, And Models)

This tutorial focuses on adapting a FastAPI application to use a **persistent database**, moving beyond the in-memory database (Python list). It is essential for real-world applications to use persistent storage. The tutorial specifically uses **PostgreSQL**, a widely used relational database management system. To interact with the database using Python, an **Object Relational Mapper (ORM)** is required. The video introduces **SQLModel**, an ORM that combines the power of SQLAlchemy and Pydantic, making it well-suited for FastAPI applications. SQLModel simplifies database interactions by allowing developers to use Python code instead of writing SQL queries directly. The key learning objectives include setting up database configuration using environment variables and Pydantic settings, connecting to the database using FastAPI's **lifespan events**, defining database models with SQLModel, and automatically creating database tables on application startup.

## 1. Core Concepts

**Persistent Databases vs. In-Memory Databases**
Persistent databases store data durably, meaning the data remains available even after the application stops. This contrasts with **in-memory databases**, such as a Python list, where data is lost when the application process ends. Persistent databases are crucial for real-world applications.

**Relational Databases (PostgreSQL)**
A type of database that organizes data into tables with predefined relationships. **PostgreSQL** is a popular, free, and open-source relational database management system chosen for this tutorial series. FastAPI supports various relational and non-relational databases.

**Object Relational Mapper (ORM)**
An ORM acts as a translator between an object-oriented programming language (like Python) and a relational database. It **maps objects to tables**, where Python classes represent tables and objects of those classes represent rows or records. An ORM allows developers to interact with database data using familiar Python objects and methods. Behind the scenes, it translates Python operations (like saving, deleting, updating objects) into the appropriate SQL queries that the database understands. It also handles converting Python data types to database-specific types and vice versa. ORMs simplify database interactions, reducing the need to write raw SQL.

**SQLAlchemy**
A powerful and widely used ORM solution for Python. It provides a SQL toolkit and maps Python objects to tables. While powerful, using SQLAlchemy directly with FastAPI can sometimes be complex.

**SQLModel**
An ORM created by the creator of FastAPI. It is built upon **SQLAlchemy** and **Pydantic**, combining their strengths. SQLModel classes serve as both **Pydantic models** (for data validation) and **SQLAlchemy models** (for database operations). This dual nature makes SQLModel a suitable ORM choice for FastAPI applications.

**Environment Variables (.env files) and Pydantic Settings**
**Environment variables** are used to store configuration settings that can change between environments (development, staging, production) or contain secrets like database credentials. Storing these in files like **.env** keeps them separate from the main codebase and out of version control (`.gitignore`). **Pydantic Settings** is a library built on Pydantic specifically for managing environment variables. It uses a `BaseSettings` class to define application settings. By configuring a `SettingsConfigDict` with `env_file=".env"`, it can automatically read key-value pairs from a `.env` file and make them accessible as attributes on the settings class.

**Async DB API / Async Driver (asyncpg)**
To perform database operations asynchronously in Python, an asynchronous database driver (DB API) is needed. **asyncpg** is an example of such a driver for PostgreSQL, installed via `pip install asyncpg`. The database URL format is modified to specify the async driver (e.g., `postgresql+asyncpg://`).

**Engine (Async Engine)**
In SQLAlchemy and SQLModel, the **engine** is the core object responsible for connecting to the database and managing connections. When using an async driver, an **async engine** is required. It is created using the `create_engine` function from SQLModel, providing the database URL and configuration like `echo=True`.

**`echo=True`**
An attribute passed to the `create_engine` function. When set to `True`, it enables logging of all SQL statements executed by the engine to the console, which is useful for debugging and understanding database interactions.

**Lifespan Events (FastAPI)**
A feature in FastAPI that allows code to be run specifically at the **startup** and **shutdown** of the application. This is useful for tasks like establishing a database connection when the server starts and closing it when the server stops. Lifespan events are defined using an asynchronous context manager decorated with `@asynccontextmanager` from Python's `contextlib` module. Code placed before the `yield` keyword in the decorated function runs on startup, and code after `yield` runs on shutdown.

**Context Manager (`@asynccontextmanager`)**
A decorator from Python's `contextlib` library used to define functions that can be used with an `async with` statement. For FastAPI lifespan events, it wraps an async function, allowing it to manage resources that are set up before yielding control (startup) and torn down after the `yield` (shutdown).

**Connection Object**
Represents an active connection session with the database. It is typically obtained from the engine using an `async with engine.begin() as con:` block. The `con` object is then used to execute SQL statements or ORM operations.

**`run_sync` method**
A method available on an asynchronous connection object (`con.run_sync`). It allows synchronous code to be executed safely within an asynchronous context. This is necessary, for example, to call synchronous SQLAlchemy methods like `metadata.create_all` when working with an async engine.

**SQLModel Metadata**
An object (`SQLModel.metadata`) that holds information about all database tables defined using `SQLModel` classes where `table=True`. It contains metadata about columns, primary keys, and relationships. The `metadata.create_all(engine)` method uses this information to generate and execute `CREATE TABLE` statements in the database. Note: When using an async engine, this synchronous method must be called via `await connection.run_sync(SQLModel.metadata.create_all)`.

**Database Models (SQLModel Class)**
Python classes that inherit from `SQLModel` and have the attribute `table=True`. They define the structure (schema) of a database table. Class attributes correspond to database columns. They can use Pydantic type hints and optionally the `Field` function with `sa_column` to define specific SQLAlchemy column details like types (e.g., `UUID`, `TIMESTAMP`), constraints (nullable, primary key), and default values.

**UUID (Universally Unique Identifier)**
A 128-bit number used to uniquely identify information. It is often used as a primary key in database tables because it can be generated independently and is highly unlikely to collide. Python's built-in `uuid` module can generate UUIDs (e.g., `uuid.uuid4()`). Database-specific types like PostgreSQL's `PG.UUID` are used to store them efficiently.

**DateTime and Timestamps**
Used to represent points in time. Often used for fields like `created_at` and `updated_at` to track when records were created or last modified. Python's `datetime.datetime` class represents these. Database types like PostgreSQL's `PG.TIMESTAMP` are used for storage. Default values can be set to `datetime.now` to automatically record the current time upon creation or update.

**Primary Key**
A column or set of columns in a database table that uniquely identifies each row. Primary keys enforce data integrity and are often indexed for faster retrieval. In SQLModel, the primary key is specified using `primary_key=True` within the `sa_column` definition of the field.

**Default Values**
A value that is automatically assigned to a column if no value is explicitly provided when a new row is inserted. Default values can be static values or callable functions (like `uuid.uuid4` or `datetime.now`) that are executed at the time of insertion. Set using the `default` attribute in the `sa_column` definition.

## 2. Resources

- [Source Tutorial](https://youtu.be/vTLpK5JNoWA?si=l0Nm0mCH-jOFOcdx)

## 3. Practical Steps: Hands-on Guide

1.  **Set up PostgreSQL:**

    - Install PostgreSQL locally or use a cloud service like Neon (which offers a free tier).
    - Optionally, you can use Docker to run a PostgreSQL container. The following is a sample `docker-compose.yml` file:

      ```yaml
      # docker run --name postgres_db -p 5432:5432 -e POSTGRES_USER=fastapi_usr -e POSTGRES_PASSWORD=fastapi_pwd -e POSTGRES_DB=fastapi_db -v db_data:/var/lib/postgresql/data -d postgres:17

      services:
        db:
          image: postgres:17
          container_name: postgres_db
          environment:
            POSTGRES_USER: fastapi_usr
            POSTGRES_PASSWORD: fastapi_pwd
            POSTGRES_DB: fastapi_db
          ports:
            - "5432:5432"
          volumes:
            - db_data:/var/lib/postgresql/data/

      volumes:
        db_data:
      ```

      If you want to connect with the database use the command:

      ```shell
      docker exec -it <container_name> psql -U <pg_user> -d <pg_database>
      ```

2.  **Create a Database:**
    - Using a PostgreSQL client (like `psql` shell), connect to your PostgreSQL server.
    - Execute the SQL command to create a new database (e.g., `bookly_DB`):
      ```sql
      CREATE DATABASE bookly_DB;
      ```
    - Note your PostgreSQL username, password, host, and port.
3.  **Create .env file:**

    - In the root directory of your project, create a file named `.env`.
    - Add your database connection URL to this file in the format `DATABASE_URL=postgresql+asyncpg://user:password@host:port/database_name`.

      For example:

      ```dotenv
      DATABASE_URL=postgresql+asyncpg://j35:your_password@localhost:5432/bookly_DB
      ```

4.  **Install Dependencies:**
    - Open your terminal in your project's virtual environment.
    - Install the asynchronous PostgreSQL driver (`asyncpg`) and `pydantic-settings`:
      ```bash
      pip install asyncpg pydantic-settings
      ```
    - Install SQLModel:
      ```bash
      pip install sqlmodel
      ```
5.  **Configure Pydantic Settings:**

    - Create a new Python file `src/config.py`.
    - Define a class to read your environment variables using `pydantic-settings`:

      ```python
      from pydantic_settings import BaseSettings, SettingsConfigDict

      class Settings(BaseSettings):
          DATABASE_URL: str

          model_config = SettingsConfigDict(
              env_file=".env",
              extra="ignore"
          )

      # Create an instance of the settings class to be imported elsewhere
      config = Settings()
      ```

    - This class will automatically read the `DATABASE_URL` from your `.env` file.

6.  **Add .env to .gitignore:**

    - To prevent committing your `.env` file (containing sensitive credentials) to version control, add `.env` to your project's `.gitignore` file.

7.  **Create Database Engine:**

    - Create a new package (folder) named `db` inside your `src` directory.
    - Inside the `db` package, create a file named `main.py`.
    - In `src/db/main.py`, create your database engine:

      ```python
      from sqlmodel import create_engine
      from sqlalchemy.ext.asyncio import AsyncEngine # Although AsyncEngine class is imported, create_engine directly returns async engine with asyncpg URL

      from src.config import config # Import the config object

      # Create the async database engine
      engine = AsyncEngine(create_engine(url=config.DATABASE_URL, echo=True)) # echo=True logs SQL statements
      ```

8.  **Set up FastAPI Lifespan Event:**
    - Go to your main FastAPI application file (where your `FastAPI` instance is created).
    - Import `@asynccontextmanager`:
      ```python
      from contextlib import asynccontextmanager
      from fastapi import FastAPI
      ```
    - Define an async function decorated with `@asynccontextmanager` that will serve as your lifespan event:
      ```python
      @asynccontextmanager
      async def lifespan(app: FastAPI):
          # Code before yield runs on startup
          print("Server is starting")
          # Here we will add our database initialization later
          yield # Application starts
          # Code after yield runs on shutdown
          print("Server has been stopped")
      ```
    - Pass this function to the `lifespan` attribute of your `FastAPI` application instance:
      ```python
      app = FastAPI(lifespan=lifespan)
      ```
9.  **Test Lifespan Event:**

    - Run your FastAPI application using `fastapi dev` pointing to your source directory:
      ```bash
      fastapi dev src
      ```
    - Observe "Server is starting" in the console. Press `Ctrl+C` and observe "Server has been stopped".

10. **Demonstrate Database Connection (Initial Test):**

    - In `src/db/main.py`, add a simple async function to test the database connection:

      ```python
      from sqlmodel import create_engine, text
      # ... (engine creation code from step 7) ...

      async def init_db():
          print("Initializing database connection")
          async with engine.begin() as con: # Use async with for async engine/connection
              # Simple test statement
              statement = text("SELECT 'hello'")
              result = await con.execute(statement)
              print(f"Database test result: {result.all()}")
          print("Database connection initialized")
      ```

    - In your main FastAPI app file, import the `init_db` function:

      ```python
      # ... (lifespan definition from step 8) ...
      from source.db.main import init_db # Import init_db

      @asynccontextmanager
      async def lifespan(app: FastAPI):
          print("Server is starting")
          await init_db() # Call init_db during startup
          yield
          print("Server has been stopped")
      # ... (FastAPI instance from step 8) ...
      ```

    - Run the server again (`fastapi dev source`). Observe the `SELECT 'hello'` statement logged by `echo=True` and the result printed, confirming the database connection.

11. **Define Database Model:**

    - Create a new file `src/books/models.py`. (Assuming you have a `books` package from previous steps)
    - Define your database model inheriting from `SQLModel`, setting `table=True`. Include fields with appropriate types and constraints:

      ```python
      import uuid
      from datetime import datetime

      import sqlalchemy.dialects.postgresql as pg
      from sqlmodel import Column, Field, SQLModel


      class Book(SQLModel, table=True):
          __tablename__ = "books"

          uid: uuid.UUID = Field(
              sa_column=Column(
                  pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
              )
          )
          title: str
          author: str
          publisher: str
          published_date: str
          page_count: int
          language: str
          created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
          updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

          def __repr__(self) -> str:
              return f"Book(title='{self.title}')"
      ```

12. **Create Database Tables on Startup:**

    - Modify the `init_db` function in `src/db/main.py` to create tables using SQLModel's metadata:

      ```python
      from sqlalchemy.ext.asyncio import AsyncEngine
      from sqlmodel import SQLModel, create_engine

      from src.config import config

      engine = AsyncEngine(create_engine(url=config.DATABASE_URL, echo=True))


      async def init_db():
          print("> Initializing database connection...")
          async with engine.begin() as conn:
              from src.books.models import Book  # noqa: F401 # Disable Ruff lint for this line

              await conn.run_sync(SQLModel.metadata.create_all)
          print("> Database connection initialized")
      ```

    - The `Book` model import is needed so `SQLModel.metadata` knows about it.

13. **Run Application to Create Tables:**
    - Ensure your FastAPI app is configured to call `init_db` in its lifespan startup (as done in step 10).
    - Run the server again (`fastapi dev source`).
    - Observe the logs. Due to `echo=True`, you should see `CREATE TABLE books ...` statements being executed.
14. **Verify Table Creation (Optional but Recommended):**

    - Connect to your PostgreSQL database using a client (like `psql` shell). If you're using Docker, enter this command

      ```shell
      docker exec -it <container_name> psql -U <pg_user> -d <pg_database>
      ```

    - List tables to confirm the `books` table exists:
      ```sql
      \dt
      ```
    - Describe the `books` table to see its structure and column types:
      ```sql
      \d books
      ```
    - Confirm the columns (`id`, `title`, `author`, etc.), their types (`uuid`, `character varying`, `timestamp`), nullable constraints, and primary key are as defined in your `Book` model.
