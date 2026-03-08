"""Module that defines a Config for an application that uses loguru-configurable and no other application settings"""

from application_settings import ConfigBase, attributes_doc, config_filepath_from_cli, dataclass

from loguru_configurable.config import LoguruConfigSection


@attributes_doc
@dataclass(frozen=True)
class LoguruApplicationConfig(ConfigBase):
    """Utility config class for applications that only use loguru-configurable and no other application-settings"""

    loguru_config: LoguruConfigSection = LoguruConfigSection()
    """The Loguru configuration section."""


def configure_application_for_loguru() -> None:
    """Configure loguru only with the settings from the config file."""
    config_filepath_from_cli(LoguruApplicationConfig, load=True)
