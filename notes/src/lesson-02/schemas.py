from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


class BookCreate(BookBase):
    id: int
    published_date: str


class BookUpdate(BookBase):
    pass
