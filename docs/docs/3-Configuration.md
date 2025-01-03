# Configuration options #

This document provides a tabular overview of the configuration options available in the `loguru_configurable` module.

| Option       | Type | Default  | Description  |
|---------------------|--------------------|------------------|-----------------------------------|
| `inplace`    | `bool`     | `False`   | Whether modifications to the logger configuration should be made in-place. If False, a copy of the configuration is made before modifications are applied.     |
| `do_configure`      | `bool`     | `False`   | Whether to configure the logger after loading the configuration. If False, the configuration is loaded but not applied to the logger. Useful for modifying the LoguruConfig object before applying it to the logger.       |
| `activation` | `list[tuple[str, bool]]` | `[('', True)]`   | The activation configuration to be passed to `logger.add`. Contains tuples of `(logger_name, active)` indicating which loggers to activate.  |
| `handlers`   | `list[dict[str, Any]]`   | Default handler configuration of Loguru     | List of handler configurations specifying where to send formatted log messages. Each handler configuration is passed to `logger.add`. Defaults to the default handler configuration of loguru.  |
| `levels`     | `list[LoguruLevel]`      | `[]`     | A list of custom log levels to add to the standard levels.   |
| `extra`      | `dict[str, Any]`  | `{}`     | The default contents of the `extra` dictionary (without calling `logger.bind`).       |
| `patcher`    | `str`     | `''`    | Specifies the record-patcher parameter in `logger.configure`. Functions like `logger.patch`. Converts the string (if not empty) to a `Callable[[loguru.Record], None]`.       |
| `intercept`  | `bool`   | `False`  | Whether to intercept calls to Python's standard `logging` module and route them to loguru.   |
| `intercept_level`   | `str`    | `'DEBUG'`    | This level of calls to standard logging and above will be intercepted and routed to loguru. Valid values are `'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, and `'CRITICAL'`.   |
| `intercept_modules` | `list[str]`     | `[]`    | A list of additional modules to intercept logging calls from.  |
