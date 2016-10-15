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

from syntribos.checks.ssl import https_check


class FakeInitSignals(object):
    def ran_check(self, name):
        pass


class FakeTestObject(object):
    """A class to generate fake test objects."""

    def __init__(self, resp):
        self.init_resp = resp
        self.init_req = resp.request
        self.test_resp = resp
        self.test_req = resp.request
        self.init_signals = FakeInitSignals()


class TestSSL(testtools.TestCase):
    @requests_mock.Mocker()
    def test_https_check(self, m):
        text = ("The first url is https://example.com/index.php & \n'"
                "the second url is http://example.com/index2.php/ ,"
                "thats all folks!")

        m.register_uri("GET", "http://example.com", text=text)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = https_check(test)
        self.assertEqual("HTTP_LINKS_PRESENT", signal.slug)
