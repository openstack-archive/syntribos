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

from oslo_config import cfg

import syntribos
from syntribos._i18n import _
from syntribos.checks.header import cors
from syntribos.clients.http import client
from syntribos.clients.http import parser
from syntribos.tests import base


CONF = cfg.CONF


class CorsHeader(base.BaseTestCase):
    """Test for CORS wild character vulnerabilities in HTTP header."""

    test_name = "CORS_WILDCARD_HEADERS"
    test_type = "headers"
    client = client()
    failures = []

    @classmethod
    def get_test_cases(cls, filename, file_content):

        request_obj = parser.create_request(
            file_content, CONF.syntribos.endpoint
        )
        prepared_copy = request_obj.get_prepared_copy()
        cls.test_resp, cls.test_signals = cls.client.send_request(
            prepared_copy)
        yield cls

    def test_case(self):
        self.test_signals.register(cors(self))

        cors_slugs = [
            slugs for slugs in self.test_signals.all_slugs
            if "HEADER_CORS" in slugs]
        for slug in cors_slugs:
            if "ORIGIN" in slug:
                test_severity = syntribos.HIGH
            else:
                test_severity = syntribos.MEDIUM
            self.register_issue(
                defect_type="CORS_HEADER",
                severity=test_severity,
                confidence=syntribos.HIGH,
                description=(
                    _("CORS header vulnerability found.\n"
                      "Make sure that the header is not assigned "
                      "a wildcard character.")))
