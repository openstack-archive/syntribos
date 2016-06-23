# Copyright 2015 Rackspace
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
import syntribos
from syntribos.checks import time_diff as time_diff
from syntribos.tests.fuzz import base_fuzz


class SQLInjectionBody(base_fuzz.BaseFuzzTestCase):
    test_name = "SQL_INJECTION_BODY"
    test_type = "data"
    data_key = "sql-injection.txt"
    failure_keys = [
        "SQL syntax",
        "mysql",
        "MySqlException (0x",
        "valid MySQL result",
        "check the manual that corresponds to your MySQL server version",
        "MySqlClient.",
        "com.mysql.jdbc.exceptions",
        "SQLite/JDBCDriver",
        "SQLite.Exception",
        "System.Data.SQLite.SQLiteException",
        "sqlite_.",
        "SQLite3::",
        "[SQLITE_ERROR]",
        "Unknown column",
        "where clause",
        "SqlServer",
        "syntax error"
    ]

    def test_case(self):
        self.test_default_issues()
        failed_strings = self.data_driven_failure_cases()
        if failed_strings:
            self.register_issue(
                defect_type="sql_strings",
                severity=syntribos.MEDIUM,
                confidence=syntribos.LOW,
                description=("The string(s): \'{0}\', known to be commonly "
                             "returned after a successful SQL injection attack"
                             ", have been found in the response. This could "
                             "indicate a vulnerability to SQL injection "
                             "attacks."
                             ).format(failed_strings))

        self.diff_signals.register(time_diff(self.init_resp, self.test_resp))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="sql_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.MEDIUM,
                description=("A response to one of our payload requests has "
                             "taken too long compared to the baseline "
                             "request. This could indicate a vulnerability "
                             "to time-based SQL injection attacks"))


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
