from cafe.engine.models.data_interfaces import ConfigSectionInterface


class UserAuthConfig(ConfigSectionInterface):
    SECTION_NAME = 'auth'

    @property
    def endpoint(self):
        return self.get("endpoint")

    @property
    def serialize_format(self):
        return self.get("serialize_format", "json")

    @property
    def deserialize_format(self):
        return self.get("deserialize_format", "json")


class UserConfig(ConfigSectionInterface):
    SECTION_NAME = 'user'

    @property
    def username(self):
        return self.get("username")

    @property
    def password(self):
        return self.get_raw("password")

    @property
    def api_key(self):
        return self.get_raw("api_key")

    @property
    def tenant_id(self):
        return self.get("tenant_id")

    @property
    def tenant_name(self):
        return self.get("tenant_name")

    @property
    def token(self):
        return self.get("token")

    @property
    def endpoint(self):
        """Added to allow different users to auth at different endpoints.  For
        example the admin user needs to use an internal endpoint.
        """
        return self.get("endpoint")
