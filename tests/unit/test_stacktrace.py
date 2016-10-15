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
import textwrap

import requests
import requests_mock
import testtools

from syntribos.checks.stacktrace import stacktrace


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


class TestStackTrace(testtools.TestCase):
    @requests_mock.Mocker()
    def test_stacktrace(self, m):
        text = """'Traceback (most recent call last):\n',
                File "<doctest...>", line 10, in <module>\n
                lumberjack()\n',
                File "<doctest...>", line 4, in lumberjack\n
                bright_side_of_death()\n',
                File "<doctest...>", line 7, in bright_side_of_death\n
                return tuple()[0]\n',
                'IndexError: tuple index out of range\n']"""

        m.register_uri("GET", "http://example.com", text=textwrap.dedent(text))
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = stacktrace(test)
        self.assertEqual("STACKTRACE_PRESENT", signal.slug)
        self.assertIn("APPLICATION_FAIL", signal.tags)
