"""Capture Python's stdlib logging messages and route them to loguru"""

import inspect
import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """Logs to loguru from Python logging module

    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _parse_log_level(level_name: str) -> int:
    """Parse a log level name into a log level number"""
    if sys.version_info >= (3, 11):
        mapping = logging.getLevelNamesMapping()
        if (level := mapping.get(level_name.upper(), None)) is not None:
            return level
    else:
        if (
            level := logging._nameToLevel.get(level_name.upper(), None)  # pylint: disable=protected-access
        ) is not None:
            return level
    logger.warning(f"Unknown log level {level_name}, defaulting to DEBUG")
    return logging.DEBUG


def setup_loguru_logging_intercept(level: str = "DEBUG", modules: tuple[str, ...] | None = None) -> None:
    """Set up an interceptor routing messages to Loguru those specified in modules or, if no modules are specified, from
    the root logger.

    Parameters
    ----------
    level : int, optional
        The log level (as defined by Python's standard `logging`). Messages with this
        level or above will be forwarded to Loguru. By default 'DEBUG'.
    modules : tuple, optional
        A list of module names whose `logging` messages should be intercepted, by
        default None, which means only the root logger is intercepted.

    Example
    -------
    >>> setup_loguru_interceptor(modules=("my_module", "your_module.config"))
    """
    _level = _parse_log_level(level)
    _modules = modules or ("",)
    for logger_name in _modules:
        reported_logger = f" logger {logger_name}" if logger_name else "root logger"
        if logger_name:
            # undocumented way of getting a logger without creating it:
            if (mod_logger := logging.Logger.manager.loggerDict.get(logger_name)) and (
                isinstance(mod_logger, logging.Logger)
            ):
                mod_logger.handlers = [InterceptHandler(level=_level)]
                mod_logger.propagate = False
                logger.debug(f"InterceptHandler in place for {reported_logger}")
            else:
                logger.debug(f"No logger found named {logger_name}")
        else:
            # add intercept handler to root logger
            logging.basicConfig(handlers=[InterceptHandler()], level=_level, force=True)
            logger.debug(f"InterceptHandler in place for {reported_logger}")
