import logging
import os
from datetime import datetime


def setup_logger() -> logging.Logger:
    """
    Sets up and returns a logger that writes to a dated log file in the 'logs' folder.
    Log file is named after the current date and time: YYYY-MM-DD_HH-MM-SS.log
    """
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join("logs", f"{timestamp}.log")

    logger = logging.getLogger("CoCBot")
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler (keeps existing print-like output in terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logger initialized. Log file: {log_filename}")
    return logger
