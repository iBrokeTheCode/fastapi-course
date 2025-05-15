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


# FIXME: routes.py
class BookUpdate(BookBase):
    pass
