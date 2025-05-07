from typing import List

from fastapi import FastAPI, status

from db import sample_books
from schemas import Book

app = FastAPI()


@app.get("/books", response_model=List[Book])
async def get_all_books():
    """Return all books."""
    return sample_books


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> dict:
    """Create a book."""
    new_book = book.model_dump()
    sample_books.append(book)
    return new_book
