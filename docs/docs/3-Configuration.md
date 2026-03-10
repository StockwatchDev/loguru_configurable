# Configuration options #

This document provides a tabular overview of the configuration options available in the `loguru_configurable` module.

| Option              | Type                     | Default                         | Description                                                                 |
|---------------------|--------------------------|---------------------------------|-----------------------------------------------------------------------------|
| `inplace`           | `bool`                   | `False`                         | Whether modifications to the logger configuration should be made            |
|                     |                          |                                 | in-place. If `False`, a copy is made before applying modifications.         |
| `do_configure`      | `bool`                   | `False`                         | Whether to configure the logger after loading. Useful for modifying the     |
|                     |                          |                                 | `LoguruConfig` object before applying it.                                   |
| `activation`        | `list[tuple[str, bool]]` | `[('', True)]`                  | Activation config for `logger.add`. Contains `(logger_name, active)`        |
|                     |                          |                                 | tuples to specify which loggers are enabled.                                |
| `handlers`          | `list[dict[str, Any]]`   | Default Loguru handler config   | Handler configurations passed to `logger.add`. Defines where to send        |
|                     |                          |                                 | formatted log output.                                                       |
| `levels`            | `list[LoguruLevel]`      | `[]`                            | Custom log levels added to the standard levels.                             |
| `extra`             | `dict[str, Any]`         | `{}`                            | Default contents for the `extra` dictionary (used without `logger.bind`).   |
| `patcher`           | `str`                    | `''`                            | Name of a record‑patcher used with `logger.configure`. Converted to a       |
|                     |                          |                                 | callable if non‑empty.                                                      |
| `intercept`         | `bool`                   | `False`                         | Whether to intercept calls to Python’s standard `logging` module and        |
|                     |                          |                                 | forward them to Loguru.                                                     |
| `intercept_level`   | `str`                    | `'DEBUG'`                       | Minimum level of standard logging calls that will be intercepted.           |
| `intercept_modules` | `list[str]`              | `[]`                            | List of additional modules from which logging calls are intercepted.        |
