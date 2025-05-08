from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.books.db import sample_books
from src.books.schemas import BookCreate, BookUpdate

book_router = APIRouter()


@book_router.get("/", response_model=List[BookCreate])
async def get_all_books():
    """Return all books."""
    return sample_books


@book_router.post("/", response_model=BookCreate, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate) -> dict:
    """Create a book."""
    new_book = book.model_dump()
    sample_books.append(book)
    return new_book


@book_router.get("/{book_id}", response_model=BookCreate)
async def get_book(book_id: int) -> dict:
    """Get book by id."""
    for book in sample_books:
        if book.id == book_id:
            return book.model_dump()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch("/{book_id}", response_model=BookCreate)
async def update_book(book_id: int, book_data: BookUpdate) -> dict:
    """Update book."""
    for book in sample_books:
        if book.id == book_id:
            book.title = book_data.title
            book.author = book_data.author
            book.publisher = book_data.publisher
            book.page_count = book_data.page_count
            book.language = book_data.language

            return book.model_dump()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete book."""
    for book in sample_books:
        if book.id == book_id:
            sample_books.remove(book)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
