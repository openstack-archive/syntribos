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
from syntribos.checks import https_check
from syntribos.tests import base


class SSLTestCase(base.BaseTestCase):

    """Test if response body contains non-https links."""

    test_name = "SSL_ENDPOINT_BODY"
    test_type = "body"

    def test_case(self):
        self.init_signals.register(https_check(self))

        if "HTTP_LINKS_PRESENT" in self.init_signals:
            self.register_issue(
                defect_type=_("SSL_ERROR"),
                severity=syntribos.MEDIUM,
                confidence=syntribos.HIGH,
                description=(_("Make sure that all the returned endpoint URIs"
                               " use 'https://' and not 'http://'")))
