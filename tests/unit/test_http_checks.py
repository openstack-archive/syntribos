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
# import requests
import requests.exceptions as rex
import requests_mock
import testtools

import syntribos.checks.http as http_checks
import syntribos.clients.http.client as client
import syntribos.signal

client = client()


class HTTPCheckUnittest(testtools.TestCase):

    def _get_one_signal(self, signals, slug=None, tags=None):
        to_search = None

        if isinstance(signals, syntribos.signal.SynSignal):
            to_search = signals

        elif isinstance(signals, syntribos.signal.SignalHolder):
            slugs = [slug] if slug else None
            matching = signals.find(slugs=slugs, tags=tags)
            self.assertEqual(1, len(matching))
            to_search = matching[0]

        return to_search

    def _assert_has_slug(self, slug, signals):
        signal = self._get_one_signal(signals, slug)
        self.assertEqual(slug, signal.slug)

    def _assert_has_tags(self, tags, signals):
        signal = self._get_one_signal(signals, tags=tags)
        self.assertEqual(len(tags), len(signal.tags))
        list(map(lambda t: self.assertIn(t, signal.tags), tags))


class HTTPFailureUnittest(HTTPCheckUnittest):

    timeout_tags = [
        "EXCEPTION_RAISED", "CONNECTION_TIMEOUT", "SERVER_FAIL"
    ]
    bad_request_tags = [
        "EXCEPTION_RAISED", "INVALID_REQUEST", "CLIENT_FAIL"
    ]
    conn_fail_tags = ["EXCEPTION_RAISED", "CONNECTION_FAIL"]

    def test_read_timeout(self):
        signal = http_checks.check_fail(rex.ReadTimeout())
        self._assert_has_tags(self.timeout_tags, signal)
        self._assert_has_slug("HTTP_FAIL_READ_TIMEOUT", signal)

    def test_connect_timeout(self):
        signal = http_checks.check_fail(rex.ConnectTimeout())
        self._assert_has_tags(self.timeout_tags, signal)
        self._assert_has_slug("HTTP_FAIL_CONNECT_TIMEOUT", signal)

    def test_invalid_url(self):
        signal = http_checks.check_fail(rex.InvalidURL())
        self._assert_has_tags(self.bad_request_tags, signal)
        self._assert_has_slug("HTTP_FAIL_INVALID_URL", signal)

    def test_missing_schema(self):
        signal = http_checks.check_fail(rex.MissingSchema())
        self._assert_has_tags(self.bad_request_tags, signal)
        self._assert_has_slug("HTTP_FAIL_MISSING_SCHEMA", signal)

    def test_invalid_schema(self):
        signal = http_checks.check_fail(rex.InvalidSchema())
        self._assert_has_tags(self.bad_request_tags, signal)
        self._assert_has_slug("HTTP_FAIL_INVALID_SCHEMA", signal)

    def test_url_required(self):
        signal = http_checks.check_fail(rex.URLRequired())
        self._assert_has_tags(self.bad_request_tags, signal)
        self._assert_has_slug("HTTP_FAIL_URL_REQUIRED", signal)

    def test_proxy_error(self):
        signal = http_checks.check_fail(rex.ProxyError())
        self._assert_has_tags(self.conn_fail_tags, signal)
        self._assert_has_slug("HTTP_FAIL_PROXY_ERROR", signal)

    def test_SSL_error(self):
        signal = http_checks.check_fail(rex.SSLError())
        self._assert_has_tags(self.conn_fail_tags, signal)
        self._assert_has_slug("HTTP_FAIL_SSL_ERROR", signal)


@requests_mock.Mocker()
class HTTPStatusCodeUnittest(HTTPCheckUnittest):

    def _mock_status_code(self, m, code):
        """Convenience method for mocking a status code."""
        m.register_uri("GET", "http://test.com", text="Ok", status_code=code)
        return client.request("GET", "http://test.com")

    def test_200(self, m):
        """Test a 200 status code."""
        resp, signals = self._mock_status_code(m, 200)
        self._assert_has_slug("HTTP_STATUS_CODE_2XX_200", signals)

    def test_302(self, m):
        """Test a 302 status code."""
        resp, signals = self._mock_status_code(m, 302)
        self._assert_has_slug("HTTP_STATUS_CODE_3XX_302", signals)
        self._assert_has_tags(["SERVER_REDIRECT"], signals)

    def test_401(self, m):
        """Test a 401 status code."""
        resp, signals = self._mock_status_code(m, 401)
        self._assert_has_slug("HTTP_STATUS_CODE_4XX_401", signals)
        self._assert_has_tags(["CLIENT_FAIL"], signals)

    def test_501(self, m):
        """Test a 501 status code."""
        resp, signals = self._mock_status_code(m, 501)
        self._assert_has_slug("HTTP_STATUS_CODE_5XX_501", signals)
        self._assert_has_tags(["SERVER_FAIL"], signals)


@requests_mock.Mocker()
class HTTPContentTypeUnittest(HTTPCheckUnittest):

    def _mock_content_type(self, m, content_type):
        """Convenience method for mocking a content type."""
        m.register_uri("GET", "http://test.com", text="Ok",
                       headers={"Content-Type": content_type})
        return client.request("GET", "http://test.com")

    # XML

    def test_real_xml(self, m):
        """Test a real XML content type."""
        resp, signals = self._mock_content_type(m, "application/xml")
        self._assert_has_slug("HTTP_CONTENT_TYPE_XML", signals)

    def test_real_xml_suffix(self, m):
        """Test a real XML content type w/ "xml" suffix."""
        resp, signals = self._mock_content_type(m, "application/atom+xml")
        self._assert_has_slug("HTTP_CONTENT_TYPE_XML", signals)

    def test_garbage_xml_suffix(self, m):
        """Test a garbage XML content type w/ "xml" suffix."""
        resp, signals = self._mock_content_type(m, "garbage/garbage+xml")
        self._assert_has_slug("HTTP_CONTENT_TYPE_XML", signals)

    def test_vague_xml(self, m):
        resp, signals = self._mock_content_type(m, "application/xml-dtd")
        self._assert_has_slug("HTTP_CONTENT_TYPE_XML", signals)

    def test_vague_xml_with_charset(self, m):
        resp, signals = self._mock_content_type(
            m, "application/xml-dtd; charset=utf-8")
        self._assert_has_slug("HTTP_CONTENT_TYPE_XML", signals)

    # JSON

    def test_real_json(self, m):
        """Test a real JSON content type"json" suffix."""
        resp, signals = self._mock_content_type(m, "application/json")
        self._assert_has_slug("HTTP_CONTENT_TYPE_JSON", signals)

    def test_real_json_suffix(self, m):
        """Test a real JSON content type w/ "json" suffix."""
        resp, signals = self._mock_content_type(
            m, "application/json-patch+json")
        self._assert_has_slug("HTTP_CONTENT_TYPE_JSON", signals)

    def test_garbage_json_suffix(self, m):
        """Test a garbage JSON content type w/ "json" suffix."""
        resp, signals = self._mock_content_type(m, "garbage/garbage+json")
        self._assert_has_slug("HTTP_CONTENT_TYPE_JSON", signals)

    def test_json_type_with_charset(self, m):
        """Test a real JSON content type w/ "charset" appended."""
        resp, signals = self._mock_content_type(
            m, "application/json; charset=utf-8")
        self._assert_has_slug("HTTP_CONTENT_TYPE_JSON", signals)

    # HTML

    def test_html(self, m):
        """Test a real HTML content type w/ "charset" appended."""
        resp, signals = self._mock_content_type(m, "text/html")
        self._assert_has_slug("HTTP_CONTENT_TYPE_HTML", signals)

    # TEXT

    def test_plain(self, m):
        """Test a real HTML content type w/ "charset" appended."""
        resp, signals = self._mock_content_type(m, "text/plain")
        self._assert_has_slug("HTTP_CONTENT_TYPE_PLAIN", signals)
