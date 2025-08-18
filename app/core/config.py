import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILM_DIR = BASE_DIR / "film_slugs.json"
SHORT_URL_DIR = BASE_DIR / "short_url_slugs.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
