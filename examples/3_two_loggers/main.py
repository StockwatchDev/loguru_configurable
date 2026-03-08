"""Main module for the loguru_configurable example with two loggers."""

import config  # isort: skip

import copy
import os
import sys

from loguru import logger

from loguru_configurable import configure_logger

# Create two loggers, see
# https://loguru.readthedocs.io/en/stable/resources/recipes.html#creating-independent-loggers-with-separate-set-of-handlers
# remove any default handlers
logger.remove()
# create a copy of the logger for the special logger
logger_special = copy.deepcopy(logger)
# configure std logger (you don't have to pass the logger, it uses the default one)
configure_logger(config.ExampleConfig.get().loguru_config_std)
# configure special logger
configure_logger(config.ExampleConfig.get().loguru_config_special, logger_to_configure=logger_special)


def main() -> int:
    """Main entry point for the loguru_configurable example with two loggers."""

    logger.info("Messages sent to the standard loguru logger will end up on the screen.")
    logger_special.debug("Messages sent to the special loguru logger will end up in a file.")
    logger.success("Bye...")
    logger_special.success("Second time bye.")

    # For the special logger, we have configured `enqueue=True` which means that the logger will use a background
    # thread to write log messages.
    # Hence, we need to call `complete` to make sure all log messages are written before the application exits,
    # otherwise we might lose some log messages.
    logger_special.complete()

    if sys.version_info >= (3, 11):
        return os.EX_OK
    return 0


if __name__ == "__main__":
    sys.exit(main())
