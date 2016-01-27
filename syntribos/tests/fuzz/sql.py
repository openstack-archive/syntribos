"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from syntribos.issue import Issue
from syntribos.tests.fuzz import base_fuzz


class SQLInjectionBody(base_fuzz.BaseFuzzTestCase):
    test_name = "SQL_INJECTION_BODY"
    test_type = "data"
    data_key = "sql-injection.txt"
    failure_keys = [
        'fatal',
        'warning',
        'error',
        'exception',
        'illegal',
        'invalid',
        'fail',
        'stack',
        'access',
        'directory',
        'file',
        'not found',
        'unknown',
        'uid=',
        'varchar',
        'ODBC',
        'SQL',
        'quotation mark',
        'syntax',
        'ORA-',
        '111111']

    def data_driven_failure_cases(self):
        failure_assertions = []
        if self.failure_keys is None:
            return []
        for line in self.failure_keys:
            failure_assertions.append((self.assertNotIn,
                                      line, self.resp.content))
        return failure_assertions

    def test_case(self):
        self.register_issue(
            Issue(test="injection_strings",
                  severity="Medium",
                  confidence="Low",
                  text=("A string known to be commonly returned after a "
                        "successful SQL injection attack was included in the "
                        "response. This could indicate a vulnerability to "
                        "SQL injection attacks."),
                  assertions=self.data_driven_failure_cases()))
        self.test_issues()


class SQLInjectionParams(SQLInjectionBody):
    test_name = "SQL_INJECTION_PARAMS"
    test_type = "params"


class SQLInjectionHeaders(SQLInjectionBody):
    test_name = "SQL_INJECTION_HEADERS"
    test_type = "headers"


class SQLInjectionURL(SQLInjectionBody):
    test_name = "SQL_INJECTION_URL"
    test_type = "url"
    url_var = "FUZZ"
