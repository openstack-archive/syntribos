# Copyright 2016 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import syntribos
from syntribos._i18n import _
from syntribos.checks import has_string as has_string
from syntribos.checks import time_diff as time_diff
from syntribos.tests.fuzz import base_fuzz


class CommandInjectionBody(base_fuzz.BaseFuzzTestCase):
    """Test for command injection vulnerabilities in HTTP body."""

    test_name = "COMMAND_INJECTION_BODY"
    parameter_location = "data"
    data_key = "command_injection.txt"
    failure_keys = [
        'uid=',
        'root:',
        'default=',
        '[boot loader]']

    def test_case(self):
        self.run_default_checks()
        self.test_signals.register(has_string(self))
        if "FAILURE_KEYS_PRESENT" in self.test_signals:
            failed_strings = self.test_signals.find(
                slugs="FAILURE_KEYS_PRESENT")[0].data["failed_strings"]
            self.register_issue(
                defect_type="command_injection",
                severity=syntribos.HIGH,
                confidence=syntribos.MEDIUM,
                description=("A string known to be commonly returned after a "
                             "successful command injection attack was "
                             "included in the response. This could indicate "
                             "a vulnerability to command injection "
                             "attacks.").format(failed_strings))
        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="command_injection",
                severity=syntribos.HIGH,
                confidence=syntribos.MEDIUM,
                description=(_("The time elapsed between the sending of "
                               "the request and the arrival of the res"
                               "ponse exceeds the expected amount of time, "
                               "suggesting a vulnerability to command "
                               "injection attacks.")))


class CommandInjectionParams(CommandInjectionBody):
    """Test for command injection vulnerabilities in HTTP params."""

    test_name = "COMMAND_INJECTION_PARAMS"
    parameter_location = "params"


class CommandInjectionHeaders(CommandInjectionBody):
    """Test for command injection vulnerabilities in HTTP header."""

    test_name = "COMMAND_INJECTION_HEADERS"
    parameter_location = "headers"


class CommandInjectionURL(CommandInjectionBody):
    """Test for command injection vulnerabilities in HTTP URL."""

    test_name = "COMMAND_INJECTION_URL"
    parameter_location = "url"
    url_var = "FUZZ"
