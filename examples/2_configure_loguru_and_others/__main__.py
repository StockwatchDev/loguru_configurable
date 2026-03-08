"""Entry point for the loguru_configurable example where loguru is configured along with other libraries.

To run this example, from the root of the project execute
'poetry run python ./examples/2_configure_loguru_and_others -c ./examples/2_configure_loguru_and_others/config.toml'
"""

import sys

from main import main

sys.exit(main())
