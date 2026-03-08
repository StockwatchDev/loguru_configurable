"""Module that defines a ConfigSection for loguru, defines a function to configure loguru
and uses loguru-logging-intercept to re-route standard logging calls"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import asdict, field
from typing import TYPE_CHECKING, Any, Protocol, cast

from application_settings import ConfigSectionBase, attributes_doc, dataclass
from loguru import logger

from .loguru_config_ezinman.loguru_config import LoguruConfig
from .loguru_config_ezinman.parsers import parse_external
from .loguru_logging_intercept import setup_loguru_logging_intercept

if TYPE_CHECKING:
    from loguru import Logger, Record


@attributes_doc
@dataclass(frozen=True)
class LoguruLevel:
    """Defines a loguru log level"""

    name: str
    """Name of the logging level"""

    no: int
    """The severity of the level"""

    color: str = ""
    """The color markup of the level; defaults to ''"""

    icon: str = ""
    """The icon of the level; defaults to ''"""


def _adheres_to_patcher_protocol(imported_patcher: Callable[["Record"], None]) -> bool:

    if not callable(imported_patcher):
        logger.debug(f"{imported_patcher.__name__} is not a Callable")
        return False

    parameter_classes = [p.annotation for p in inspect.signature(imported_patcher).parameters.values()]
    if len(parameter_classes) != 1:
        logger.debug(f"{imported_patcher.__name__} does not have a single argument")
        return False

    if parameter_classes[0] != "loguru.Record":
        logger.debug(f"Single argument of {imported_patcher.__name__} is not a loguru.Record")
        return False

    if str(inspect.signature(imported_patcher).return_annotation) != "None":
        logger.debug(f"{imported_patcher.__name__} does not return None")
        return False

    logger.debug(f"{imported_patcher.__name__} meets the required protocol: Callable[[loguru.Record], None]")
    return True


def configure_logger(
    loguru_config_section: LoguruConfigSection, logger_to_configure: "Logger" | None = None
) -> list[int]:
    """
    Configure the logger_to_configure with the passed configuration.

    Returns
    -------
        The IDs of the handlers that were added to the logger.
    """
    _logger = logger if logger_to_configure is None else logger_to_configure
    if (
        parsed_config := LoguruConfig.load(
            loguru_config_section.as_config_dict(), inplace=loguru_config_section.inplace
        )
    ) is None:
        logger.error("Loguru configuration failed; parsed configuration is None")
        return []
    return parsed_config.configure(logger_to_configure=_logger)  # pylint: disable=no-member


def default_handlers() -> Callable[[], list[dict[str, Any]]]:
    """Returns a default handler field for LoguruConfigSection.handlers; equals the default handler of loguru"""

    return lambda: [
        {
            "sink": "ext://sys.stderr",
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": "DEBUG",
        }
    ]


class PatcherProtocol(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol class for a function argument for loguru.patch"""

    def __call__(self, record: "Record") -> None: ...


@attributes_doc
@dataclass(frozen=True)
class LoguruConfigSection(ConfigSectionBase):  # pylint: disable=too-many-instance-attributes
    """ConfigSection for loguru-config"""

    inplace: bool = False
    """Whether modifications to the logger configuration should be made in-place. If False, a copy of the configuration
    is made before modifications are made. Defaults to False."""

    do_configure: bool = False
    """Whether to configure the logger after loading the configuration. If False, the configuration is loaded but
    not applied to the logger. This is useful if you want to have more control over when to apply the configuration
    to the logger, e.g. if you have multiple loggers. Defaults to False."""

    activation: list[tuple[str, bool]] = field(default_factory=lambda: [("", True)])
    """The activation configuration to be passed to `logger.add`. The sequence contains tuples of the form
    `(logger_name, active)`, where `logger_name` is the name of the logger to activate, and `active` is a boolean
    indicating whether the logger should be active or not; defaults to a list containing a single tuple to activate
    the root logger."""

    handlers: list[dict[str, Any]] = field(default_factory=default_handlers())
    """List of handlers to use. Each handler is given as a dict with parameters that configure the handler.
    The 'sink' parameter is mandatory and specifies where to send the formatted log messages. The handler
    configurations are passed to `logger.add` as keyword arguments. See the examples
    folder for examples. For more info on handler parameters refer to
    [the logure docs](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add).
    Defaults to the default handler configuration of loguru."""

    levels: list[LoguruLevel] = field(default_factory=lambda: [])
    """A list of loguru logging levels, to add to the standard levels; defaults to an empty list."""

    extra: dict[str, Any] = field(default_factory=lambda: {})
    """The default contents of the `extra` dictionary (without calling `logger.bind`); defaults to an empty dict."""

    patcher: str = ""
    """Specifies the record-patcher parameter in `logger.configure` that functions like `logger.patch`;
    post-init converts the string (if not empty) to a Callable[[loguru.Record], None]; defaults to ''."""

    intercept: bool = False
    """Whether to intercept calls to Python's standard `logging` module and route them to loguru; defaults to False."""

    intercept_level: str = "DEBUG"
    """This level of calls to standard logging and above will be intercepted and routed to loguru; defaults to 'DEBUG'.
    This is only used if `intercept` is True. Valid values: 'DEBUG', 'WARNING', 'INFO', 'ERROR' and 'CRITICAL'.
    """

    intercept_modules: list[str] = field(default_factory=lambda: [])
    """A list of modules to intercept calls from, in addition to the root logger (which is always intercepted if
    intercept is True); defaults to an empty list."""

    def __post_init__(self) -> None:
        if self.do_configure:
            configure_logger(self)
            logger.debug("Loguru config applied.")
        if self.intercept:
            logger.debug("Intercepting standard logging calls...")
            setup_loguru_logging_intercept(level=self.intercept_level, modules=tuple(self.intercept_modules))

    def _patcher(self) -> PatcherProtocol | None:
        if not self.patcher:
            return None
        imported_patcher = parse_external(self.patcher)
        if not _adheres_to_patcher_protocol(imported_patcher):
            raise TypeError(f"{self.patcher} is not a Callable[[loguru.Record], None]")
        return cast(PatcherProtocol, imported_patcher)

    def as_config_dict(self) -> dict[str, Any]:
        """Returns the configuration as a dict suitable for passing to `logger.configure`"""
        loguru_config_dict = asdict(self)
        loguru_config_dict.pop("inplace")
        loguru_config_dict.pop("do_configure")
        loguru_config_dict.pop("patcher")
        loguru_config_dict.pop("intercept")
        loguru_config_dict.pop("intercept_level")
        loguru_config_dict.pop("intercept_modules")
        if imported_patcher := self._patcher():
            loguru_config_dict["patcher"] = imported_patcher
        logger.trace(f"{loguru_config_dict = }")
        return loguru_config_dict
