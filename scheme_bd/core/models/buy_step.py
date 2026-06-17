from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class BuyStep(Base):
    __tablename__ = 'buy_step'

    buy_step_id: Mapped[int] = mapped_column(primary_key=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey(
            'buy.buy_id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey(
            'step.step_id',
            ondelete='RESTRICT',
        ),
        nullable=False,
        index=True,
    )
    date_buy_beg: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
    date_step_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )