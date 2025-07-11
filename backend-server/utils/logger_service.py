import logging
import sys
import json
from datetime import datetime


class StructuredFormatter(logging.Formatter):
    """JSON structured logging formatter"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry, ensure_ascii=False)


def setup_logger(name: str, level: str = "INFO", structured: bool = False) -> logging.Logger:
    """
    Setup production-ready logger

    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        structured: Use JSON structured logging
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="[%(levelname)s]: %(asctime)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """Get logger with default settings"""

    return setup_logger(name)
