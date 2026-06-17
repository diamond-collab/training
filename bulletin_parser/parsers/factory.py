import logging

from bulletin_parser.parsers.pdf_parser import PdfParser
from bulletin_parser.parsers.xls_parser import XlsParser


logger = logging.getLogger(__name__)

class ParserFactory:
    @staticmethod
    def get_parser(bulletin_type: str):
        if bulletin_type == 'xls':
            logger.info(f'Получен файл с расширением {bulletin_type}')
            return XlsParser()
        elif bulletin_type == 'pdf':
            logger.info(f'Получен файл с расширением {bulletin_type}')
            return PdfParser()
        else:
            raise NotImplementedError('Файл с подходящим расширением не найден')
