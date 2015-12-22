"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import cafe.engine.models.data_interfaces as data_interfaces


class EndpointConfig(data_interfaces.ConfigSectionInterface):
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


class UserConfig(data_interfaces.ConfigSectionInterface):
    SECTION_NAME = 'user'

    @property
    def username(self):
        return self.get("username")

    @property
    def password(self):
        return self.get_raw("password")

    @property
    def user_id(self):
        return self.get("user_id")

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
        """endpoint

        Added to allow different users to auth at different endpoints.  For
        example the admin user needs to use an internal endpoint.
        """
        return self.get("endpoint")

    @property
    def domain_id(self):
        return self.get("domain_id")

    @property
    def domain_name(self):
        return self.get("domain_name")
