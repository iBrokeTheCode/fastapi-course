from typing import List

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

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


@app.get("/book/{book_id}", response_model=Book)
async def get_book(book_id: int) -> dict:
    for book in sample_books:
        if book.id == book_id:
            return book.model_dump()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
