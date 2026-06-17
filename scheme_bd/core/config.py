from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]

class DataBaseConfig(BaseModel):
    name: str = ''
    host: str = 'localhost'
    port: int = 5432
    user: str = ''
    password: str = ''
    echo: bool = False

    @property
    def url(self):
        """Собирается полный URL для SQLAlchemy"""
        return (f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}'
                f'/{self.name}')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )

    db: DataBaseConfig = DataBaseConfig()


settings = Settings()
print(settings.db.url)