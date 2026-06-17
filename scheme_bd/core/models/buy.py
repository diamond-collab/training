from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Buy(Base):
    __tablename__ = 'buy'

    buy_id: Mapped[int] = mapped_column(primary_key=True)
    buy_description: Mapped[str] = mapped_column(Text, nullable=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey(
            'client.client_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )