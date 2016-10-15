# Copyright 2016 Rackspace
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

from syntribos.checks.string import has_string


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
        self.failure_keys = ["fail"]


class TestString(testtools.TestCase):
    @requests_mock.Mocker()
    def test_has_string(self, m):
        text = ("This is a server response, and its only job is to say:\n"
                "fail.")

        m.register_uri("GET", "http://example.com", text=text)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = has_string(test)
        self.assertEqual("FAILURE_KEYS_PRESENT", signal.slug)
        self.assertIn('fail', signal.data['failed_strings'])
        self.assertIn('fail', signal.text)
