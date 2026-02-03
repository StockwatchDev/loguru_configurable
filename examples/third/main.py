"""Do some logging to show the behavior of the configured logger"""

from application_settings import config_filepath_from_cli  # isort: skip
from loguru_configurable import LoguruApplicationConfig  # isort: skip

config_filepath_from_cli(LoguruApplicationConfig, load=True)  # isort: skip

# pylint: disable=wrong-import-position
import logging
import os
import sys

from loguru import logger
from my_module import do_logging

# pylint: enable=wrong-import-position


def main() -> int:
    """Dummy method to demonstrate logging"""

    logging.error("Hay there.")

    do_logging()
    logger.success("Bye...")

    if sys.version_info >= (3, 11):
        return os.EX_OK
    return 0


if __name__ == "__main__":
    sys.exit(main())
