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
from syntribos._i18n import _
from syntribos.checks import has_string as has_string
from syntribos.checks import time_diff as time_diff
from syntribos.tests.fuzz import base_fuzz


class JSONDepthOverflowBody(base_fuzz.BaseFuzzTestCase):
    """Test for json depth overflow in HTTP body."""

    test_name = "JSON_DEPTH_OVERFLOW_BODY"
    test_type = "data"
    failure_keys = [
        "maximum recursion depth exceeded",
        "RuntimeError",
    ]

    @classmethod
    def _get_strings(cls, file_name=None):
        return [
            '{"id":' * 1000 + '42' + '}' * 1000,
            '{"id":' * 10000 + '4242' + '}' * 10000
        ]

    def test_case(self):
        self.run_default_checks()
        self.test_signals.register(has_string(self))
        if "FAILURE_KEYS_PRESENT" in self.test_signals:
            failed_strings = self.test_signals.find(
                slugs="FAILURE_KEYS_PRESENT")[0].data["failed_strings"]
            self.register_issue(
                defect_type="json_depth_limit_strings",
                severity=syntribos.MEDIUM,
                confidence=syntribos.HIGH,
                description=(
                    "The string(s): '{0}', is known to be commonly "
                    "returned after a successful overflow of the json"
                    " parsers depth limit. This could possibly "
                    "result in a dos vulnerability.").format(failed_strings))

        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="json_depth_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.MEDIUM,
                description=(_("The time it took to resolve a request "
                               "was too long compared to the "
                               "baseline request. This could indicate a "
                               "vulnerability to denial of service attacks.")))
