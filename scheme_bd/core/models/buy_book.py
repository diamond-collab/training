from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class BuyBook(Base):
    __tablename__ = 'buy_book'
    __table_args__ = (
        UniqueConstraint(
            'buy_id',
            'book_id',
            name='uq_buy_book_buy_id_book_id',
        ),
        CheckConstraint(
            'amount > 0',
            name='ck_buy_book_amount_positive',
        ),
    )

    buy_book_id: Mapped[int] = mapped_column(primary_key=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey(
            'buy.buy_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey(
            'book.book_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    amount: Mapped[int] = mapped_column(nullable=False)