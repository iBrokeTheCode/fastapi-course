from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def home() -> dict[str, str]:
    return {"message": "Hello world!"}


# Path Parameter -> 127.0.0.1:8000/greet/john-doe
@app.get("/greet/{name}")
async def greet(name: str) -> dict:
    return {"message": f"Hello {name}"}


# Query Parameters -> 127.0.0.1:8000/greet-user/?name=john-doe
@app.get("/greet-user")
async def greet_user(name: str) -> dict:
    return {"message": f"Hi {name}"}


# Query + Path Parameters -> 127.0.0.1:8000/full-greet/john-doe?age=20
@app.get("/full-greet/{name}")
async def full_greet(name: str, age: int) -> dict:
    return {"message": f"Hello {name}", "age": age}


# Optional Query Parameters -> http://127.0.0.1:8000/greet-optional or http://127.0.0.1:8000/greet-optional?name=john-doe&age=20
@app.get("/greet-optional")
async def greet_optional(name: Optional[str] = "N/A", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}


# Model
class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create-book")
def create_book(book_data: BookCreateModel) -> dict:
    return {"title": book_data.title, "author": book_data.author}
