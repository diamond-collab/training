from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    name_genre: Mapped[str] = mapped_column(nullable=False)
