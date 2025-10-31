import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

DESCRIPTION_MAX_LENGTH = 200


class LoggingConfig(BaseModel):
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDBConfig(BaseModel):
    db: int = 0
    db_tokens: int = 1
    db_users: int = 2
    db_short_url: int = 3
    db_films: int = 4

    @model_validator(mode="after")
    def check_not_duplicated(self) -> "RedisDBConfig":
        vals = self.model_dump().values()
        unic_val = set(vals)
        list_val = list(vals)
        if len(unic_val) != len(list_val):
            raise ValueError("Duplicated values: " + ", ".join(list_val))
        return self


class RedisTokensConfig(BaseModel):
    set_name: str = "TOKENS_SET"
    short_url: str = "short-url"
    film: str = "films"


class RedisConfig(BaseSettings):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDBConfig = RedisDBConfig()
    token: RedisTokensConfig = RedisTokensConfig()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        cache_strings=False,
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        env_nested_delimiter="__",
        env_prefix="ENV__",
    )
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
