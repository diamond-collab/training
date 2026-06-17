import logging
from typing import Any

import pdfplumber
from pdfplumber.pdf import PDF
from pdfplumber.page import Page

from bulletin_parser.dto.trading_result_dto import TradingResultDTO

logger = logging.getLogger(__name__)



class PdfParser:
    def parse(self, file_path) -> list[TradingResultDTO]:
        with pdfplumber.open(file_path) as pdf:
            first_page_data = self._find_first_page(pdf=pdf)

            if first_page_data is None:
                return []

            page_index, y = first_page_data
            results: list[TradingResultDTO] = []

            for idx, page in enumerate(pdf.pages[page_index:]):
                # logger.info("Page: %s", idx)
                if idx == 0:
                    tables = self._extract_tables_from_page(page=page, y=y)
                else:
                    # Все последующие страницы берём полностью
                    tables = self._extract_tables_from_page(page=page)

                for table in tables:
                    for row in table[2:]:
                        # logger.info("ROW: %s", row)
                        trading_result = self._parse_row(row)
                        if trading_result is None:
                            continue

                        results.append(trading_result)

            return results

    def _find_first_page(self, pdf: PDF) -> tuple[int, float] | None:
        for idx, page in enumerate(pdf.pages):
            # logger.info(f'Page Number: {idx}')

            if 'Единица измерения: Метрическая тонна' in page.extract_text():
                y = self._search_coords(page)
                if y is None:
                    continue

                return idx, y

        return None

    @staticmethod
    def _extract_tables_from_page(page: Page, y=None):
        if y is None:
            return page.extract_tables()
        else:
            cropped_page = page.crop((0, y, page.width, page.height))
            return cropped_page.extract_tables()

    @staticmethod
    def _search_coords(page: Page) -> float | None:
        coords = page.search('Единица измерения: Метрическая тонна')
        if not coords:
            return None

        bottom = coords[0].get('bottom')
        if not isinstance(bottom, int | float):
            return None

        return float(bottom)

    @staticmethod
    def _parse_row(row) -> TradingResultDTO | None:
        # logger.info(f'Row: {row[0]}')

        if row[-1] != '-':
            return TradingResultDTO(
                exchange_product_id=row[0],
                exchange_product_name=row[1],
                delivery_basis_name=row[2],
                volume=int(row[3]),
                total=int(row[4]),
                count=int(row[-1]),
            )

        return None
