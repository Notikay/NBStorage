from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    APP_VERSION = version('nbstorage')
except PackageNotFoundError:
    APP_VERSION = "dev"


class DBSettings(BaseModel):
    url: str = 'postgresql+psycopg2://postgres:nbtestpassword@db:5432/postgres-database'
    # url: str = 'sqlite:///db/nbstorage.db'


class StoreSettings(BaseModel):
    endpoint: str = 'minio:9000'
    access_key: str = 'minio'
    secret_key: str = 'nbtestpassword'
    secure: bool = False

    public_bucket_name: str = 'public'
    private_bucket_name: str = 'private'
    public_url: str = 'http://localhost:9000'


class APISettings(BaseModel):
    title: str = 'NBStorage API'
    summary: str = "API для менеджера паролей NBStorage"
    description: str = """..."""
    version: str = APP_VERSION
    openapi_url: str | None = '/openapi.json'
    docs_url: str | None = '/docs'
    redoc_url: str | None = '/redoc'


class CORSSettings(BaseModel):
    allow_origins: list[str] = ['*']
    allow_methods: list[str] = ['*']
    allow_headers: list[str] = ['*']


class Settings(BaseSettings):
    database: DBSettings = DBSettings()
    store: StoreSettings = StoreSettings()

    api: APISettings = APISettings()

    cors: CORSSettings = CORSSettings()
    trusted_hosts: list[str] = ["localhost", "127.0.0.1"]

    debug: bool = False
    environment: Literal['dev', 'prod'] = 'prod'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        extra='ignore',
        validate_default=True,
        frozen=True
    )


@lru_cache
def load_settings() -> Settings:
    return Settings()
