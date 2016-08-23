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
    testsRunSinceLastPrint = 0

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

    def print_result(self, start_time):
        """Prints test summary/stats (e.g. # failures) to stdout."""
        self.printErrors(
            CONF.output_format, CONF.min_severity, CONF.min_confidence)
        self.print_log_path_and_stats(start_time)

    def print_log_path_and_stats(self, start_time):
        """Print the path to the log folder for this run."""
        test_log = Runner.get_log_file_name()
        run_time = time.time() - start_time
        print("\n{sep}\nTotal: Ran {num} test{suff} in {time:.3f}s".format(
            sep=syntribos.SEP, num=self.testsRun,
            suff="s" * bool(self.testsRun - 1), time=run_time))
        print("Total: {f} failure{fsuff} and {e} error{esuff}".format(
            f=len(self.failures), e=len(self.errors),
            fsuff="s" * bool(len(self.failures) - 1),
            esuff="s" * bool(len(self.errors) - 1)))
        if test_log:
            print(syntribos.SEP)
            print("LOG PATH...: {path}".format(path=test_log))
            print(syntribos.SEP)
