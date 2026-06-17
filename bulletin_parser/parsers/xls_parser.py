import logging
from typing import Any, Sequence

import xlrd
from xlrd.sheet import Sheet

from bulletin_parser.dto.trading_result_dto import TradingResultDTO

logger = logging.getLogger(__name__)


ROWS_AFTER_TITLE = 3


class XlsParser:
    def parse(self, file_path: str) -> list[TradingResultDTO]:
        with xlrd.open_workbook(file_path) as xls:
            sheet = xls.sheet_by_index(0)

            result: list[TradingResultDTO] = []
            start_row = self._find_start_row(sheet=sheet)
            if start_row is None:
               return []

            for row_index in range(start_row + ROWS_AFTER_TITLE, sheet.nrows):
                row_values = sheet.row_values(row_index)
                # logger.info(f'Values: {row_values}')
                trading_result = self._parse_row(row_values)

                if trading_result is None:
                    continue

                result.append(trading_result)
            # logger.info(f'Results: {result}')
            return result

    @staticmethod
    def _find_start_row(sheet: Sheet) -> int | None:
        for row_index in range(sheet.nrows):
            if 'Единица измерения: Метрическая тонна' in sheet.row_values(row_index):
                # logger.info(f'Нашел нужную единицу измерения')
                # logger.info(f'Index: {row_index}')
                return row_index

        return None

    @staticmethod
    def _parse_row(values: Sequence[str]) -> TradingResultDTO | None:
        # logger.info(type(values[5]))
        # logger.info(type(values[-1]))
        if values[1].startswith('Итого'):
            return None

        if len(values[1]) <= 1:
            return None

        if len(values[1]) != 11:
            return None

        if values[-1] != '-':
            # logger.info(f'VALUES: {values[1]}')
            # raw_volume = values[4].strip()
            # volume = int(raw_volume) if raw_volume else 0
            # logger.info(f'VOLUME: {volume}')

            return TradingResultDTO(
                exchange_product_id=values[1],
                exchange_product_name=values[2],
                delivery_basis_name=values[3],
                volume=int(values[4]),
                total=int(values[5]),
                count=int(values[-1]),
            )

        return None


