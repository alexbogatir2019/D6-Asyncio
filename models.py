import os
from dotenv import load_dotenv

from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncAttrs)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

PG_PASSWORD = os.getenv("PG_PASSWORD", "password")
PG_USER = os.getenv("PG_USER", "swapi")
PG_DB = os.getenv("PG_DB", "swapi")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiPerson(Base):
    __tablename__ = 'swapi_person'

    # идентификатор персонажа
    id: Mapped[int] = mapped_column(primary_key=True)
    # дата рождения персонажа
    birth_year: Mapped[str] = mapped_column(String(1000), nullable=True)
    # цвет глаз персонажа
    eye_color: Mapped[str] = mapped_column(String(1000), nullable=True)
    # строка с названиями фильмов (перечисленными через запятую)
    films: Mapped[str] = mapped_column(String(1000), nullable=True)
    # пол
    gender: Mapped[str] = mapped_column(String(1000), nullable=True)
    # цвет волос
    hair_color: Mapped[str] = mapped_column(String(1000), nullable=True)
    # рост
    height: Mapped[str] = mapped_column(String, nullable=True)
    # родной мир
    homeworld: Mapped[str] = mapped_column(String(1000), nullable=True)
    # масса
    mass: Mapped[str] = mapped_column(String, nullable=True)
    # имя
    name: Mapped[str] = mapped_column(String(1000))
    skin_color: Mapped[str] = mapped_column(String(1000), nullable=True)
    # строка с названиями типов (перечисленными через запятую)
    species: Mapped[str] = mapped_column(String(1000), nullable=True)
    # строка с названиями космических кораблей (перечисленными через запятую)
    starships: Mapped[str] = mapped_column(String(1000), nullable=True)
    # строка с названиями транспорта (перечисленными через запятую)
    vehicles: Mapped[str] = mapped_column(String(1000), nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
