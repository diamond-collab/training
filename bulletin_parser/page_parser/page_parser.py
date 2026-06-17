import logging
import time
from urllib.parse import urljoin
from dataclasses import dataclass
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

from bulletin_parser.core.settings import settings


logger = logging.getLogger(__name__)


MAX_ATTEMPTS = 3
DELAY_SECONDS = 5


@dataclass
class BulletinLink:
    url: str
    trade_date: date
    file_type: str


class PageFetcher:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def fetch_page(self) -> str:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                response = requests.get(self.base_url, timeout=15)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning("Ошибка получения HTML: %s", e)

                if attempt < MAX_ATTEMPTS:
                    logger.info(
                        f'Повторная попытка {DELAY_SECONDS} секунд... (Attempt {attempt} от {MAX_ATTEMPTS})'
                    )
                    time.sleep(DELAY_SECONDS)
                else:
                    raise

        raise RuntimeError('Запрос не выполнен не удалось получить html страницы')




class PageParser:
    def __init__(self, html: str, base_url: str) -> None:
        self.html = html
        self.bulletins: list[BulletinLink] = []
        self.base_url = base_url

    def parse_page(self) -> list[BulletinLink]:
        if self.html is None:
            raise ValueError("HTML не передан в PageParser, невозможно запустить парсер")

        soup = BeautifulSoup(self.html, 'lxml')
        items = soup.find_all('div', class_='accordeon-inner__item')

        for item in items:
            bulletin = self._parse_item(item=item)
            if bulletin is None:
                # logger.info('SKIPPED %s')
                # logger.info('ITEM %s', item.prettify()[:1000])
                continue

            self.bulletins.append(bulletin)

        return self.bulletins

    def _parse_item(self, item) -> BulletinLink | None:
        tag_a = item.find('a')
        href = tag_a.get('href')

        full_href = urljoin(settings.urls.base_url, href) # заменить base_url на https://spimex.com

        file_type = self._get_file_type(href=href)
        if file_type is None:
            return None

        title_div = item.find('div', class_='accordeon-inner__item-inner__title')
        # logger.info('TITLE_DIV %s', title_div)
        if title_div:
            span_tag = title_div.find('span')
            # logger.info('SPAN_TAG', span_tag)
            if span_tag:
                trade_date = self._parse_trade_date(raw_date=span_tag.text)
              #  logger.info('TRADE DATE', trade_date)

                return BulletinLink(
                    url=full_href,
                    trade_date=trade_date,
                    file_type=file_type
                )

        return None

    @staticmethod
    def _get_file_type(href: str) -> str | None:
        if '.pdf' in href:
            return 'pdf'
        elif '.xls' in href:
            return 'xls'

        return None

    @staticmethod
    def _parse_trade_date(raw_date: str) -> date:
        trade_date_str = raw_date.strip()
        return datetime.strptime(trade_date_str, '%d.%m.%Y').date()