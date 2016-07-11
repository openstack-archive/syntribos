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

from syntribos.checks.header import cors


class FakeTestObject(object):
    """A class to generate fake test objects."""
    def __init__(self, resp):
        self.init_resp = resp
        self.init_req = resp.request
        self.test_resp = resp
        self.test_req = resp.request


class TestHeaders(testtools.TestCase):

    @requests_mock.Mocker()
    def test_cors_origin(self, m):
        cors_headers = {"Access-Control-Allow-Origin": "*"}

        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_ORIGIN_WILDCARD", signal.slug)

    @requests_mock.Mocker()
    def test_cors_origin_headers(self, m):
        cors_headers = {"Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*"}

        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_ORIGIN_HEADERS_WILDCARD", signal.slug)

    @requests_mock.Mocker()
    def test_cors_origin_methods(self, m):
        cors_headers = {"Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "*"}

        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_ORIGIN_METHODS_WILDCARD", signal.slug)

    @requests_mock.Mocker()
    def test_cors_headers_methods(self, m):
        cors_headers = {"Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"}

        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_METHODS_HEADERS_WILDCARD", signal.slug)

    @requests_mock.Mocker()
    def test_cors_origin_headers_methods(self, m):
        cors_headers = {"Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"}

        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_ORIGIN_METHODS_HEADERS_WILDCARD",
                         signal.slug)

    @requests_mock.Mocker()
    def test_cors_methods(self, m):
        cors_headers = {"Access-Control-Allow-Methods": "*"}
        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_METHODS_WILDCARD", signal.slug)

    @requests_mock.Mocker()
    def test_cors_headers(self, m):
        cors_headers = {"Access-Control-Allow-Headers": "*"}
        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertEqual("HEADER_CORS_HEADERS_WILDCARD", signal.slug)

    @requests_mock.Mocker()
    def test_not_cors_headers(self, m):
        cors_headers = {"Access-Control-Allow-Origin": "www.gg.com"}
        m.register_uri("GET", "http://example.com", headers=cors_headers)
        resp = requests.get("http://example.com")
        test = FakeTestObject(resp)
        signal = cors(test)
        self.assertIsNone(signal)
