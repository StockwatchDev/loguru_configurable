"""Do some logging to show the behavior of the configured logger"""

import config  # isort: skip  # pylint: disable=unused-import


import logging
import os
import sys

from loguru import logger
from my_module import do_logging


def main() -> int:
    """Dummy method to demonstrate logging"""

    # the loguru logger has been configured to intercept standard logging calls,
    # so this message will end up in the same place as loguru messages
    logging.error("Hay there.")

    do_logging()
    logger.success("Bye...")

    if sys.version_info >= (3, 11):
        return os.EX_OK
    return 0


if __name__ == "__main__":
    sys.exit(main())
