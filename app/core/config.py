import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILM_DIR = BASE_DIR / "film_slugs.json"
SHORT_URL_DIR = BASE_DIR / "short_url_slugs.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# API_TOKENS = frozenset(
#     {
#         "h13uvxfgo21r2ZizTwIsep2UyLM",
#         "YVFuyt23pDfI-M7rXjguR9Oi0l4",
#     },
# )
#
# USERS = {
#     "bob": "bob",
#     "jim": "jim",
#     "admin": "admin",
# }


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2

REDIS_TOKENS_SET_NAME = "TOKENS_SET"
