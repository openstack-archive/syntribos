# Copyright 2016 Intel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from oslo_config import fixture as config_fixture


class ConfFixture(config_fixture.Config):
    """Fixture to fake config values."""

    def common_config_fixture(self):
        """common config values."""
        # TODO(unrahul): Add mock path for templates and payload dir
        self.conf.set_default("endpoint", "http://localhost",
                              group="syntribos")
        self.conf.set_default("exclude_results", ["500_errors"],
                              group="syntribos")
        self.conf.set_default("endpoint", "http://localhost", group="user")
        self.conf.set_default("username", "user", group="user")
        self.conf.set_default("password", "pass", group="user")
        self.conf.set_default("serialize_format", "json", group="user")
        self.conf.set_default("deserialize_format", "json", group="user")
        self.conf.set_default("enable_cache", True, group="remote")
        self.conf.set_default("cache_dir", "", group="remote")

    def v2_identity_fixture(self):
        """config values only applicable to keystone v2."""
        self.conf.set_default("tenant_name", "demo", group="user")
        self.conf.set_default("tenant_id", "1234", group="user")
        self.conf.set_default("version", "v2.0", group="user")

    def v3_identity_fixture(self):
        """config values only applicable to keysotne v3."""
        self.conf.set_default("project_name", "demo", group="user")
        self.conf.set_default("project_id", "1234", group="user")
        self.conf.set_default("domain_name", "default", group="user")
        self.conf.set_default("domain_id", "5678", group="user")
        self.conf.set_default("version", "v3", group="user")
        self.conf.set_default("token_ttl", 0, group="user")

    def test_config_fixture(self):
        """config values for test group."""
        self.conf.set_default("length_diff_percent", 1000.0, group="test")
        self.conf.set_default("time_diff_percent", 1000.0, group="test")
        self.conf.set_default("max_time", 10, group="test")
        self.conf.set_default("max_length", 500, group="test")

    def logger_config_fixture(self):
        """config values for logger group."""
        # TODO(unrahul): Add mock path for logdir
        self.conf.set_default("http_request_compression", True,
                              group="logging")

    def cli_config_fixture(self):
        """config values for CLI options(default group)."""
        # TODO(unrahul): Add mock file path for outfile
        self.conf.set_default("test_types", [""])
        self.conf.set_default("colorize", False)
        self.conf.set_default("output_format", "json")
        self.conf.set_default("min_severity", "LOW")
        self.conf.set_default("min_confidence", "LOW")

    def setUp(self):
        super(ConfFixture, self).setUp()
        self.common_config_fixture()
        self.v2_identity_fixture()
        self.v3_identity_fixture()
        self.test_config_fixture()
        self.logger_config_fixture()
        self.cli_config_fixture()
