"""version test"""

from importlib.metadata import version as get_installed_version

from packaging.version import parse

from loguru_configurable import __version__


def test_version() -> None:
    """
    Verify that the package's internal __version__ matches the version
    declared in its installation metadata (from pyproject.toml). Semantic
    comparison via `packaging.version.parse` ensures equivalence.
    """

    assert parse(__version__) == parse(get_installed_version(distribution_name="loguru_configurable"))
