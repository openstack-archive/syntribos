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
import time
import unittest

from oslo_config import cfg

import syntribos
from syntribos.formatters.json_formatter import JSONFormatter
from syntribos.runner import Runner

CONF = cfg.CONF


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

    def addError(self, test, err):
        """Duplicates parent class addError functionality.

        :param test: The test that encountered an error
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        :param err:
        :type tuple: Tuple of format ``(type, value, traceback)``
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self.stats["errors"] += 1

    def addSuccess(self, test):
        """Duplicates parent class addSuccess functionality.

        :param test: The test that was run
        :type test: :class:`syntribos.tests.base.BaseTestCase`
        """
        self.stats["successes"] += 1

    def printErrors(self, output_format, min_severity, min_confidence):
        """Print out each :class:`syntribos.issue.Issue` that was encountered

        :param str output_format: Either "json" or "xml"
        """
        formatter_types = {
            "json": JSONFormatter(self)
        }
        formatter = formatter_types[output_format]
        formatter.report(min_severity, min_confidence)

    def stopTestRun(self):
        """Print errors when the test run is complete."""
        super(IssueTestResult, self).stopTestRun()
        self.printErrors()


def print_log_file_path():
    """Print the path to the log folder for this run."""
    test_log = Runner.get_log_file_name()
    if test_log:
        print(syntribos.SEP)
        print("LOG PATH...: {path}".format(path=test_log))
        print(syntribos.SEP)


def print_result(result, start_time):
    """Prints test summary/stats (e.g. # failures) to stdout

    :param result: Global result object with all issues/etc.
    :type result: :class:`syntribos.result.IssueTestResult`
    :param float start_time: Time this run started
    """
    result.printErrors(
        CONF.output_format, CONF.min_severity, CONF.min_confidence)
    run_time = time.time() - start_time
    tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)

    print("\n{sep}\nRan {num} test{suff} in {time:.3f}s".format(
        sep=syntribos.SEP, num=tests, suff="s" * bool(tests - 1),
        time=run_time))
    if failures or errors:
        print("\nFAILED ({0}{1}{2})".format(
            "failures={0}".format(failures) if failures else "",
            ", " if failures and errors else "",
            "errors={0}".format(errors) if errors else ""))
    print_log_file_path()
    return tests, errors, failures
