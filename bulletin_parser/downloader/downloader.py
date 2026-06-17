import logging
from pathlib import Path
from urllib.parse import urlparse
import time

import requests

from bulletin_parser.page_parser import BulletinLink


logger = logging.getLogger(__name__)


current_dir = Path(__file__).resolve().parent
download_dir = current_dir / 'downloads'
download_dir.mkdir(parents=True, exist_ok=True)


class Downloader:
    @staticmethod
    def create_path(file_url: str) -> Path:
        filename = Path(urlparse(file_url).path).name
       # logger.info(f'filename: {filename}')

        file_path = Path(download_dir / filename)
       # logger.info(f'file_path: {file_path}')

        return file_path

    @staticmethod
    def download(bulletin: BulletinLink) -> Path:
        file_url = bulletin.url
        logger.info(f'Downloading {file_url}')
        file_path = Downloader.create_path(file_url=file_url)

        max_attempts = 3
        delay_seconds = 5

        for attempt in range(1, max_attempts + 1):
            try:
                response = requests.get(file_url, timeout=60)
                response.raise_for_status()

                with open(file_path, 'wb') as file:
                    file.write(response.content)
                return file_path

            except requests.RequestException as e:
                logger.exception('Не удалось загрузить файл: %s', file_url)

                if attempt < max_attempts:
                    logger.info(
                        f'Повторная попытка {delay_seconds} секунд... (Attempt {attempt} '
                                f'от {max_attempts})')
                    time.sleep(delay_seconds)
                else:
                    raise

        raise RuntimeError(f"Не удалось скачать файл {file_url} после {max_attempts} попыток")