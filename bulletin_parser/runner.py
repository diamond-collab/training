import logging
import json
from datetime import date
from pathlib import Path

from bulletin_parser.core import settings, setup_logging

from bulletin_parser.dto import TradingResultDTO
from bulletin_parser.page_parser import PageFetcher, PageParser
from bulletin_parser.downloader import Downloader
from bulletin_parser.parsers import ParserFactory
from bulletin_parser.services import save_results
from bulletin_parser.core.models import db_helper

setup_logging(settings.logging)

logger = logging.getLogger(__name__)


CHECK_DATE = date(2023, 1, 1)
PROGRESS_FILE = 'progress.json'


class ProgressTracker:
    def __init__(self, file: Path):
        self.file = file
        self.page: int = 1
        self.last_date: date | None = None
        self.load()

    def save(self, page: int, last_date: date):
        self.page = page
        self.last_date = last_date
        with open(self.file, 'w') as file:
            json.dump(
                {
                    'page': self.page,
                    'last_date': last_date.isoformat(),
                },
                file
            )

    def load(self):
        if self.file.exists():
            with open(self.file, 'r') as file:
                data = json.load(file)
                self.page = data.get('page', 1)
                last_date_str = data.get('last_date')
                self.last_date = date.fromisoformat(last_date_str) if last_date_str else None
        else:
            self.page = 1
            self.last_date = None


def build_page_url(base_url: str, page: int) -> str:
    if page == 1:
        return base_url

    return f'{base_url}?page=page-{page}'


def main():
    base_url = settings.urls.trade_results_url
    # base_url = 'https://spimex.com/markets/oil_products/trades/results/?page=page-12'
    progress = ProgressTracker(Path(PROGRESS_FILE))

    page = progress.page
    saved_last_date = progress.last_date

    logger.info(f'Start cycle\nPage: {page}')

    while True:
        page_url = build_page_url(base_url, page)
        html = PageFetcher(page_url).fetch_page()
        bulletins = PageParser(html, base_url).parse_page()
        if not bulletins:
            break

        for bulletin in bulletins:
            if saved_last_date and bulletin.trade_date >= saved_last_date:
                logger.info(f"Бюллетень {bulletin.trade_date} уже обработан, пропускаем")
                continue

            if bulletin.trade_date < CHECK_DATE:
                logger.info(f'Все данные получены, достигнута дата {bulletin.trade_date}')
                return

            file_path = Downloader.download(bulletin=bulletin)
            parser = ParserFactory.get_parser(bulletin_type=bulletin.file_type)
            trading_results: list[TradingResultDTO] = parser.parse(file_path=file_path)

            with db_helper.get_session() as session:
                save_results(
                    session=session,
                    trading_results=trading_results,
                    trade_date=bulletin.trade_date,
                )
                logger.info(
                    f'Данные со страницы {page} сохранены'
                    f'Дата обработанного файла: {bulletin.trade_date}'
                )

            file_path.unlink()
            progress.save(page=page, last_date=bulletin.trade_date)


        page += 1

if __name__ == '__main__':
    main()
