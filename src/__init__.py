from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.books.routes import book_router

version = "v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("> Server is starting...")
    yield
    print("> Server has been stopped...")


app = FastAPI(
    title="Bookly",
    description="A book review web service",
    version=version,
    lifespan=lifespan,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books", "api"])
