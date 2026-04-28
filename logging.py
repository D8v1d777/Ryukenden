import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(level=logging.INFO):
    """Sets up a structured logging system for Ryukenden."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    logger = logging.getLogger("ryukenden")
    logger.setLevel(level)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Production Grade)
    try:
        file_handler = RotatingFileHandler(
            "ryukenden.log", maxBytes=10485760, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to initialize file logging: {e}")

    return logger

def get_logger(module_name):
    """Returns a logger instance for a specific module."""
    return logging.getLogger(f"ryukenden.{module_name}")