"""Do some logging to show the behavior of the configured logger"""

import config  # pylint: disable=unused-import  # isort: skip

import sys

import my_module_1
import my_module_2
from loguru import logger


def main() -> None:
    """Dummy method to demonstrate logging"""

    logger.error("Hay there.")

    my_module_1.do_logging()
    my_module_2.do_logging("INFO")
    my_module_2.do_logging("NEW")
    my_module_2.do_logging("OLD")
    my_module_2.do_logging_with_bind("OLD", "not default")
    logger.debug("Bye...")


if __name__ == "__main__":
    sys.exit(main())
