"""Utility module for the application.

This module contains utility functions used throughout the application.
"""

import logging
from functools import lru_cache
from typing import Final

from rich.console import Console
from rich.logging import RichHandler

from src.core.config import settings


class Logger:
    """A singleton logger class for the application.

    This class implements a singleton pattern to ensure only one logger instance
    exists throughout the application lifetime. It uses Rich for beautiful console
    output and proper formatting.

    Example:
        >>> logger = Logger.get_instance()
        >>> logger.info("Application started")
        >>> logger.error("An error occurred", exc_info=True)
    """

    _INSTANCE: Final[logging.Logger] = logging.getLogger("rich")

    def __init__(self) -> None:
        """Initialize the logger configuration.

        This should not be called directly. Use get_instance() instead.
        """
        raise RuntimeError("Use get_instance() instead")

    @classmethod
    @lru_cache(maxsize=1)
    def get_instance(cls) -> logging.Logger:
        """Get the singleton logger instance.

        This method ensures that only one logger instance is created and configured
        throughout the application lifetime.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, console=Console(width=127))],
            force=True,
        )
        return cls._INSTANCE


# Convenience function for getting the logger
def get_logger() -> logging.Logger:
    """Get the application logger instance.

    This is a convenience function that returns the singleton logger instance.
    It's the recommended way to get the logger throughout the application.

    Returns:
        logging.Logger: The configured logger instance.

    Example:
        >>> logger = get_logger()
        >>> logger.info("Starting process...")
        >>> logger.debug("Debug information")
    """
    return Logger.get_instance()
