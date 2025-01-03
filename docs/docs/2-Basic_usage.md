# Basic usage #

The `loguru_configurable` package is designed to simplify the configuration and integration of the `loguru` logging
library with additional features like routing standard logging calls and defining custom logging levels. This guide
explains how to use `loguru_configurable` in your Python application.

## Setting Up Configuration

### Configuration Module

Define a module to load and manage the configuration of your application. For example, `config.py`:

```python
from application_settings import ConfigBase, config_filepath_from_cli, dataclass
from loguru_configurable import LoguruConfigSection

@dataclass(frozen=True)
class ExampleConfig(ConfigBase):
    """Config for the application."""
    loguru_config: LoguruConfigSection = LoguruConfigSection()

# Load config.
config_filepath_from_cli(ExampleConfig, load=True)
```

This module uses `application_settings` to load the configuration from file.

### Configuration File

Create a `config.toml` file to configure your logging setup. Here is an example:

```toml
[loguru_config]
do_configure = true
intercept = true

activation = [["", "true"], ["my_module_1", "false"]]
patcher = "my_module_1.my_patcher"

[[loguru_config.handlers]]
sink = 'ext://sys.stderr'
level = 'INFO'
format = '<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>'

[[loguru_config.handlers]]
sink = './logs/file-{time}.log'
level = 'DEBUG'
format = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}'
enqueue = true
serialize = false

[[loguru_config.levels]]
name = 'NEW'
no = 13
icon = '¤'
color = ''

[[loguru_config.levels]]
name = 'OLD'
no = 31

[loguru_config.extra]
context = 'default'
```

This file defines:

- Handlers for console and file logging.
- Custom log levels (`NEW` and `OLD`).
- Extra context information.
- Interception of standard logging calls.

## Logging in the Application

### Main Script

Here's a main script (`__main__.py`) to demonstrate the logging behavior:

```python
# Ensure configuration is loaded first
import config  # pylint: disable=unused-import  # isort: skip

import sys
import my_module_1
import my_module_2
from loguru import logger

def main() -> None:
    """Dummy method to demonstrate logging."""
    logger.error("Hay there.")

    my_module_1.do_logging()
    my_module_2.do_logging("INFO")
    my_module_2.do_logging("NEW")
    my_module_2.do_logging("OLD")
    my_module_2.do_logging_with_bind("OLD", "not default")
    logger.debug("Bye...")

if __name__ == "__main__":
    sys.exit(main())
```

### Supporting Modules

#### `my_module_1.py`

```python
import datetime
import logging
import loguru

def my_patcher(record: loguru.Record) -> None:
    """Adds a UTC timestamp to the log record."""
    record["extra"].update(utc=datetime.datetime.now(datetime.timezone.utc))

def do_logging() -> None:
    """Logs a message at the specified level without binding."""
    loguru.logger.warning("This is a warning, sent to loguru")
    logging.warning("This is a warning, sent to the standard logger")
```

#### `my_module_2.py`

```python
import loguru

def do_logging(level: str) -> None:
    """Logs a message at the specified level without binding."""
    loguru.logger.log(level, "This is a log message without bind")

def do_logging_with_bind(level: str, context: str = "default") -> None:
    """Logs a message with an optional context binding."""
    loguru.logger.bind(context=context).log(level, "This is a log message with bind")
```

### Output Example

Depending on your `config.toml` settings, you will see:

- Logs in the console with the specified format.
- Logs written to files in the `./logs` directory.
- Custom log levels (`NEW`, `OLD`) displayed.
- Standard logging calls routed through `loguru`.
