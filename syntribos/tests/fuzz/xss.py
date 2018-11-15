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
from syntribos.checks import has_string as has_string
from syntribos.tests.fuzz import base_fuzz


class XSSBody(base_fuzz.BaseFuzzTestCase):
    """Test for cross-site-scripting vulnerabilities in HTTP body."""

    test_name = "XSS_BODY"
    parameter_location = "data"
    data_key = "xss.txt"

    def test_case(self):
        self.run_default_checks()
        self.failure_keys = self._get_strings()
        self.test_signals.register(has_string(self))

        if 'content-type' in self.init_req.headers:
            content_type = self.init_req.headers['content-type']
            if 'html' in content_type:
                sev = syntribos.MEDIUM
            else:
                sev = syntribos.LOW
        else:
            sev = syntribos.LOW
        if "FAILURE_KEYS_PRESENT" in self.test_signals:
            failed_strings = self.test_signals.find(
                slugs="FAILURE_KEYS_PRESENT")[0].data["failed_strings"]
            self.register_issue(
                defect_type="xss_strings",
                severity=sev,
                confidence=syntribos.LOW,
                description=("The string(s): '{0}', known to be commonly "
                             "returned after a successful XSS "
                             "attack, have been found in the response. This "
                             "could indicate a vulnerability to XSS "
                             "attacks.").format(failed_strings))
