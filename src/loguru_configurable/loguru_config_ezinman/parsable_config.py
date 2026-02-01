"""This module contains the ParsableConfiguration class for parsing configurations."""

import copy
import os
import re
import sys
from collections.abc import Callable, Collection
from re import Pattern
from typing import Any

from . import parsers

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

cfg_protocol = re.compile(r"^cfg://(.*)$")
word_regex = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*")

file_protocol = re.compile(r"^file://(.*)$")
literal_protocol = re.compile(r"^literal://(.*)$")
ext_protocol = re.compile(r"^ext://(.*)$")
env_var_protocol = re.compile(r"^env://(.*)$")

fmt_protocol = re.compile(r"^fmt://(.*)$")
format_value_regex = re.compile(r"(\{[^{}]+\}|[^{}]+)")


class ParsableConfiguration:
    """
    A configuration that can be parsed by the configuration loader. This class is used to load a configuration from a
    file or a dictionary, and then apply it to the logger.
    """

    __parsables__: Collection[str]
    """
    The names of the attributes that can be parsed by the configuration loader.
    """

    supported_protocol_parsers: Collection[
        tuple[Callable[[str], bool] | Pattern[Any], Callable[["ParsableConfiguration", str], str]]
    ]
    """
    The parsers that are supported by the configuration loader. The keys are the protocol parsers (either a callable
    that takes a string and returns a boolean, or a compiled regular expression); the values are the protocol parsers
    (callables that take a string and return a string).

    In case when a regex is used as a key, and the regex has a group, the group is used as the value to be passed to
    the protocol parser. Otherwise (a callable or no group in the regex), the entire string is passed to the protocol
    parser.
    """

    def __init__(self, **kwargs: dict[str, Any]):
        self.__dict__.update(kwargs)
        self.supported_protocol_parsers = list(self.supported_protocol_parsers)

    @classmethod
    def load(cls, config_dict: dict[str, Any], *, inplace: bool = False) -> Self:
        """
        Load a configuration from a dictionary.

        Parameters
        ----------
        config_dict : dict
            The configuration to load.

        inplace : bool, default False
            Whether modifications to the configuration should be made in-place. If False, a copy of the configuration
            is made before modifications are made.

        Returns
        -------
        parsed: ParsableConfiguration
            The loaded Parsable

        """

        if not inplace:
            config_dict = copy.deepcopy(config_dict)

        return cls(**config_dict)

    def parse(self) -> Self:
        """
        Parse the configuration. The parsed configuration is stored in the same object.
        """

        for key in self.__parsables__:
            if (value := getattr(self, key)) is None:
                continue
            setattr(self, key, self._recursive_parse(value))

        return self

    def _recursive_parse(self, element: dict[str, Any] | list[Any] | tuple[Any, ...] | str) -> Any:
        if isinstance(element, dict):
            if "()" in element:
                return parsers.parse_user_defined(element)
            return {k: self._recursive_parse(v) for k, v in element.items()}
        if isinstance(element, (list, tuple)):
            tp = type(element)
            return tp(self._recursive_parse(v) for v in element)
        if isinstance(element, str):
            return self._parse_string(element)
        return element

    def _parse_string(self, config_str: str) -> Any:
        result = None
        for cond, handler in self.supported_protocol_parsers:
            if isinstance(cond, str):
                cond = re.compile(cond)
            if isinstance(cond, Pattern):
                if match := cond.match(config_str):
                    # Check if it has groups, then take the first. Otherwise, pass the original string.
                    if match.groups():
                        result = handler(self, match.group(1))
                    else:
                        result = handler(self, config_str)
            elif callable(cond):
                if cond(config_str):
                    result = handler(self, config_str)
            else:
                raise TypeError(f"Condition must be a regex, or callable, not {type(cond)!r}.")

            if result is not None:
                # Even though we just loaded it, we allow it to be parsed further (as a string).
                return self._recursive_parse(result)

        return config_str

    def parse_format(self, format_str: str) -> str:
        """Parse a format string with embedded references."""
        # Split by { and } to get the parts that are not inside curly braces.
        parts = format_value_regex.split(format_str)
        for i, part in enumerate(parts):
            if part.startswith("{") and part.endswith("}"):
                part = parts[i] = part[1:-1]
                if part.startswith("{") and part.endswith("}"):
                    # This is an escaped curly brace part, so we skip it.
                    parts[i] = part[1:-1]
                else:
                    # This is a curly brace part, so we need to parse it.
                    parts[i] = str(self._parse_string(parts[i]))

        return "".join(parts)


ParsableConfiguration.supported_protocol_parsers = [
    (literal_protocol, lambda self, name: parsers.parse_literal(name)),
    (ext_protocol, lambda self, ref: parsers.parse_external(ref)),
    (env_var_protocol, lambda self, name: os.environ[name]),
    (cfg_protocol, parsers.parse_reference),
    (fmt_protocol, ParsableConfiguration.parse_format),
]
