import os
import datetime
import asyncio
from sqlalchemy import DateTime, String, Integer, JSON
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD",)
POSTGRES_USER = os.getenv("POSTGRES_USER",)
POSTGRES_DB = os.getenv("POSTGRES_DB",)
POSTGRES_HOST = os.getenv("POSTGRES_HOST",)
POSTGRS_PORT = os.getenv("POSTGRES_PORT",)

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRS_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    films: Mapped[str] = mapped_column(String(350), nullable=True)
    gender: Mapped[str] = mapped_column(String(200), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(200), nullable=True)
    height: Mapped[str] = mapped_column(String(30), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(200), nullable=True)
    mass: Mapped[str] = mapped_column(String(200), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(200), nullable=True)
    species: Mapped[str] = mapped_column(String(200), nullable=True)
    starships: Mapped[str] = mapped_column(String(200), nullable=True)
    vehicles: Mapped[str] = mapped_column(String(200), nullable=True)
    #



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_db():
    await engine.dispose()


async def main():
    await drop_db()
    await init_db()
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())