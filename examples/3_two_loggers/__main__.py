"""Entry point for the loguru_configurable example with two loggers.

To run this example, from the root of the project execute
'poetry run python ./examples/3_two_loggers -c ./examples/3_two_loggers/config.toml'
"""

import sys

from main import main

sys.exit(main())
