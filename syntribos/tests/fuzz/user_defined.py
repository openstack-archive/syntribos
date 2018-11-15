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
import os

from oslo_config import cfg

import syntribos
from syntribos._i18n import _
from syntribos.checks import has_string as has_string
from syntribos.checks import time_diff as time_diff
from syntribos.tests.fuzz import base_fuzz

CONF = cfg.CONF


def user_defined_config():
    """Create config options for user defined test."""
    user_defined_group = cfg.OptGroup(
        name="user_defined", title="Data for user defined test")
    CONF.register_group(user_defined_group)
    options = [
        cfg.StrOpt(
            "payload", help="Path to a payload data file."), cfg.StrOpt(
                "failure_keys", help="Possible failure keys")
    ]
    CONF.register_opts(options, group=user_defined_group)


class UserDefinedVulnBody(base_fuzz.BaseFuzzTestCase):
    """Test for user defined vulnerabilities in HTTP body."""

    test_name = "USER_DEFINED_VULN_BODY"
    parameter_location = "data"
    user_defined_config()
    data_key = CONF.user_defined.payload
    failure_keys = CONF.user_defined.failure_keys

    def test_case(self):
        self.run_default_checks()
        self.test_signals.register(has_string(self))
        if "FAILURE_KEYS_PRESENT" in self.test_signals:
            failed_strings = self.test_signals.find(
                slugs="FAILURE_KEYS_PRESENT")[0].data["failed_strings"]
            self.register_issue(
                defect_type="user_defined_strings",
                severity=syntribos.MEDIUM,
                confidence=syntribos.LOW,
                description=("The string(s): '{0}', is in the list of "
                             "possible vulnerable keys. This may "
                             "indicate a vulnerability to this form of "
                             "user defined attack.").format(failed_strings))

        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="user_defined_string_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.LOW,
                description=(_("A response to one of the payload requests has "
                               "taken too long compared to the baseline "
                               "request. This could indicate a vulnerability "
                               "to time-based injection attacks using the user"
                               " provided strings.")))

    @classmethod
    def get_test_cases(cls, filename, file_content, meta_vars):
        """Generates test cases if a payload file is provided."""
        conf_var = CONF.user_defined.payload
        if conf_var is None or not os.path.isfile(conf_var):
            return
        cls.failures = []
        prefix_name = "{filename}_{test_name}_{fuzz_file}_".format(
            filename=filename,
            test_name=cls.test_name,
            fuzz_file=cls.data_key)
        fr = syntribos.tests.fuzz.datagen.fuzz_request(
            cls.init_req, cls._get_strings(), cls.parameter_location,
            prefix_name)
        for fuzz_name, request, fuzz_string, param_path in fr:
            yield cls.extend_class(fuzz_name, fuzz_string, param_path,
                                   {"request": request})


class UserDefinedVulnParams(UserDefinedVulnBody):
    """Test for user defined vulnerabilities in HTTP params."""

    test_name = "USER_DEFINED_VULN_PARAMS"
    parameter_location = "params"


class UserDefinedVulnHeaders(UserDefinedVulnBody):
    """Test for user defined vulnerabilities in HTTP header."""

    test_name = "USER_DEFINED_VULN_HEADERS"
    parameter_location = "headers"


class UserDefinedVulnURL(UserDefinedVulnBody):
    """Test for user defined vulnerabilities in HTTP URL."""

    test_name = "USER_DEFINED_VULN_URL"
    parameter_location = "url"
    url_var = "FUZZ"
