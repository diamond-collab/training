from dataclasses import asdict

from sqlalchemy import insert
from sqlalchemy.orm import Session

from bulletin_parser.dto.save_result_data import SaveResultData
from bulletin_parser.core.models.spimex_trading_results import SpimexTradingResults


def save_many(session: Session, save_data: list[SaveResultData]):
    values = [asdict(item) for item in save_data]

    stmt = insert(SpimexTradingResults).values(values)
    session.execute(stmt)
    session.commit()





