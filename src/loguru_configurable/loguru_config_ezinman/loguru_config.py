"""Definition of the LoguruConfigEZinman class, which can parse a configuration for the loguru logger."""

import sys
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from .parsable_config import ParsableConfiguration

if TYPE_CHECKING:
    from loguru import LevelConfig, Logger, Record

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class LoguruConfig(ParsableConfiguration):
    """
    A configuration for the loguru logger. This class is used to load a configuration from a file or a dictionary,
    and then apply it to the logger. The structure of the configuration is taken from `loguru`'s `logger.configure`
    method.

    See [1] for more information on the structure of the configuration.

    References
    ----------
    [1] https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.configure

    Parameters
    ----------
    handlers : Sequence[Dict[str, Any]]
        The handlers to use. The keys are the names of the handlers, and the values are the handler configurations.
        The handler configurations are passed to `logger.add` as keyword arguments.

    levels : Sequence[LevelConfig]] optional
        The levels to use. This is a sequence of dictionaries, where each dictionary is passed to `logger.level` as
        keyword arguments. The dictionaries contain the keys `name`, `no` (number), `color`, `icon`.

    extra : dict, optional
        The default contents of the `extra` dictionary (without calling `logger.bind`).

    patcher : Callable[[Record], None], optional
        The record-patcher function to be passed to `logger.patch`.

    activation : Sequence[Tuple[Optional[str], bool]], optional
        The activation configuration to be passed to `logger.add`. The sequence contains tuples of the form
        `(logger_name, active)`, where `logger_name` is the name of the logger to activate, and `active` is a boolean
        indicating whether the logger should be active or not.

    """

    __parsables__ = ["handlers", "levels", "extra", "patcher", "activation"]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        handlers: Sequence[dict[str, Any]] | None = None,
        levels: Sequence["LevelConfig"] | None = None,
        extra: dict[str, Any] | None = None,
        patcher: Callable[["Record"], None] | None = None,
        activation: Sequence[tuple[str | None, bool]] | None = None,
    ):
        self.handlers = handlers
        self.levels = levels
        self.extra = extra
        self.patcher = patcher
        self.activation = activation
        super().__init__()

    @classmethod
    def load(
        cls,
        config_dict: dict[str, Any],
        *,
        inplace: bool = False,
    ) -> Self:
        """
        Load a configuration from a file or a dictionary.

        Parameters
        ----------
        config_or_file : dict
            The configuration to load. If a string, it is interpreted as a path to a file.
            If a dictionary, it is interpreted as a configuration dictionary.

        inplace : bool, default False
            Whether modifications to the configuration should be made in-place. If False, a copy of the configuration
            is made before modifications are made.

        configure : bool, optional
            Whether to configure the logger after loading the configuration. If False, the configuration is loaded but
            not applied to the logger. This is useful if you want to load the configuration and then modify it before
            applying it to the logger.

        Returns
        -------
        config: Optional[LoguruConfig]
            The loaded configuration. If `configure` is True, returns None.

        """

        return super().load(config_dict, inplace=inplace).parse()

    def configure(self, logger_to_configure: "Logger") -> list[int]:
        """
        Configure the logger with the loaded configuration.

        Returns
        -------
        list[int]
            The IDs of the handlers that were added to the logger.
        """

        return logger_to_configure.configure(
            handlers=self.handlers,  # type: ignore[arg-type]
            levels=self.levels,
            extra=self.extra,
            patcher=self.patcher,
            activation=self.activation,
        )
