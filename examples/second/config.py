"""File containing the config of the example."""

from application_settings import ConfigBase, config_filepath_from_cli, dataclass

from loguru_configurable import LoguruConfigSection


@dataclass(frozen=True)
class ExampleConfig(ConfigBase):
    """Config for loguru_configurable example with two loggers."""

    loguru_config_std: LoguruConfigSection = LoguruConfigSection()
    loguru_config_special: LoguruConfigSection = LoguruConfigSection()


# Load config.
config_filepath_from_cli(ExampleConfig, load=True)
