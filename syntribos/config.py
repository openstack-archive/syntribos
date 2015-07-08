from cafe.engine.models.data_interfaces import ConfigSectionInterface


class BaseTestConfig(ConfigSectionInterface):
    SECTION_NAME = "syntribos"

    @property
    def endpoint(self):
        return self.get("endpoint")
