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

from syntribos.checks.content_validity import valid_content


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


@requests_mock.Mocker()
class TestValidContent(testtools.TestCase):
    """Tests valid_content check for both valid and invalid json/xml."""

    def test_valid_json(self, m):
        text = u'{"text": "Sample json"}'
        headers = {"Content-type": "application/json"}
        m.register_uri("GET", "http://example.com", text=text, headers=headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = valid_content(test)
        self.assertEqual("VALID_JSON", signal.slug)

    def test_invalid_json(self, m):
        text = u'{"text""" "Sample json"}'
        headers = {"Content-type": "application/json"}
        m.register_uri("GET", "http://example.com", text=text, headers=headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = valid_content(test)
        self.assertEqual("INVALID_JSON", signal.slug)
        self.assertIn("APPLICATION_FAIL", signal.tags)

    def test_valid_xml(self, m):
        text = u"""<note>\n
                     <to>Tove</to>\n
                     <from>Jani</from>\n
                     <heading>Reminder</heading>\n
                     <body>Don't forget me this weekend!</body>\n
                     </note>"""
        headers = {"Content-type": "application/xml"}
        m.register_uri(
            "GET",
            "http://example.com",
            text=textwrap.dedent(text),
            headers=headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = valid_content(test)
        self.assertEqual("VALID_XML", signal.slug)

    def test_invalid_xml(self, m):
        text = u"""<xml version=='1.0' encoding==UTF-8'?>
                     <!DOCTYPE note SYSTEM 'Note.dtd'>
                     <note>
                     <to>Tove</to>
                     <from>Jani</from>
                     <heading>Reminder</heading>
                     <body>Don't forget me this weekend!</body>
                     html>"""
        headers = {"Content-type": "application/xml"}
        m.register_uri(
            "GET",
            "http://example.com",
            text=textwrap.dedent(text),
            headers=headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = valid_content(test)
        self.assertEqual("INVALID_XML", signal.slug)
        self.assertIn("APPLICATION_FAIL", signal.tags)
