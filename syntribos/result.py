"""
Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

import sys
import unittest

from syntribos.formatters.json_formatter import JSONFormatter


class IssueTestResult(unittest.TextTestResult):

    """Custom unnittest results holder class

    This class aggregates :class:`syntribos.issue.Issue` objects from all the
    tests as they run
    """
    stats = {"errors": 0, "failures": 0, "successes": 0}

    def addFailure(self, test, err):
        """Adds issues to data structures

        Appends issues to the result's list of failures, as well as
        to a dict of {url: {method: {test_name: issue}}} structure.

        :param test: The test that has failed
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        :param tuple err: Tuple of format ``(type, value, traceback)``
        """
        self.failures.append((test, test.failures))
        self.stats["failures"] += len(test.failures)
        if self.showAll:
            sys.stdout.write("FAIL\n")
        elif self.dots:
            sys.stdout.write('F')
            sys.stdout.flush()

    def addError(self, test, err):
        """Duplicates parent class addError functionality.

        :param test: The test that encountered an error
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        :param err:
        :type tuple: Tuple of format ``(type, value, traceback)``
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self.stats["errors"] += 1
        if self.showAll:
            sys.stdout.write("ERROR\n")
        elif self.dots:
            sys.stdout.write('E')
            sys.stdout.flush()

    def addSuccess(self, test):
        """Duplicates parent class addSuccess functionality.

        :param test: The test that was run
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        """
        self.stats["successes"] += 1
        if self.showAll:
            sys.stdout.write("ok\n")
        elif self.dots:
            sys.stdout.write('.')
            sys.stdout.flush()

    def printErrors(self, output_format):
        """Print out each :class:`syntribos.issue.Issue` that was encountered

        :param str output_format: Either "json" or "xml"
        """
        formatter_types = {
            "json": JSONFormatter(self)
        }
        formatter = formatter_types[output_format]
        if self.dots or self.showAll:
            self.stream.writeln()
        formatter.report()

    def stopTestRun(self):
        """Print errors when the test run is complete."""
        super(IssueTestResult, self).stopTestRun()
        self.printErrors()
