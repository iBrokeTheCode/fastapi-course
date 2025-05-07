from typing import List

from fastapi import FastAPI

from db import sample_books
from schemas import Book

app = FastAPI()


@app.get("/books", response_model=List[Book])
async def get_all_books():
    return sample_books
