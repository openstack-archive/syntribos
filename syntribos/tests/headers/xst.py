# Copyright 2017 Intel
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
from syntribos.checks.header import xst
from syntribos.clients.http import client
from syntribos.clients.http import parser
from syntribos.tests import base


CONF = cfg.CONF


class XstHeader(base.BaseTestCase):
    """Test for Cross Site Tracing vulnerabilities.

    A TRACE request with a fake request is sent to the server,
    if the server responds back with the entire request flow
    as a reponse, this can be termed a vulnerability. All TRACE
    requests should be vetted and filtered by the server to
    prevent accidental leakage of cookies, etc. If an app is
    already vulnerable to XSS attacks, then this can enable an
    attacker to steal session cookies.

    :more: https://www.owasp.org/index.php/Cross_Site_Tracing
    """

    test_name = "XST_HEADERS"
    test_type = "headers"
    client = client()
    failures = []

    @classmethod
    def get_test_cases(cls, filename, file_content):
        xst_header = {"TRACE_THIS": "XST_Vuln"}
        request_obj = parser.create_request(
            file_content, CONF.syntribos.endpoint, meta_vars=None)
        prepared_copy = request_obj.get_prepared_copy()
        prepared_copy.method = "TRACE"
        prepared_copy.headers.update(xst_header)
        cls.test_resp, cls.test_signals = cls.client.send_request(
            prepared_copy)
        yield cls

    def test_case(self):
        self.test_signals.register(xst(self))

        xst_slugs = [
            slugs for slugs in self.test_signals.all_slugs
            if "HEADER_XST" in slugs]
        for i in xst_slugs:  # noqa
            test_severity = syntribos.LOW
            self.register_issue(
                defect_type="XST_HEADER",
                severity=test_severity,
                confidence=syntribos.HIGH,
                description=(_("XST vulnerability found.\n"
                               "Make sure that response to a "
                               "TRACE request is filtered.")))
