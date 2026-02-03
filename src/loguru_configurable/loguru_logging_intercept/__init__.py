"""This module is an adapted version of Loguru-logging-intercept, see
https://github.com/MatthewScholefield/loguru-logging-intercept

Original copyright:
(c) Matthew D. Scholefield 2021, licensed under MIT License.

Adaptations made by the loguru authors and the loguru_configurable authors
"""

from .loguru_logging_intercept import setup_loguru_logging_intercept

__all__ = [
    "setup_loguru_logging_intercept",
]
