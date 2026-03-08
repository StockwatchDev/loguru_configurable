"""File containing the config of the example."""

from application_settings import ConfigBase, config_filepath_from_cli, dataclass

from loguru_configurable import LoguruConfigSection


@dataclass(frozen=True)
class ExampleConfig(ConfigBase):
    """Config for loguru_configurable example where loguru is configured along with other libraries."""

    loguru_config: LoguruConfigSection = LoguruConfigSection()
    # We can also have other config sections for other libraries or application items here.


# Load config.
config_filepath_from_cli(ExampleConfig, load=True)
