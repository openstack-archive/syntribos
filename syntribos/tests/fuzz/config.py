from cafe.engine.models.data_interfaces import ConfigSectionInterface


class BaseFuzzConfig(ConfigSectionInterface):
    SECTION_NAME = "FUZZ"

    @property
    def percent(self):
        return self.get("percent")

    @property
    def string_fuzz_name(self):
        return self.get("string_fuzz_name", "FUZZ")
