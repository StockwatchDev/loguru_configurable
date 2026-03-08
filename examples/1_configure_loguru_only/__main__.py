"""Entry point for the loguru_configurable example which configures loguru and nothing else.

To run this example, from the root of the project execute
'poetry run python ./examples/1_configure_loguru_only -c ./examples/1_configure_loguru_only/config.toml'
"""

import sys

from main import main

sys.exit(main())
