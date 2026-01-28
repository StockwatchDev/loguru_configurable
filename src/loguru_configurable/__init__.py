"""Entry point of the loguru_configurable library, collects all exportable items and disables logging by default."""

from loguru import logger

from loguru_configurable._version import __version__
from loguru_configurable.config import LoguruConfigSection, configure_logger

logger.disable("loguru_configurable")

__all__ = [
    "__version__",
    "configure_logger",
    "LoguruConfigSection",
]
