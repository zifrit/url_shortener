import logging
from os import getenv
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

DESCRIPTION_MAX_LENGTH = 200

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", "0")) or 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_SHORT_URL = 3
REDIS_DB_FILMS = 4

REDIS_TOKENS_SET_NAME = "TOKENS_SET"
REDIS_TOKENS_SHORT_URL_HASH_NAME = "short-url"
REDIS_TOKENS_FILMS_HASH_NAME = "films"


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDBConfig(BaseModel):
    db: int = REDIS_DB
    db_tokens: int = REDIS_DB_TOKENS
    db_users: int = REDIS_DB_USERS
    db_short_url: int = REDIS_DB_SHORT_URL
    db_films: int = REDIS_DB_FILMS


class RedisTokensConfig(BaseModel):
    set_name: str = REDIS_TOKENS_SET_NAME
    short_url: str = REDIS_TOKENS_SHORT_URL_HASH_NAME
    film: str = REDIS_TOKENS_FILMS_HASH_NAME


class RedisConfig(BaseSettings):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDBConfig = RedisDBConfig()
    token: RedisTokensConfig = RedisTokensConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
