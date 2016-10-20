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
import testtools

import syntribos.config
from syntribos.runner import Runner
import syntribos.tests

syntribos.config.register_opts()


class RunnerUnittest(testtools.TestCase):

    r = Runner()
    common_endings = ["BODY", "HEADERS", "PARAMS", "URL"]

    def _compare_tests(self, expected, loaded):
        """Compare list of expected test names with those that were loaded."""
        # loaded_test_names = []
        loaded_test_names = [x[0] for x in loaded]
        self.assertEqual(expected, loaded_test_names)

    def test_get_LDAP_tests(self):
        """Check that we get the proper LDAP tests."""
        expected = ["LDAP_INJECTION_" + x for x in self.common_endings]
        loaded_tests = self.r.get_tests(["LDAP"])
        self._compare_tests(expected, loaded_tests)

    def test_get_SQL_tests(self):
        """Check that we get the proper SQLi tests."""
        expected = ["SQL_INJECTION_" + x for x in self.common_endings]
        loaded_tests = self.r.get_tests(["SQL"])
        self._compare_tests(expected, loaded_tests)

    def test_get_XXE_tests(self):
        """Check that we get the proper XXE tests."""
        expected = ["XML_EXTERNAL_ENTITY_BODY"]
        loaded_tests = self.r.get_tests(["XML"])
        self._compare_tests(expected, loaded_tests)

    def test_get_int_overflow_tests(self):
        """Check that we get the proper integer overflow tests."""
        expected = ["INTEGER_OVERFLOW_" + x for x in self.common_endings]
        loaded_tests = self.r.get_tests(["INTEGER_OVERFLOW"])
        self._compare_tests(expected, loaded_tests)

    def test_get_buffer_overflow_tests(self):
        """Check that we get the proper buffer overflow tests."""
        expected = ["BUFFER_OVERFLOW_" + x for x in self.common_endings]
        loaded_tests = self.r.get_tests(["BUFFER_OVERFLOW"])
        self._compare_tests(expected, loaded_tests)

    def test_get_command_injection_tests(self):
        """Check that we get the proper command injection tests."""
        expected = ["COMMAND_INJECTION_" + x for x in self.common_endings]
        loaded_tests = self.r.get_tests(["COMMAND_INJECTION"])
        self._compare_tests(expected, loaded_tests)

    def test_get_string_validation_tests(self):
        """Check that we get the proper string validation tests."""
        expected = [
            "STRING_VALIDATION_" + x for x in self.common_endings
        ]
        loaded_tests = self.r.get_tests(["STRING_VALIDATION"])
        self._compare_tests(expected, loaded_tests)

    def test_get_xss_test(self):
        """Check that we get only the XSS_BODY test from get_tests."""
        expected = ["XSS_BODY"]
        loaded_tests = self.r.get_tests(["XSS"])
        self._compare_tests(expected, loaded_tests)

    def test_get_ssl_test(self):
        """Check that we get only the SSL test from get_tests."""
        expected = ["SSL_ENDPOINT_BODY"]
        loaded_tests = self.r.get_tests(["SSL"])
        self._compare_tests(expected, loaded_tests)

    def test_get_cors_test(self):
        """Check that we get only the CORS_HEADER test from get_tests."""
        expected = ["CORS_WILDCARD_HEADERS"]
        loaded_tests = self.r.get_tests(["CORS_WILDCARD_HEADERS"])
        self._compare_tests(expected, loaded_tests)

    def test_get_sql_tests_exclude_header(self):
        """Check that we get the right SQL tests when "HEADER" is excluded."""
        expected = [
            "SQL_INJECTION_BODY", "SQL_INJECTION_PARAMS", "SQL_INJECTION_URL"]
        loaded_tests = self.r.get_tests(["SQL"], ["HEADER"])
        self._compare_tests(expected, loaded_tests)

    def test_get_sql_tests_exclude_header_url(self):
        """Check that we get the right SQL tests, excluding HEADER/URL."""
        expected = [
            "SQL_INJECTION_BODY", "SQL_INJECTION_PARAMS"]
        loaded_tests = self.r.get_tests(["SQL"], ["HEADER", "URL"])
        self._compare_tests(expected, loaded_tests)

    def test_get_sql_tests_exclude_header_url_body(self):
        """Check that we get the right SQL tests, excluding HEADER/URL/BODY."""
        expected = ["SQL_INJECTION_PARAMS"]
        loaded_tests = self.r.get_tests(["SQL"], ["HEADER", "URL", "BODY"])
        self._compare_tests(expected, loaded_tests)

    def test_get_rce_sql_tests_exclude_url_body(self):
        """Check that we get the right SQL tests, excluding HEADER/URL/BODY."""
        expected = [
            "SQL_INJECTION_HEADERS", "SQL_INJECTION_PARAMS",
            "COMMAND_INJECTION_HEADERS", "COMMAND_INJECTION_PARAMS"]
        loaded_tests = self.r.get_tests(["SQL", "COMMAND"], ["URL", "BODY"])
        self._compare_tests(expected, loaded_tests)

    def test_list_tests(self):
        """Check that we can list tests and exit successfully."""
        self.r.list_tests()

    def test_run_empty_tests(self):
        """Call Runner.run_given_tests with an empty list for sanity check."""
        self.r.run_given_tests([], "", "")

    def test_dry_run_empty_tests(self):
        """Call Runner.dry_run with empty list for sanity check."""
        self.r.dry_run([], "", "", {})
