from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine, text

from src.config import config

engine = AsyncEngine(create_engine(url=config.DATABASE_URL, echo=True))


async def init_db():
    print("> Initializing database connection...")
    async with engine.begin() as conn:
        statement = text("SELECT 'Hello';")
        result = await conn.execute(statement)
        print(f"> Results: {result.all()}")
    print("> Database connection initialized")
