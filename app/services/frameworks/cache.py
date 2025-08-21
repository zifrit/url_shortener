from redis import Redis
from core import config

cache_token_storage = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    decode_responses=True,
)
