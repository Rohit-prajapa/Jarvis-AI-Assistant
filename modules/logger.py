"""
modules/logger.py
-----------------
Logging System for Jarvis.
"""

import logging
import os


LOG_FOLDER = "logs"
LOG_FILE = os.path.join(
    LOG_FOLDER,
    "jarvis.log"
)


# Create logs directory
os.makedirs(
    LOG_FOLDER,
    exist_ok=True
)


# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_info(message):
    """Save an information message."""

    logging.info(message)


def log_error(message):
    """Save an error message."""

    logging.error(message)


def log_warning(message):
    """Save a warning message."""

    logging.warning(message)