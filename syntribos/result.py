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
    aggregated_failures = {}
    pruned_failures = []

    def addFailure(self, test, err):
        """Adds issues to data structures

        Appends issues to the result's list of failures, as well as
        to a dict of {url: {method: {test_name: issue}}} structure.

        :param test: The test that has failed
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        :param tuple err: Tuple of format ``(type, value, traceback)``
        """
        self.failures.append((test, test.failures))
        for issue in test.failures:
            url = issue.request.url
            method = issue.request.method
            if url in self.aggregated_failures:
                if method in self.aggregated_failures[url]:
                    if issue.test in self.aggregated_failures[url][method]:
                        (self.aggregated_failures[url]
                         [method][issue.test].append(issue))
                    else:
                        self.aggregated_failures[url][method][issue.test] = []
                        self.pruned_failures.append((test, [issue.as_dict()]))
                else:
                    self.aggregated_failures[url][method] = {}
            else:
                self.aggregated_failures[url] = {}
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
        super(IssueTestResult, self).addError(test, err)

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
        self.failures = self.pruned_failures
        formatter.report()

    def stopTestRun(self):
        """Print errors when the test run is complete."""
        super(IssueTestResult, self).stopTestRun()
        self.printErrors()
