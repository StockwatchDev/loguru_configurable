"""Main module for the loguru_configurable example with two loggers."""

import config  # pylint: disable=unused-import  # isort: skip

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

    logger.info("Messages sent to the standard logger will end up on the screen.")
    logger_special.debug("Messages sent to the special logger will end up in a file.")
    logger.info("Bye...")
    logger_special.debug("Second message.")

    # We need to explicitly complete the (additional) loggers to ensure all messages are flushed
    # logger.complete()  # this one is not needed, it's done implicitly at program end
    logger_special.complete()

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
