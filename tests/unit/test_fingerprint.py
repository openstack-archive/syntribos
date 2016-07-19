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
import requests
import requests_mock
import testtools

from syntribos.checks.fingerprint import remote_os
from syntribos.checks.fingerprint import server_software


class FakeInitSignals(object):
    def ran_check(self, check_name):
        pass


class FakeTestObject(object):
    """A class to generate fake test objects."""
    def __init__(self, resp):
        self.init_resp = resp
        self.init_req = resp.request
        self.test_resp = resp
        self.test_req = resp.request
        self.init_signals = FakeInitSignals()


class TestFingerprint(testtools.TestCase):

    @requests_mock.Mocker()
    def test_server_software_found(self, m):
        headers = {"Server": "WSGIServer"}
        m.register_uri("GET", "http://example.com", headers=headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = server_software(test)
        self.assertEqual("SERVER_SOFTWARE_WSGI", signal.slug)

    @requests_mock.Mocker()
    def test_server_software_not_found(self, m):
        m.register_uri("GET", "http://example.com")
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = server_software(test)
        self.assertEqual("SERVER_SOFTWARE_UNKNOWN", signal.slug)

    @requests_mock.Mocker()
    def test_remote_os_found(self, m):
        headers = {"X-Distribution": "Ubuntu"}
        m.register_uri("GET", "http://example.com", headers=headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = remote_os(test)
        self.assertEqual("SERVER_OS_UBUNTU", signal.slug)

    @requests_mock.Mocker()
    def test_remote_os_not_found(self, m):
        m.register_uri("GET", "http://example.com")
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = remote_os(test)
        self.assertEqual("SERVER_OS_UNKNOWN", signal.slug)
