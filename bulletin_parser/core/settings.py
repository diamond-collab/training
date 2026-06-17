from typing import Literal
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class UrlConfig(BaseModel):
    base_url: str = 'https://spimex.com'
    trade_results_url: str = 'https://spimex.com/markets/oil_products/trades/results'


class LoggerConfig(BaseModel):
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level: Literal[
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
    ] = 'INFO'


class DataBaseConfig(BaseModel):
    name: str = ''
    host: str = 'localhost'
    port: int = 5432
    user: str = ''
    password: str = ''
    echo: bool = False

    @property
    def url(self) -> str:
        return (
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )

    logging: LoggerConfig = LoggerConfig()

    db: DataBaseConfig = DataBaseConfig()

    urls: UrlConfig = UrlConfig()


settings = Settings()
print(BASE_DIR)