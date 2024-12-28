"""File containing the config and setup of the example."""

from application_settings import ConfigBase, config_filepath_from_cli, dataclass

from loguru_configurable import LoguruConfigSection


@dataclass(frozen=True)
class ExampleConfig(ConfigBase):
    """Config for async_server_cli app."""

    loguru_config: LoguruConfigSection = LoguruConfigSection()


# Load config.
config_filepath_from_cli(ExampleConfig, load=True)
