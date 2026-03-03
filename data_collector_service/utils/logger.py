# Centralized logging setup
import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Thiết lập và trả về một logger tập trung.
    """
    logger = logging.getLogger(name)
    if not logger.handlers: # Tránh thêm handler nhiều lần
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
