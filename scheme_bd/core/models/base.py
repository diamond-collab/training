from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    abstract = True # Не создает таблицу Base