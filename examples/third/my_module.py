"""Module that logs to both loguru and the standard logging module."""

import logging

import loguru


def do_logging() -> None:
    """Logs a message at the specified level without binding."""
    loguru.logger.warning("This is a warning, sent to loguru")
    logging.info("This is an info message, sent to the standard logger")
