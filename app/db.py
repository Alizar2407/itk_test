import os
from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession


DATABASE_URL = os.getenv("DATABASE_URL")

async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)
async_session_factory = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
