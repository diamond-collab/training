from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from bulletin_parser.core.models import Base



class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[date]
    created_on: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_on: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )



