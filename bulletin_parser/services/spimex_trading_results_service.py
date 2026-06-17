from datetime import date

from sqlalchemy.orm import Session

from bulletin_parser.dto import TradingResultDTO
from bulletin_parser import repository as repo
from bulletin_parser.dto.save_result_data import SaveResultData


def prepare_save_data(trading_results: list[TradingResultDTO], trade_date: date) -> list[
    SaveResultData]:
    save_data = []
    for tr in trading_results:
        save_data.append(
            SaveResultData(
                exchange_product_id=tr.exchange_product_id,
                exchange_product_name=tr.exchange_product_name,
                oil_id=tr.exchange_product_id[:4],
                delivery_basis_id=tr.exchange_product_id[4:7],
                delivery_basis_name=tr.delivery_basis_name,
                delivery_type_id=tr.exchange_product_id[-1],
                volume=tr.volume,
                total=tr.total,
                count=tr.count,
                date=trade_date,
            )
        )

    return save_data


def save_results(session: Session, trading_results: list[TradingResultDTO], trade_date: date):
    save_data = prepare_save_data(trading_results, trade_date)

    return repo.save_many(session, save_data)

