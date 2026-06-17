from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class City(Base):
    __tablename__ = 'city'

    city_id: Mapped[int] = mapped_column(primary_key=True)
    name_city: Mapped[str] = mapped_column(nullable=False)
    days_delivery: Mapped[datetime] = mapped_column(nullable=False)