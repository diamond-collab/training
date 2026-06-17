import logging

from bulletin_parser.core.settings import LoggerConfig

LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}


def setup_logging(config: LoggerConfig) -> None:
    level = LEVEL_MAP.get(config.level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format=config.format,
        datefmt='%Y-%m-%d %H:%M:%S',
    )