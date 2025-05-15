# CRUD With Async SQLModel (An Introduction to Dependency Injection)

This tutorial builds upon previous videos, focusing on implementing CRUD (Create, Read, Update, Delete) operations for a book resource using **Async SQLModel** in a FastAPI application. The primary learning objectives are to **separate database interaction logic** into a dedicated **service class** and to introduce **FastAPI's dependency injection system** to manage and share resources like the database session across different route handlers. The video also addresses and corrects some initial mistakes made in setting up the database model and schemas.

## 1. Core Concepts

- **Service Class Pattern:** A **service class** is introduced as a way to encapsulate and organize all the **CRUD logic** for a specific resource (e.g., books). This separation keeps route handlers cleaner and focused on handling requests and responses, delegating database operations to the service class.
- **SQLModel/SQLAlchemy Session Object:** The **session object** (specifically **`AsyncSession`** when working with asynchronous operations) acts as the primary interface provided by SQLModel and SQLAlchemy for interacting with the database. It is used to perform **transactions**, execute **SQL statements**, and manage the lifecycle of database objects. The session is obtained from a **session class** created using SQLAlchemy's **`sessionmaker`**, bound to an **async engine**. Setting **`expire_on_commit=False`** on the sessionmaker allows session objects to be used even after committing transactions.
- **Database Statement Construction:** Database queries are constructed using **SQLModel/SQLAlchemy functions** like **`select`** to define the data to retrieve. **`where`** is used for filtering based on conditions. **`order_by`** is used to specify the sorting of results, often combined with **`descending` (`desc`)** for reverse order.
- **Executing Statements:** Statements are executed asynchronously using the **`await session.exec(statement)`** method. This returns a **result object**.
- **Retrieving Results:** Data is retrieved from the result object using methods like **`result.all()`** to get a list of all matching records or **`result.first()`** to retrieve a single record (or `None` if no record is found).
- **Adding and Deleting Records:** New objects are added to the session using **`session.add(object)`**. Existing objects are marked for deletion using **`session.delete(object)`**.
- **Committing Transactions:** Changes made via the session (additions, updates, deletions) are persisted to the database by **awaiting `session.commit()`**. **`session.refresh(object)`** can be used to update an object's state after a commit, though not explicitly detailed for all operations in this transcript segment.
- **Pydantic Schemas (Data Models):** Separate Pydantic classes (e.g., **`BookCreate`**, **`BookUpdate`**) are defined, often in a `schemas.py` file, to specify the **structure and validation rules for incoming request data** (like data needed to create or update a book). These are distinct from the main SQLModel class used for database interaction and retrieving full objects.
- **Type Hinting:** Using **type hints** (e.g., specifying a parameter as `AsyncSession` or `BookCreate`) improves code readability and allows development tools to provide better assistance.
- **Dependency Injection (FastAPI):** FastAPI's **`Depends`** mechanism allows injecting resources or logic into route handler functions. A function (like **`get_session`**) that **`yield`**s a resource (like an `AsyncSession`) can be used as a dependency. FastAPI handles the setup and teardown of the dependency for each request.
- **Response Model (FastAPI):** The **`response_model`** parameter in FastAPI route decorators is used to specify the Pydantic schema that the response data will be validated and serialized against. This ensures the output is in the expected JSON format and handles conversions (like date objects to strings).
- **Error Handling in Route Handlers:** Route handlers should check the results returned by service methods (especially methods that might return `None` if an object is not found). If an object is not found, an **`HTTPException`** (e.g., `status_code=404`, `detail="Not Found"`) should be raised to inform the client.

## 2. Resources

- [Source Tutorial](https://youtu.be/AtHEX76Wysw?si=zQa-E4ei5lx2Yphy)

## 3. Practical Steps: Hands-on Guide

1.  **Correct Database Model Errors:**

    - Modify timestamp fields (`created_at`, `updated_at`) in your SQLModel class (`src/books/models.py`) to use `sa_column` explicitly for SQLAlchemy types instead of being treated purely as Pydantic fields.
    - Ensure UUID fields are correctly defined, typically not calling `uuid4()` with brackets in the default value definition, as this can lead to generating the same UUID repeatedly.
    - Update the `published_date` field in your database model to be a `Date` type (SQLAlchemy/SQLModel type) if you intend to store dates, while potentially receiving it as a string in schemas.
    - **Drop and recreate your database table** to apply model changes. This can be done via a database client (e.g., `psql`) by running `DROP TABLE books;`. The table will be recreated when the server starts with the updated model.

      ```shell
      docker exec -it <container_name> psql -U <pg_user> -d <pg_database>

      # psql CLI
      \c db_name
      DROP TABLE table_name;
      ```

2.  **Create Pydantic Schemas for Request Data:**

    - Create a file (e.g., `schemas.py`) for your data models.
    - Define a class (e.g., `BookCreate`) inheriting from `BaseModel` (or SQLModel) with fields required for _creating_ a book. This typically excludes auto-generated fields like `id`, `created_at`, `updated_at`. Include necessary fields like `title`, `author`, `publisher`, `published_date`, etc.. Ensure UUID fields match the model's UUID type. Define date fields (like `published_date`) as appropriate for incoming data (e.g., `str` initially, though conversion will be needed).
    - Define a class (e.g., `BookUpdate`) inheriting from `BaseModel` for _updating_ a book. This model might have optional fields since not all fields may be updated.

      ```py
      import uuid
      from datetime import datetime

      from pydantic import BaseModel


      class BookBase(BaseModel):
          title: str
          author: str
          publisher: str
          page_count: int
          language: str


      class Book(BookBase):
          uid: uuid.UUID
          published_date: str
          created_at: datetime
          updated_at: datetime


      class BookCreate(BookBase):
          published_date: str


      class BookUpdate(BookBase):
          pass
      ```

3.  **Create the Service Class:**

    - Create a Python file (e.g., `service.py`) for your service logic.
    - Define an async class (e.g., `BookService`).
    - Inside the class, define **async methods** for each CRUD operation (`get_all_books`, `get_book`, `create_book`, `update_book`, `delete_book`).
    - Each service method should accept an **`AsyncSession`** object as a parameter. Use type hinting for the session (`session: AsyncSession`).
    - Creation and update methods should accept a Pydantic model instance (e.g., `book_data: BookCreate`, `update_data: BookUpdate`) representing the input data.
    - Retrieve and delete methods should accept the ID of the resource (e.g., `book_uid: UUID` or `str`, depending on how it's received).

      ```py
        from sqlmodel.ext.asyncio.session import AsyncSession

        from src.books.schemas import BookCreate, BookUpdate


        class BookService:
            async def get_all_books(self, session: AsyncSession):
                pass

            async def get_book(self, book_uid: str, session: AsyncSession):
                pass

            async def create_book(self, book_data: BookCreate, session: AsyncSession):
                pass

            async def update_book(
                self, book_uid: str, update_data: BookUpdate, session: AsyncSession
            ):
                pass

            async def delete_book(self, book_uid: str, session: AsyncSession):
                pass
      ```

---

4.  **Implement Read Operations in the Service Class:**

    - **`get_all_books`:**
      - Construct a select statement using `select(Book)`.
      - Optionally, order the results using `order_by(desc(Book.created_at))`.
      - Execute the statement: `result = await session.exec(statement)`.
      - Return all results: `return result.all()`.
    - **`get_book`:**
      - Construct a select statement: `statement = select(Book).where(Book.uid == book_uid)`.
      - Execute the statement: `result = await session.exec(statement)`.
      - Return the first result: `return result.first()`. Add a check: `return book if book is not None else None`.

5.  **Implement Create Operation in the Service Class:**

    - **`create_book`:**
      - Receive `book_data: BookCreate` and `session: AsyncSession`.
      - Convert the Pydantic model to a dictionary: `book_data_dict = book_data.model_dump()`.
      - Create a new `Book` object, unpacking the dictionary: `new_book = Book(**book_data_dict)`.
      - **Handle Date Conversion:** For fields like `published_date` received as strings in the schema but stored as `Date` in the database, manually convert the string to a `datetime` or `date` object using `datetime.strptime(date_string, format_string)` before adding the object to the session. Assign the converted date to the new book object: `new_book.published_date = datetime.strptime(...)`.
      - Add the new book to the session: `session.add(new_book)`.
      - Commit the transaction: `await session.commit()`.
      - (Optional but good practice) Refresh the object to load any auto-generated fields: `await session.refresh(new_book)` (not explicitly shown for create commit in transcript, but common).
      - Return the created book object: `return new_book`.

6.  **Implement Update Operation in the Service Class:**

    - **`update_book`:**
      - Receive `book_uid: UUID` (or `str`), `update_data: BookUpdate`, and `session: AsyncSession`.
      - Retrieve the existing book using the `get_book` method: `book_to_update = await self.get_book(book_uid=book_uid, session=session)`. Note the required `await`.
      - **Check if the book was found:** If `book_to_update is None`, return `None`.
      - Convert the update data Pydantic model to a dictionary, excluding fields that weren't provided (None values): `update_data_dict = update_data.model_dump(exclude_unset=True)` (or similar approach).
      - Iterate through the items in the update data dictionary: `for key, value in update_data_dict.items():`.
      - Update the attributes of the `book_to_update` object using `setattr(book_to_update, key, value)`.
      - Add the updated book to the session: `session.add(book_to_update)` (or implicitly done if retrieved via session).
      - Commit the transaction: `await session.commit()`.
      - (Optional but good practice) Refresh the object: `await session.refresh(book_to_update)` (not explicitly shown for update commit in transcript, but common).
      - Return the updated book object: `return book_to_update`.

7.  **Implement Delete Operation in the Service Class:**

    - **`delete_book`:**
      - Receive `book_uid: UUID` (or `str`) and `session: AsyncSession`.
      - Retrieve the book to delete (similar to update): `book_to_delete = await self.get_book(book_uid=book_uid, session=session)` (though the final code shown directly uses `book_to_delete` without explicitly showing the `get_book` call, the logic implies retrieving it first to check if it exists).
      - **Check if the book was found:** If `book_to_delete is None`, return `None`.
      - Delete the book from the session: `await session.delete(book_to_delete)`.
      - Commit the transaction: `await session.commit()`.
      - Return the deleted object (or a confirmation, or `None` as handled in the route).

8.  **Create the Session Dependency:**

    - Create a file for database dependencies (e.g., `db/main.py`).
    - Import `AsyncSession` and `sessionmaker`.
    - Define your `AsyncEngine` (created in a previous step/video, not shown here).
    - Create the session class using `sessionmaker`:

      ```python
      SessionLocal = sessionmaker(
          bind=async_engine,
          class_=AsyncSession,
          expire_on_commit=False
      )
      ```

    - Define an async function `get_session` that will be the dependency:
      ```python
      async def get_session() -> AsyncSession:
          async with SessionLocal() as session:
              yield session
      ```
      This function creates a session context and yields the session, ensuring it's closed after the request.

9.  **Inject Dependencies and Use the Service in Route Handlers:**

    - Navigate to your route handler file (e.g., `routes.py`).
    - Import `Depends` from `fastapi`.
    - Import your `get_session` dependency function and `AsyncSession` type.
    - Import your `BookService` class and Pydantic schemas (`Book`, `BookCreate`, `BookUpdate`).
    - For each route handler function that needs database access:
      - Add a session parameter with type hinting and `Depends`: `session: AsyncSession = Depends(get_session)`.
      - (Optional but good practice) Instantiate your `BookService` inside the route handler, passing the session: `book_service = BookService()`. You could also potentially inject the service itself if it depends only on the session, but instantiating inside is simpler initially.
      - Call the appropriate async method on the `book_service` instance, **awaiting** the call: `books = await book_service.get_all_books(session=session)`.
      - For methods that might return `None` (like `get_book`, `update_book`, `delete_book`), **check the return value**. If it's `None`, raise an `HTTPException` with a `404 Not Found` status code.
      - Add the **`response_model`** parameter to your route decorator (`@router.<method>(..., response_model=YourSchema)`) to validate and serialize the response. Use the appropriate schema (e.g., `List[Book]` for getting all, `Book` for getting one/creating/updating).
      - Ensure path/query parameters for IDs are correctly typed (e.g., `UUID` or `str`, matching your service method definition).

10. **Test the Endpoints:**
    - Use a tool like Restfox (shown in the video) or `curl`, Postman, Swagger UI (`/docs`) to test your API endpoints (GET all, POST create, GET by ID, PUT update, DELETE by ID).
    - Debug any errors related to data types (e.g., string vs. date conversion, integer vs. UUID/string for IDs), missing fields (check schemas and response models), or database interaction (check session usage and statement execution). Correct type hints and `response_model` definitions as needed. Ensure `await` is used for all async calls.
