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

    A test result class that can return issues raised by tests
    to the Syntribos runner
    """
    aggregated_failures = {}
    pruned_failures = []

    def addFailure(self, test, err):
        """Adds failed issues to data structures

        Appends failed issues to the result's list of failures, as well as
        to a dict of {url:
                        method:
                            test_name: issue} structure.
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
        """Duplicates parent class addError functionality."""
        super(IssueTestResult, self).addError(test, err)

    def printErrors(self, output_format):
        formatter_types = {
            "json": JSONFormatter(self)
        }
        formatter = formatter_types[output_format]
        if self.dots or self.showAll:
            self.stream.writeln()
        self.failures = self.pruned_failures
        formatter.report()

    def stopTestRun(self):
        super(IssueTestResult, self).stopTestRun()
        self.printErrors()
