import os

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings

load_dotenv(find_dotenv())

BASE_PATH = os.path.abspath(os.path.join(__file__, '..', '..'))


class Settings(BaseSettings):
    db_host: str = os.environ.get('DB_HOST')
    db_port: int = os.environ.get('DB_PORT')
    db_user: str = os.environ.get('DB_USER')
    db_pass: str = os.environ.get('DB_PASSWORD')
    db_base: str = os.environ.get('DB_NAME')

    redis_host: str = os.environ.get('REDIS_HOST')

    broker: str = os.environ.get('BROKER')

    def db_url(self):
        url = f"postgres://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_base}"
        return url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
print(settings.dict())
