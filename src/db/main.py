from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, create_engine

from src.config import config

engine = AsyncEngine(create_engine(url=config.DATABASE_URL, echo=True))


async def init_db():
    print("> Initializing database connection...")
    async with engine.begin() as conn:
        from src.books.models import Book  # noqa: F401

        await conn.run_sync(SQLModel.metadata.create_all)
    print("> Database connection initialized")
