from typing import List

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from db import sample_books
from schemas import BookCreate, BookUpdate

app = FastAPI()


@app.get("/books", response_model=List[BookCreate])
async def get_all_books():
    """Return all books."""
    return sample_books


@app.post("/books", response_model=BookCreate, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate) -> dict:
    """Create a book."""
    new_book = book.model_dump()
    sample_books.append(book)
    return new_book


@app.get("/book/{book_id}", response_model=BookCreate)
async def get_book(book_id: int) -> dict:
    """Get book by id."""
    for book in sample_books:
        if book.id == book_id:
            return book.model_dump()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch("/book/{book_id}", response_model=BookCreate)
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


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete book."""
    for book in sample_books:
        if book.id == book_id:
            sample_books.remove(book)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
