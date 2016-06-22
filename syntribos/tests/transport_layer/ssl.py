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
import os
import re

from six.moves.urllib.parse import urlparse

import syntribos
from syntribos.clients.http import client
from syntribos.clients.http import parser
from syntribos.tests import base


class SSLTestCase(base.BaseTestCase):

    test_name = "SSL"
    test_type = "headers"
    client = client()
    failures = []

    @classmethod
    def get_test_cases(cls, filename, file_content):

        request_obj = parser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT")
        )
        cls.resp = cls.client.send_request(request_obj)
        yield cls

    def test_case(self):

        target = self.resp.url
        domain = urlparse(target).hostname
        regex = r"\bhttp://{0}".format(domain)
        response_text = self.resp.text

        if re.search(regex, response_text):
            self.register_issue(
                syntribos.Issue(
                    test="SSL_ERROR",
                    severity=syntribos.MEDIUM,
                    confidence=syntribos.HIGH,
                    text=("Make sure that all the returned endpoint URIs"
                          " use 'https://' and not 'http://'"))
            )
