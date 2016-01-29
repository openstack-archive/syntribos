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

import json
import unittest


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
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavor, errors):
        """Prints test failures and errors

        Right now, just spits out the list of Issues as json in the simplest
        way possible. The idea is to pass this results class into bandit-style
        formatters
        """
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" %
                                (flavor, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            if flavor == "FAIL":
                self.stream.writeln("%s" %
                                    json.dumps(err, sort_keys=True, indent=2))
            else:
                self.stream.writeln("%s" % err)

    def stopTestRun(self):
        super(IssueTestResult, self).stopTestRun()
        self.printErrors()
