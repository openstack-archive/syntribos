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
import textwrap

import requests
import requests_mock
import testtools

from syntribos.checks.header import xst


class FakeInitSignals(object):
    def ran_check(self, name):
        pass


class FakeTestObject(object):
    """A class to generate fake test objects."""

    def __init__(self, resp):
        self.init_req = "TRACE / HTTP/1.1"
        self.init_resp = resp
        self.test_req = "TRACE /<script>foo()</script> HTTP/1.1"
        self.test_resp = resp
        self.init_signals = FakeInitSignals()


class TestStackTrace(testtools.TestCase):
    @requests_mock.Mocker()
    def test_stacktrace(self, m):
        text = """
        HTTP/1.1 200 OK
        Date: Thu, 02 Feb 2017 17: 15 GMT\n',
        Content-type: application/xml\n',
        Transfer-Encoding: chunked\n',
        Server: Apache,
        \r\n
        TRACE /<script>foo()/</script> HTTP/1.1
        HOST: xyz
        X-Wing: <script>bar()</script>\n
        TRACE_THIS: XST_Vuln"""

        m.register_uri("TRACE",
                       "http://example.com",
                       text=textwrap.dedent(text))
        resp = requests.request("TRACE", "http://example.com")
        test = FakeTestObject(resp)
        signal = xst(test)
        self.assertEqual("HEADER_XST", signal.slug)
