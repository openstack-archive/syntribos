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
import datetime
import logging
import os
import pkgutil
import sys
import time
import unittest

from oslo_config import cfg

import syntribos.config
from syntribos.result import IssueTestResult
import syntribos.tests as tests
import syntribos.tests.base

result = None
CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class Runner(object):

    log_file = ""

    @classmethod
    def print_tests(cls, list_tests=False):
        """Print out the list of available tests types that can be run."""
        if list_tests:
            testlist = []
            print("Test types...:")
            testlist = [name for name, _ in cls.get_tests()]
            print(testlist)

    @classmethod
    def load_modules(cls, package):
        """Imports all tests (:mod:`syntribos.tests`)

        :param package: a package of tests for pkgutil to load
        """
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + '.',
                onerror=lambda x: None):
            __import__(modname, fromlist=[])

    @classmethod
    def get_tests(cls, test_types=None, excluded_types=None):
        """Yields relevant tests based on test type (from ```syntribos.arguments```)

        :param list test_types: Test types to be run

        :rtype: tuple
        :returns: (test type (str), ```syntribos.tests.base.TestType```)
        """
        cls.load_modules(tests)
        test_types = test_types or [""]
        excluded_types = excluded_types or [""]
        for k, v in sorted(syntribos.tests.base.test_table.iteritems()):
            for e in excluded_types:
                if e and e in k:
                    break
                else:
                    for t in test_types:
                        if t in k:
                            yield k, v

    @staticmethod
    def print_symbol():
        """Syntribos radiation symbol."""
        symbol = """               Syntribos
                xxxxxxx
           x xxxxxxxxxxxxx x
        x     xxxxxxxxxxx     x
               xxxxxxxxx
     x          xxxxxxx          x
                 xxxxx
    x             xxx             x
                   x
   xxxxxxxxxxxxxxx   xxxxxxxxxxxxxxx
    xxxxxxxxxxxxx     xxxxxxxxxxxxx
     xxxxxxxxxxx       xxxxxxxxxxx
      xxxxxxxxx         xxxxxxxxx
        xxxxxx           xxxxxx
          xxx             xxx
              x         x
                   x
      === Automated API Scanning  ==="""

        print(syntribos.SEP)
        print(symbol)
        print(syntribos.SEP)

    @classmethod
    def print_log(cls):
        """Print the path to the log folder for this run."""
        test_log = cls.get_log_file_name()
        if test_log:
            print(syntribos.SEP)
            print("LOG PATH..........: {path}".format(path=test_log))
            print(syntribos.SEP)

    @classmethod
    def get_default_conf_files(cls):
        return ["~/.syntribos/syntribos.conf"]

    @classmethod
    def get_log_file_name(cls):
        if not cls.log_file:
            log_dir = CONF.logging.log_dir
            time_str = datetime.datetime.now().strftime("%Y-%m-%d_%X.%f")
            file_name = "{time}.log".format(time=time_str)
            cls.log_file = os.path.join(log_dir, file_name)
        return cls.log_file

    @classmethod
    def run(cls):
        global result
        try:
            try:
                syntribos.config.register_opts()
                CONF(sys.argv[1:],
                     default_config_files=cls.get_default_conf_files())
                logging.basicConfig(filename=cls.get_log_file_name(),
                                    level=logging.DEBUG)
            except Exception as exc:
                syntribos.config.handle_config_exception(exc)

            cls.print_symbol()

            # 2 == higher verbosity, 1 == normal
            verbosity = 1
            if not CONF.outfile:
                decorator = unittest.runner._WritelnDecorator(sys.stdout)
            else:
                decorator = unittest.runner._WritelnDecorator(
                    open(CONF.outfile, 'w'))
            result = IssueTestResult(decorator, True, verbosity)

            start_time = time.time()

            if not CONF.list_tests:
                for file_path, req_str in CONF.syntribos.templates:
                    for test_name, test_class in cls.get_tests(
                            CONF.test_types, CONF.excluded_types):
                        test_class.send_init_request(file_path, req_str)
                        for test in test_class.get_test_cases(file_path,
                                                              req_str):
                            if test:
                                test_time = cls.run_test(test, result,
                                                         CONF.dry_run)
                                test_time = "Test run time: {} sec.".format(
                                    test_time)
                                LOG.debug(test_time)
                cls.print_result(result, start_time)
            else:
                cls.print_tests(CONF.list_tests)
        except KeyboardInterrupt:
            cls.print_result(result, start_time)
            print("Keyboard interrupt, exiting...")
            exit(0)

    @classmethod
    def run_test(cls, test, result, dry_run=False):
        """Create a new test suite, add a test, and run it

        :param test: The test to add to the suite
        :param result: The result object to append to
        :type result: :class:`syntribos.result.IssueTestResult`
        :param bool dry_run: (OPTIONAL) Only print out test names
        """
        suite = unittest.TestSuite()
        test_start_time = time.time()

        suite.addTest(test("run_test_case"))
        if dry_run:
            for test in suite:
                print(test)
        else:
            suite.run(result)
        test_end_time = time.time() - test_start_time
        test_end_time = '%.5f' % test_end_time
        return test_end_time

    @classmethod
    def print_result(cls, result, start_time):
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
        cls.print_log()
        return tests, errors, failures


def entry_point():
    """Start runner. Need this so we can point to it in ``setup.cfg``."""
    Runner.run()
    return 0

if __name__ == '__main__':
    entry_point()
