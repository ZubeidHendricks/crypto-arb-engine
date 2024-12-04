from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from ..config.settings import Settings

def get_session_factory(settings: Settings):
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )