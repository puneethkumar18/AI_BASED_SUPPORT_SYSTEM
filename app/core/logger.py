import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("support_system")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_DIR / "application.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)