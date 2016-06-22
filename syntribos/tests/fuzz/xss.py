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


class XSSBody(base_fuzz.BaseFuzzTestCase):
    test_name = "XSS_BODY"
    test_type = "data"
    data_key = "xss.txt"

    def test_case(self):
        self.test_default_issues()
        self.failure_keys = self._get_strings()
        failed_strings = self.data_driven_failure_cases()
        if 'content-type' in self.init_request.headers:
            content_type = self.init_request.headers['content-type']
            if 'html' in content_type:
                sev = syntribos.MEDIUM
            else:
                sev = syntribos.LOW
        else:
            sev = syntribos.LOW
        if failed_strings:
            self.register_issue(
                syntribos.Issue(
                    test="xss_strings",
                    severity=sev,
                    confidence=syntribos.LOW,
                    text=("The string(s): \'{0}\', known to be commonly "
                          "returned after a successful XSS "
                          "attack, have been found in the response. This "
                          "could indicate a vulnerability to XSS "
                          "attacks.").format(failed_strings))
            )
