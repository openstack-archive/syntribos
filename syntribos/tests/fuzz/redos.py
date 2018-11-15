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
import syntribos
from syntribos.checks import time_diff as time_diff
from syntribos.tests.fuzz import base_fuzz


class ReDosBody(base_fuzz.BaseFuzzTestCase):
    """Test for Regex DoS vulnerabilities in HTTP body."""

    test_name = "REDOS_BODY"
    parameter_location = "data"
    data_key = "redos.txt"

    def test_case(self):
        self.run_default_checks()
        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="redos_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.LOW,
                description=("A response to one of our payload requests has "
                             "taken too long compared to the baseline "
                             "request. This could indicate a vulnerability "
                             "to time-based Regex DoS attacks"))


class ReDosParams(ReDosBody):
    """Test for Regex DoS vulnerabilities in HTTP params."""

    test_name = "REDOS_PARAMS"
    parameter_location = "params"


class ReDosHeaders(ReDosBody):
    """Test for Regex DoS vulnerabilities in HTTP header."""

    test_name = "REDOS_HEADERS"
    parameter_location = "headers"


class ReDosURL(ReDosBody):
    """Test for Regex DoS vulnerabilities in HTTP URL."""

    test_name = "REDOS_URL"
    parameter_location = "url"
    url_var = "FUZZ"
