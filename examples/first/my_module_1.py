"""Module that defines a logure patcher"""

from __future__ import annotations

import datetime
import logging

import loguru


def my_patcher(record: loguru.Record) -> None:
    """Adds a UTC timestamp to the log record."""

    record["extra"].update(utc=datetime.datetime.now(datetime.timezone.utc))


def do_logging() -> None:
    """Logs a message at the specified level without binding."""
    loguru.logger.warning("This is a warning, sent to loguru")
    logging.warning("This is a warning, sent to the standard logger")
