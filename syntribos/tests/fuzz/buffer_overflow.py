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
from syntribos.tests.fuzz import base_fuzz


class BufferOverflowBody(base_fuzz.BaseFuzzTestCase):
    test_name = "BUFFER_OVERFLOW_BODY"
    test_type = "data"
    data_key = "buffer-overflow.txt"
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
        self.test_default_issues()
        failed_strings = self.data_driven_failure_cases()
        if failed_strings:
            self.register_issue(
                syntribos.Issue(
                    test="bof_strings",
                    severity=syntribos.MEDIUM,
                    confidence=syntribos.LOW,
                    text=("The string(s): \'{0}\', known to be commonly "
                          "returned after a successful buffer overflow "
                          "attack, have been found in the response. This "
                          "could indicate a vulnerability to buffer "
                          "overflow attacks.").format(failed_strings))
            )
        time_diff = self.config.time_difference_percent / 100
        if (self.resp.elapsed.total_seconds() >
                time_diff * self.init_response.elapsed.total_seconds()):
            self.register_issue(
                syntribos.Issue(
                    test="bof_timing",
                    severity=syntribos.MEDIUM,
                    confidence=syntribos.MEDIUM,
                    text=("The time it took to resolve a request with a "
                          "long string was too long compared to the "
                          "baseline request. This could indicate a "
                          "vulnerability to buffer overflow attacks"))
            )


class BufferOverflowParams(BufferOverflowBody):
    test_name = "BUFFER_OVERFLOW_PARAMS"
    test_type = "params"


class BufferOverflowHeaders(BufferOverflowBody):
    test_name = "BUFFER_OVERFLOW_HEADERS"
    test_type = "headers"


class BufferOverflowURL(BufferOverflowBody):
    test_name = "BUFFER_OVERFLOW_URL"
    test_type = "url"
    url_var = "FUZZ"
