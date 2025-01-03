# Install the package

`loguru_configurable` is available for [pypi](https://pypi.org/project/loguru_configurable/)
and can hence be installed with [pip](https://pypi.org/project/pip) or
[poetry](https://python-poetry.org). The package is not available on
[conda](https://docs.conda.io/en/latest/).

If you don't want to wait for a release and prefer to try the develop version, then you
can install from our repo.

=== "Windows"
    ```python
    # From pypi with pip:
    py -m pip install -U loguru_configurable

    # From pypi with poetry:
    poetry add loguru_configurable

    # From the repo with pip:
    py -m pip install git+https://github.com/StockwatchDev/loguru_configurable#develop

    # From the repo with poetry:
    poetry add git+https://github.com/StockwatchDev/loguru_configurable#develop
    ```

=== "Linux"
    ```python
    # From pypi:
    python -m pip install -U loguru_configurable

    # From pypi with poetry:
    poetry add loguru_configurable

    # From the repo with pip:
    python -m pip install git+https://github.com/StockwatchDev/loguru_configurable#develop

    # From the repo with poetry:
    poetry add git+https://github.com/StockwatchDev/loguru_configurable#develop
    ```

We have direct dependencies on the following packages:

- [application_settings](https://pypi.org/project/application_settings/)
- [loguru](https://pypi.org/project/loguru/)
- [loguru-config](https://pypi.org/project/loguru-config/)
- [loguru-logging-intercept](https://pypi.org/project/loguru-logging-intercept/)
