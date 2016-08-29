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
import syntribos.result
import syntribos.tests as tests
import syntribos.tests.base
from syntribos.utils import cli as cli

result = None
CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class Runner(object):

    log_file = ""
    current_test_id = 1000

    @classmethod
    def list_tests(cls):
        """Print out the list of available tests types that can be run."""
        print("List of available tests...:\n")
        print("{:<50}{}\n".format("[Test Name]", "[Description]"))
        testdict = {name: clss.__doc__ for name, clss in cls.get_tests()}
        for test in sorted(testdict):
            if testdict[test] is None:
                raise Exception(("No test description provided"
                                 " as doc string for the test: {0}".format(
                                     test)))
            else:
                test_description = testdict[test].split(".")[0]
            print("{test:<50}{desc}\r".format(
                test=test, desc=test_description))
        print("\n")
        exit(0)

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
        """Yields relevant tests based on test type

        :param list test_types: Test types to be run

        :rtype: tuple
        :returns: (test type (str), ```syntribos.tests.base.TestType```)
        """
        cls.load_modules(tests)
        test_types = test_types or [""]
        excluded_types = excluded_types or [""]
        items = sorted(syntribos.tests.base.test_table.iteritems())
        included = []
        # Only include tests allowed by value in -t params
        for t in test_types:
            included += [x for x in items if t in x[0]]
        # Exclude any tests that meet the above but are excluded by -e params
        for e in excluded_types:
            if e:
                included = [x for x in included if e not in x[0]]
        return (i for i in included)

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
        """Method sets up logger and decides on Syntribos control flow

        This is the method where control flow of Syntribos is decided
        based on the commands entered. Depending upon commands such
        as ```list_tests``` or ```run``` the respective method is called.
        """
        global result
        try:
            syntribos.config.register_opts()
            CONF(sys.argv[1:],
                 default_config_files=cls.get_default_conf_files())
            logging.basicConfig(filename=cls.get_log_file_name(),
                                level=logging.DEBUG)
            CONF.log_opt_values(LOG, logging.DEBUG)
        except Exception as exc:
            syntribos.config.handle_config_exception(exc)

        cli.print_symbol()
        if not CONF.outfile:
            decorator = unittest.runner._WritelnDecorator(sys.stdout)
        else:
            decorator = unittest.runner._WritelnDecorator(
                open(CONF.outfile, 'w'))
        result = syntribos.result.IssueTestResult(decorator, True, verbosity=1)
        if CONF.sub_command.name == "list_tests":
            cls.list_tests()
        else:
            cls.start_time = time.time()
            list_of_tests = list(cls.get_tests(CONF.test_types,
                                               CONF.excluded_types))
            print("\nRunning Tests...:")
            for file_path, req_str in CONF.syntribos.templates:
                if not file_path.endswith(".template"):
                    LOG.debug('file.......: {0} (SKIPPED)'.format(file_path))
                    continue

                test_names = [t for (t, _) in list_of_tests]
                log_string = ''.join([
                    '\n{0}\nTEMPLATE FILE\n{0}\n'.format('-' * 12),
                    'file.......: {0}\n'.format(file_path),
                    'tests......: {0}\n'.format(test_names)])
                LOG.debug(log_string)

                print(syntribos.SEP)
                print("Template File...: {}".format(file_path))
                print(syntribos.SEP)

                if CONF.sub_command.name == "run":
                    cls.run_all_tests(list_of_tests, file_path, req_str)
                elif CONF.sub_command.name == "dry_run":
                    cls.dry_run(list_of_tests, file_path, req_str)
            result.print_result(cls.start_time)

    @classmethod
    def dry_run(cls, list_of_tests, file_path, req_str):
        """Loads all the template and data files and prints out the tests

        This method  does not run any tests, but loads all the templates
        and payload data files and prints all the loaded tests.

        :param list list_of_tests: A list of all the tests loaded
        :param str file_path: Path of the  payload file
        :param str req_str: Request string of each template

        :return: None
        """
        for test_name, test_class in list_of_tests:
            log_string = "Dry ran  :  {name}".format(name=test_name)
            LOG.debug(log_string)
            test_class.send_init_request(file_path, req_str)
            test_cases = list(
                test_class.get_test_cases(file_path, req_str))
            if len(test_cases) > 0:
                for test in test_cases:
                    if test:
                        cls.run_test(test, result, dry_run=True)

    @classmethod
    def run_all_tests(cls, list_of_tests, file_path, req_str):
        """Loads all the payload data and templates runs all the tests

        This method call run_test method to run each of the tests one
        by one.

        :param list list_of_tests: A list of all the tests loaded
        :param str file_path: Path of the  payload file
        :param str req_str: Request string of each template

        :return: None
        """
        try:
            template_start_time = time.time()
            failures = 0
            errors = 0
            print("\n  ID \t\tTest Name      \t\t\t\t\t\tProgress")
            for test_name, test_class in list_of_tests:
                test_class.test_id = cls.current_test_id
                cls.current_test_id += 5
                log_string = "[{test_id}]  :  {name}".format(
                    test_id=test_class.test_id, name=test_name)
                result_string = "[{test_id}]  :  {name}".format(
                    test_id=cli.colorize(test_class.test_id, color="green"),
                    name=test_name.replace("_", " ").capitalize())
                if not CONF.colorize:
                    result_string = result_string.ljust(55)
                else:
                    result_string = result_string.ljust(60)
                LOG.debug(log_string)
                test_class.send_init_request(file_path, req_str)
                test_cases = list(
                    test_class.get_test_cases(file_path, req_str))
                if len(test_cases) > 0:
                    bar = cli.ProgressBar(message=result_string,
                                          max=len(test_cases))
                    last_errors = len(result.errors)
                    last_failures = len(result.failures)
                    for test in test_cases:
                        if test:
                            cls.run_test(test, result)
                            bar.increment(1)
                        bar.print_bar()
                        failures = result.stats["failures"] - last_failures
                        errors = result.stats["errors"] - last_errors
                        total_tests = len(test_cases)
                        if failures > total_tests * 0.90:
                            # More than 90 percent failure
                            failures = cli.colorize(failures, "red")
                        elif failures > total_tests * 0.45:
                            # More than 45 percent failure
                            failures = cli.colorize(failures, "yellow")
                        elif failures > total_tests * 0.15:
                            # More than 15 percent failure
                            failures = cli.colorize(failures, "blue")
                    if errors:
                        last_failures = result.stats["failures"]
                        last_errors = result.stats["errors"]
                        errors = cli.colorize(errors, "red")
                        print ("  :  {0} Failure(s), {1} Error(s)\r".format(
                            failures, errors))
                    else:
                        last_failures = len(result.failures)
                        print("  :  {} Failure(s)\r".format(failures))

            run_time = time.time() - template_start_time
            LOG.debug("Run time: {} sec.".format(run_time))
            num_tests = result.testsRun - result.testsRunSinceLastPrint
            print("\nRan {num} test(s) in {time:.3f}s\n".format(
                  num=num_tests, time=run_time))
            result.testsRunSinceLastPrint = result.testsRun

        except KeyboardInterrupt:
            result.print_result(cls.start_time)
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
        suite.addTest(test("run_test_case"))
        if dry_run:
            for test in suite:
                print(test)
        else:
            suite.run(result)


def entry_point():
    """Start runner. Need this so we can point to it in ``setup.cfg``."""
    Runner.run()
    return 0

if __name__ == '__main__':
    entry_point()
