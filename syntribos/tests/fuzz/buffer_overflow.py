"""
Copyright 2016 Rackspace

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

from syntribos.issue import Issue
from syntribos.tests.fuzz import base_fuzz


class BufferOverflowBody(base_fuzz.BaseFuzzTestCase):
    test_name = "BUFFER_OVERFLOW_BODY"
    test_type = "data"
    data_key = "buffer-overflow.txt"
    failure_keys = [
        'fatal',
        'warning',
        'error',
        'exception',
        'fail',
        'not found',
        'unknown'
        ]

    @classmethod
    def _get_strings(cls, file_name=None):
        return [
            "A" * (2 ** 16 + 1),
            "%%s" * 513,
            "%d" % 0x7fffffff,
        ]

    def test_case(self):
        self.test_default_issues()
        failed_strings = self.data_driven_failure_cases()
        if failed_strings:
            self.register_issue(
                Issue(test="sql_strings",
                      severity="Medium",
                      confidence="Low",
                      text=("The string(s): \'{0}\', known to be commonly "
                            "returned after a successful buffer overflow "
                            "attack, have been found in the response. This "
                            "could indicate a vulnerability to buffer "
                            "overflow attacks.").format(failed_strings)
                      )
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
