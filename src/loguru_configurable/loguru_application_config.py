"""Module that defines a Config for an application that uses loguru-configurable and no other application settings"""

from application_settings import ConfigBase, attributes_doc, dataclass

from loguru_configurable.config import LoguruConfigSection


@attributes_doc
@dataclass(frozen=True)
class LoguruApplicationConfig(ConfigBase):
    """Utility config class for applications that only use loguru-configurable and no other application-settings"""

    loguru_config: LoguruConfigSection = LoguruConfigSection()
    """The Loguru configuration section."""
