from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from bulletin_parser.core.settings import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        with self.session_factory() as session:
            yield session



db_helper = DataBaseHelper(url=settings.db.url, echo=settings.db.echo)