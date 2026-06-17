from sqlalchemy import ForeignKey, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = (
        CheckConstraint(
            'price > 0',
            name='ck_book_price_positive',
        ),
        CheckConstraint(
            'amount >= 0',
            name='ck_book_amount_non_negative',
        ),
    )


    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            'author.author_id',
            ondelete='RESTRICT',
        ),
        nullable=False,
        index=True,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            'genre.genre_id',
            ondelete='RESTRICT',
        ),
        nullable=False,
        index=True,
    )
    price: Mapped[int] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)