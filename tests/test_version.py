"version tests"

from loguru_configurable import __version__


def test_version() -> None:
    """
    Test version
    """
    assert __version__ == "0.2.0"
