from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine

from src.config import config

engine = AsyncEngine(create_engine(url=config.DATABASE_URL, echo=True))
