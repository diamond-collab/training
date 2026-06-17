from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Client(Base):
    __tablename__ = 'client'

    client_id: Mapped[int] = mapped_column(primary_key=True)
    name_client: Mapped[str] = mapped_column(String(100),nullable=False)
    city_id: Mapped[int] = mapped_column(
        ForeignKey(
            'city.city_id',
            ondelete='RESTRICT',
        ),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
