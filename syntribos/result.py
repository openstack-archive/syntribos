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

import unittest

from syntribos.formatters.json_formatter import JSONFormatter


class IssueTestResult(unittest.TextTestResult):
    """Custom unnittest results holder class

    A test result class that can return issues raised by tests
    to the Syntribos runner
    """

    def addFailure(self, test, err):
        self.failures.append((test, test.failures))
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

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
        formatter.report()

    def stopTestRun(self):
        super(IssueTestResult, self).stopTestRun()
        self.printErrors()
