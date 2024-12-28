"""Module that defines two logging functions"""

import loguru


def do_logging(level: str) -> None:
    """Logs a message at the specified level without binding."""
    loguru.logger.log(level, "This is a log message without bind")


def do_logging_with_bind(level: str, context: str = "default") -> None:
    """Logs a message with an optional context binding."""
    loguru.logger.bind(context=context).log(level, "This is a log message with bind")
