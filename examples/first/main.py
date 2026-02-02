"""Do some logging to show the behavior of the configured logger"""

# Before any other imports, import the configuration
from loguru_configurable import LoguruApplicationConfig  # isort: skip

# And load the configuration settings from the CLI arguments
from application_settings import config_filepath_from_cli  # isort: skip

config_filepath_from_cli(LoguruApplicationConfig, load=True)  # isort: skip

# pylint: disable=wrong-import-position
import os
import sys

from loguru import logger

# pylint: enable=wrong-import-position


def main() -> int:
    """Dummy method to demonstrate logging"""

    logger.error("This is not really an error but a message to demonstrate logging.")
    logger.info("As an application user, you can configure what happens with log messages in the config file.")
    logger.info("Have a look at https://loguru.readthedocs.io/en/latest/overview.html for more details on loguru.")
    logger.info(
        "And for more info on how to configure, check out https://stockwatchdev.github.io/loguru_configurable/stable/"
    )
    logger.success("Bye...")

    if sys.version_info >= (3, 11):
        return os.EX_OK
    return 0


if __name__ == "__main__":
    sys.exit(main())
