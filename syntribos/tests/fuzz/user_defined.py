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
from oslo_config import cfg

import syntribos
from syntribos.checks import has_string as has_string
from syntribos.checks import time_diff as time_diff
from syntribos.tests.fuzz import base_fuzz

CONF = cfg.CONF


class UserDefinedVulnBody(base_fuzz.BaseFuzzTestCase):
    """Test for user defined vulnerabilities in HTTP body."""

    test_name = "USER_DEFINED_VULN_BODY"
    test_type = "data"
    data_key = CONF.test.data_file
    failure_keys = CONF.test.failure_keys

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
                             "user defined attack."
                             ).format(failed_strings))

        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="user_defined_string_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.MEDIUM,
                description=("A response to one of the payload requests has "
                             "taken too long compared to the baseline "
                             "request. This could indicate a vulnerability "
                             "to time-based injection attacks using the user "
                             "provided strings."))


class UserDefinedVulnParams(UserDefinedVulnBody):
    """Test for user defined vulnerabilities in HTTP params."""

    test_name = "USER_DEFINED_VULN_PARAMS"
    test_type = "params"


class UserDefinedVulnHeaders(UserDefinedVulnBody):
    """Test for user defined vulnerabilities in HTTP header."""

    test_name = "USER_DEFINED_VULN_HEADERS"
    test_type = "headers"


class UserDefinedVulnURL(UserDefinedVulnBody):
    """Test for user defined vulnerabilities in HTTP URL."""

    test_name = "USER_DEFINED_VULN_URL"
    test_type = "url"
    url_var = "FUZZ"
