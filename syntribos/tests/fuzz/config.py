from cafe.engine.models.data_interfaces import ConfigSectionInterface


class BaseFuzzConfig(ConfigSectionInterface):
    SECTION_NAME = "fuzz"

    @property
    def percent(self):
        return float(self.get("percent", 200.0))

    @property
    def string_fuzz_name(self):
        return self.get("string_fuzz_name", "FUZZ")
