# Basic usage #

This guide explains how to use `loguru_configurable` in your Python application by means of a couple of examples.

## Simplest case: you want to configure loguru and nothing else ##

If you only want to configure `loguru` and nothing else, then you can use the config class that is defined in this
package. What is left to do is to write an appropriate config file, load the config from your application and add the
config file path as a command line option when you start your application.

### Step 1: define a config file ###

An overview of the items available for configuration is given in section [Configuration](3-Configuration.md). Each
section in your config file should start with `loguru_config`:

```toml
[loguru_config]
# apply the config after loading
do_configure = true

# activate loggers, e.g. the root logger
activation = [["", "true"]]

# send INFO and higher level log messages to stderr
[[loguru_config.handlers]]
sink = 'ext://sys.stderr'
level = 'INFO'
format = '<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>'

# write DEBUG and higher level log messages to file
[[loguru_config.handlers]]
sink = './logs/file-{time}.log'
level = 'DEBUG'
format = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}'
enqueue = true
serialize = false
```

## Setting Up Configuration ###

### Configuration Module ###

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

### Configuration File ###

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

## Logging in the Application ###

### Main Script ###

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

### Supporting Modules ###

#### `my_module_1.py` ####

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

#### `my_module_2.py` ####

```python
import loguru

def do_logging(level: str) -> None:
    """Logs a message at the specified level without binding."""
    loguru.logger.log(level, "This is a log message without bind")

def do_logging_with_bind(level: str, context: str = "default") -> None:
    """Logs a message with an optional context binding."""
    loguru.logger.bind(context=context).log(level, "This is a log message with bind")
```

### Output Example ###

Depending on your `config.toml` settings, you will see:

- Logs in the console with the specified format.
- Logs written to files in the `./logs` directory.
- Custom log levels (`NEW`, `OLD`) displayed.
- Standard logging calls routed through `loguru`.
