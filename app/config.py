from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    MODE: Literal['DEV', 'PROD']
    SITE_DOMAIN: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def database_url(self):
        user = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f'postgresql+asyncpg://{user}@{database}'

    class Config:
        env_file = '.env'


settings = Settings()
