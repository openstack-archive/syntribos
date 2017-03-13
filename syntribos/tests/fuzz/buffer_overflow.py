# Copyright 2016 Rackspace
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


class BufferOverflowBody(base_fuzz.BaseFuzzTestCase):
    """Test for buffer overflow vulnerabilities in HTTP body."""

    test_name = "BUFFER_OVERFLOW_BODY"
    test_type = "data"
    failure_keys = [
        '*** stack smashing detected ***:',
        'Backtrace:',
        'Memory map:',
    ]

    @classmethod
    def _get_strings(cls, file_name=None):
        return [
            "A" * (2 ** 16 + 1),
            "a" * 10 ** 5,
            "a" * 10 ** 6,
            '\x00' * (2 ** 16 + 1),
            "%%s" * 513,
        ]

    def test_case(self):
        self.run_default_checks()
        self.test_signals.register(has_string(self))
        if "FAILURE_KEYS_PRESENT" in self.test_signals:
            failed_strings = self.test_signals.find(
                slugs="FAILURE_KEYS_PRESENT")[0].data["failed_strings"]
            self.register_issue(
                defect_type="bof_strings",
                severity=syntribos.MEDIUM,
                confidence=syntribos.LOW,
                description=("The string(s): '{0}', known to be commonly "
                             "returned after a successful buffer overflow "
                             "attack, have been found in the response. This "
                             "could indicate a vulnerability to buffer "
                             "overflow attacks.").format(failed_strings))

        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="bof_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.MEDIUM,
                description=(_("The time it took to resolve a request with a "
                               "long string was too long compared to the "
                               "baseline request. This could indicate a "
                               "vulnerability to buffer overflow attacks")))


class BufferOverflowParams(BufferOverflowBody):
    """Test for buffer overflow vulnerabilities in HTTP params."""

    test_name = "BUFFER_OVERFLOW_PARAMS"
    test_type = "params"


class BufferOverflowHeaders(BufferOverflowBody):
    """Test for buffer overflow vulnerabilities in HTTP header."""

    test_name = "BUFFER_OVERFLOW_HEADERS"
    test_type = "headers"


class BufferOverflowURL(BufferOverflowBody):
    """Test for buffer overflow vulnerabilities in HTTP URL."""

    test_name = "BUFFER_OVERFLOW_URL"
    test_type = "url"
    url_var = "FUZZ"
