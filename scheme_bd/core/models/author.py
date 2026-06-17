from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Author(Base):
    __tablename__ = 'author'

    author_id: Mapped[int] = mapped_column(primary_key=True)
    name_author: Mapped[str] = mapped_column(nullable=False)
