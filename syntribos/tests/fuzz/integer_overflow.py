# Copyright 2015 Rackspace
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


class IntOverflowBody(base_fuzz.BaseFuzzTestCase):
    test_name = "INT_OVERFLOW_BODY"
    test_type = "data"
    data_key = "integer-overflow.txt"

    def test_case(self):
        time_diff = self.config.time_difference_percent / 100
        if (self.resp.elapsed.total_seconds() >
                time_diff * self.init_response.elapsed.total_seconds()):
            self.register_issue(
                syntribos.Issue(
                    test="int_timing",
                    severity=syntribos.MEDIUM,
                    confidence=syntribos.MEDIUM,
                    text=("The time it took to resolve a request with an "
                          "invalid integer was too long compared to the "
                          "baseline request. This could indicate a "
                          "vulnerability to buffer overflow attacks"))
            )


class IntOverflowParams(IntOverflowBody):
    test_name = "INT_OVERFLOW_PARAMS"
    test_type = "params"


class IntOverflowHeaders(IntOverflowBody):
    test_name = "INT_OVERFLOW_HEADERS"
    test_type = "headers"


class IntOverflowURL(IntOverflowBody):
    test_name = "INT_OVERFLOW_URL"
    test_type = "url"
    url_var = "FUZZ"
