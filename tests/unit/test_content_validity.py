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


@requests_mock.Mocker()
class TestValidContent(testtools.TestCase):

    def test_valid_json(self, m):
        content = '{"text": "Sample json"}'
        headers = {"Content-type": "application/json"}
        m.register_uri("GET", "http://example.com",
                       content=content, headers=headers)
        resp = requests.get("http://example.com")
        signal = valid_content(resp)
        self.assertEqual("VALID_JSON", signal.slug)

    def test_invalid_json(self, m):
        content = '{"text""" "Sample json"}'
        headers = {"Content-type": "application/json"}
        m.register_uri("GET", "http://example.com",
                       content=content, headers=headers)
        resp = requests.get("http://example.com")
        signal = valid_content(resp)
        self.assertEqual("INVALID_JSON", signal.slug)
        self.assertIn("APPLICATION_FAIL", signal.tags)

    def test_valid_xml(self, m):
        content = """<note>\n
                     <to>Tove</to>\n
                     <from>Jani</from>\n
                     <heading>Reminder</heading>\n
                     <body>Don't forget me this weekend!</body>\n
                     </note>"""
        headers = {"Content-type": "application/xml"}
        m.register_uri("GET", "http://example.com",
                       content=textwrap.dedent(content), headers=headers)
        resp = requests.get("http://example.com")
        signal = valid_content(resp)
        self.assertEqual("VALID_XML", signal.slug)

    def test_invalid_xml(self, m):
        content = """<xml version=='1.0' encoding==UTF-8'?>
                     <!DOCTYPE note SYSTEM 'Note.dtd'>
                     <note>
                     <to>Tove</to>
                     <from>Jani</from>
                     <heading>Reminder</heading>
                     <body>Don't forget me this weekend!</body>
                     html>"""
        headers = {"Content-type": "application/xml"}
        m.register_uri("GET", "http://example.com",
                       content=textwrap.dedent(content), headers=headers)
        resp = requests.get("http://example.com")
        signal = valid_content(resp)
        self.assertEqual("INVALID_XML", signal.slug)
        self.assertIn("APPLICATION_FAIL", signal.tags)
