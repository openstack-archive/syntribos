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
import json
import logging
import os
import pkgutil
import sys
import time
import traceback
import unittest

from oslo_config import cfg
from six.moves import input

import syntribos.config
from syntribos.formatters.json_formatter import JSONFormatter
from syntribos._i18n import _, _LW, _LE   # noqa
import syntribos.result
import syntribos.tests as tests
import syntribos.tests.base
from syntribos.utils import cleanup
from syntribos.utils import cli as cli
from syntribos.utils import env as ENV
from syntribos.utils.file_utils import ContentType
from syntribos.utils import remotes

result = None
user_base_dir = None
CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class Runner(object):
    """The core engine of syntribos.

    This class is composed of a set of static methods that forms the core of
    syntribos. These include methods to list tests, run, to load test modules,
    to dry run etc.
    """

    log_path = ""
    current_test_id = 1000

    @classmethod
    def list_tests(cls):
        """Print out the list of available tests types that can be run."""
        print(_("List of available tests...:\n"))
        print("{:<50}{}\n".format(_("[Test Name]"),
                                  _("[Description]")))
        testdict = {name: clss.__doc__ for name, clss in cls.get_tests()}
        for test in sorted(testdict):
            if testdict[test] is None:
                raise Exception(
                    _("No test description provided"
                      " as doc string for the test: %s") % test)
            else:
                test_description = testdict[test].split(".")[0]
            print("{test:<50}{desc}\r".format(
                test=test, desc=test_description))
        print("\n")

    @classmethod
    def load_modules(cls, package):
        """Imports all tests (:mod:`syntribos.tests`)

        :param package: a package of tests for pkgutil to load
        """
        for i, modname, k in pkgutil.walk_packages(
                path=package.__path__,
                prefix=package.__name__ + '.',
                onerror=lambda x: None):
            __import__(modname, fromlist=[])

    @classmethod
    def get_tests(cls, test_types=None, excluded_types=None, dry_run=False):
        """Yields relevant tests based on test type

        :param list test_types: Test types to be run

        :rtype: tuple
        :returns: (test type (str), ```syntribos.tests.base.TestType```)
        """

        cls.load_modules(tests)
        test_types = test_types or [""]
        excluded_types = excluded_types or [""]
        items = sorted((syntribos.tests.base.test_table).items())
        # If it's a dry run, only return the debug test
        if dry_run:
            return (x for x in items if "DEBUG" in x[0])
        # Otherwise, don't run the debug test at all
        else:
            excluded_types.append("DEBUG")
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
    def get_logger(cls, template_name):
        """Updates the logger handler for LOG."""
        template_name = template_name.replace(os.path.sep, "::")
        template_name = template_name.replace(".", "_")
        log_file = "{0}.log".format(template_name)
        if not cls.log_path:
            cls.log_path = ENV.get_log_dir_name()
        log_file = os.path.join(cls.log_path, log_file)
        log_handle = logging.FileHandler(log_file, 'w')
        LOG = logging.getLogger()
        LOG.handlers = [log_handle]
        LOG.setLevel(logging.DEBUG)
        return LOG

    @classmethod
    def setup_config(cls, use_file=False, argv=None):
        """Register CLI options & parse config file."""
        if argv is None:
            argv = sys.argv[1:]
        try:
            syntribos.config.register_opts()
            if use_file:
                CONF(argv, default_config_files=[ENV.get_default_conf_file()])
            else:
                CONF(argv, default_config_files=[])
        except Exception as exc:
            syntribos.config.handle_config_exception(exc)

    @classmethod
    def setup_runtime_env(cls):
        """Sets up the environment for a current test run.

        This includes registering / parsing config options, creating the
        timestamped log directory and the results log file, if specified
        """
        # Setup logging
        cls.log_path = ENV.get_log_dir_name()
        if not os.path.isdir(cls.log_path):
            os.makedirs(cls.log_path)

        # Create results file if any, otherwise use sys.stdout
        if CONF.outfile:
            cls.output = open(CONF.outfile, "w")
        else:
            cls.output = sys.stdout

    @classmethod
    def get_meta_vars(cls, file_path):
        """Creates the appropriate meta_var dict for the given file path

        Meta variables are inherited according to directory. This function
        builds a meta variable dict from the top down.

        :param file_path: the path of the current template
        :returns: `dict` of meta variables
        """
        path_segments = [""] + os.path.dirname(file_path).split(os.sep)
        meta_vars = {}
        current_path = ""
        for seg in path_segments:
            current_path = os.path.join(current_path, seg)
            if current_path in cls.meta_dir_dict:
                for k, v in cls.meta_dir_dict[current_path].items():
                    meta_vars[k] = v
        return meta_vars

    @classmethod
    def run(cls):
        """Method sets up logger and decides on Syntribos control flow

        This is the method where control flow of Syntribos is decided
        based on the commands entered. Depending upon commands such
        as ```list_tests``` or ```run``` the respective method is called.
        """
        global result

        cli.print_symbol()

        # If we are initializing, don't look for a default config file
        if "init" in sys.argv:
            cls.setup_config()
        else:
            cls.setup_config(use_file=True)
        try:
            if CONF.sub_command.name == "init":
                ENV.initialize_syntribos_env()
                exit(0)

            elif CONF.sub_command.name == "list_tests":
                cls.list_tests()
                exit(0)

            elif CONF.sub_command.name == "download":
                ENV.download_wrapper()
                exit(0)
        except AttributeError:
            print(
                _(
                    "Not able to run the requested sub command, please check "
                    "the debug logs for more information, exiting..."))
            exit(1)

        if not ENV.is_syntribos_initialized():
            print(_("Syntribos was not initialized. Please run the 'init'"
                    " command or set it up manually. See the README for"
                    " more information about the installation process."))
            exit(1)

        cls.setup_runtime_env()

        decorator = unittest.runner._WritelnDecorator(cls.output)
        result = syntribos.result.IssueTestResult(decorator, True, verbosity=1)

        cls.start_time = time.time()
        if CONF.sub_command.name == "run":
            list_of_tests = list(
                cls.get_tests(CONF.test_types, CONF.excluded_types))
        elif CONF.sub_command.name == "dry_run":
            dry_run_output = {"failures": [], "successes": []}
            list_of_tests = list(cls.get_tests(dry_run=True))

        print(_("\nRunning Tests...:"))
        templates_dir = CONF.syntribos.templates
        if templates_dir is None:
            print(_("Attempting to download templates from {}").format(
                CONF.remote.templates_uri))
            templates_path = remotes.get(CONF.remote.templates_uri)
            try:
                templates_dir = ContentType("r", 0)(templates_path)
            except IOError:
                print(_("Not able to open `%s`; please verify path, "
                        "exiting...") % templates_path)
                exit(1)

        print(_("\nPress Ctrl-C to pause or exit...\n"))
        meta_vars = None
        templates_dir = list(templates_dir)
        cls.meta_dir_dict = {}
        for file_path, file_content in templates_dir:
            if os.path.basename(file_path) == "meta.json":
                meta_path = os.path.dirname(file_path)
                try:
                    cls.meta_dir_dict[meta_path] = json.loads(file_content)
                except Exception:
                    print("Unable to parse %s, skipping..." % file_path)

        for file_path, req_str in templates_dir:
            if "meta.json" in file_path:
                continue
            meta_vars = cls.get_meta_vars(file_path)
            LOG = cls.get_logger(file_path)
            CONF.log_opt_values(LOG, logging.DEBUG)
            if not file_path.endswith(".template"):
                LOG.warning(
                    _LW('file.....:%s (SKIPPED - not a .template file)'),
                    file_path)
                continue

            test_names = [t for (t, i) in list_of_tests]  # noqa
            log_string = ''.join([
                '\n{0}\nTEMPLATE FILE\n{0}\n'.format('-' * 12),
                'file.......: {0}\n'.format(file_path),
                'tests......: {0}\n'.format(test_names)
            ])
            LOG.debug(log_string)
            print(syntribos.SEP)
            print("Template File...: {}".format(file_path))
            print(syntribos.SEP)

            if CONF.sub_command.name == "run":
                cls.run_given_tests(list_of_tests, file_path,
                                    req_str, meta_vars)
            elif CONF.sub_command.name == "dry_run":
                cls.dry_run(list_of_tests, file_path,
                            req_str, dry_run_output, meta_vars)

        if CONF.sub_command.name == "run":
            result.print_result(cls.start_time)
            cleanup.delete_temps()
        elif CONF.sub_command.name == "dry_run":
            cls.dry_run_report(dry_run_output)

    @classmethod
    def dry_run(cls, list_of_tests, file_path, req_str, output,
                meta_vars=None):
        """Runs debug test to check all steps leading up to executing a test

        This method does not run any checks, but does parse the template files
        and config options. It then runs a debug test which sends no requests
        of its own.

        Note: if any external calls referenced inside the template file do make
        requests, the parser will still make those requests even for a dry run

        :param str file_path: Path of the template file
        :param str req_str: Request string of each template

        :return: None
        """
        for k, test_class in list_of_tests:  # noqa
            try:
                print("\nParsing template file...\n")
                test_class.create_init_request(file_path, req_str, meta_vars)
            except Exception as e:
                print("\nError in parsing template:\n \t{0}\n".format(
                    traceback.format_exc()))
                LOG.error(_LE("Error in parsing template:"))
                output["failures"].append({
                    "file": file_path,
                    "error": e.__str__()
                })
            else:
                print(_("\nRequest sucessfully generated!\n"))
                output["successes"].append(file_path)

            test_cases = list(test_class.get_test_cases(file_path, req_str))
            if len(test_cases) > 0:
                for test in test_cases:
                    if test:
                        cls.run_test(test, result)

    @classmethod
    def dry_run_report(cls, output):
        """Reports the dry run through a formatter."""
        formatter_types = {"json": JSONFormatter(result)}
        formatter = formatter_types[CONF.output_format]
        formatter.report(output)

        test_log = cls.log_path
        print(syntribos.SEP)
        print(_("LOG PATH...: {path}").format(path=test_log))
        print(syntribos.SEP)

    @classmethod
    def run_given_tests(cls, list_of_tests, file_path, req_str,
                        meta_vars=None):
        """Loads all the templates and runs all the given tests

        This method calls run_test method to run each of the tests one
        by one.

        :param list list_of_tests: A list of all the loaded tests
        :param str file_path: Path of the template file
        :param str req_str: Request string of each template

        :return: None
        """
        try:
            template_start_time = time.time()
            failures = 0
            errors = 0
            print("\n  ID \t\tTest Name      \t\t\t\t\t\t    Progress")
            for test_name, test_class in list_of_tests:
                test_class.test_id = cls.current_test_id
                cls.current_test_id += 5
                log_string = "[{test_id}]  :  {name}".format(
                    test_id=test_class.test_id, name=test_name)
                result_string = "[{test_id}]  :  {name}".format(
                    test_id=cli.colorize(
                        test_class.test_id, color="green"),
                    name=test_name.replace("_", " ").capitalize())
                if not CONF.colorize:
                    result_string = result_string.ljust(55)
                else:
                    result_string = result_string.ljust(60)
                LOG.debug(log_string)
                try:
                    test_class.send_init_request(file_path, req_str, meta_vars)
                except Exception:
                    print(_(
                        "Error in parsing template:\n %s\n"
                    ) % traceback.format_exc())
                    LOG.error(_LE("Error in parsing template:"))
                    break
                test_cases = list(
                    test_class.get_test_cases(file_path, req_str))
                if len(test_cases) > 0:
                    p_bar = cli.ProgressBar(
                        message=result_string, total_len=len(test_cases))
                    last_failures = result.stats["failures"]
                    last_errors = result.stats["errors"]
                    for test in test_cases:
                        if test:
                            cls.run_test(test, result)
                            p_bar.increment(1)
                        p_bar.print_bar()
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
                        print(_(
                            "  :  %(fail)s Failure(s), %(err)s Error(s)\r") % {
                                "fail": failures, "err": errors})
                    else:
                        last_failures = result.stats["failures"]
                        print(
                            _(
                                "  : %s Failure(s), 0 Error(s)\r") % failures)

            run_time = time.time() - template_start_time
            LOG.info(_("Run time: %s sec."), run_time)
            if hasattr(result, "testsRun"):
                num_tests = result.testsRun - result.testsRunSinceLastPrint
                print(_("\nRan %(num)s test(s) in %(time).3f s\n") %
                      {"num": num_tests, "time": run_time})
                result.testsRunSinceLastPrint = result.testsRun

        except KeyboardInterrupt:
            print(_(
                '\n\nPausing...Hit ENTER to continue, type quit to exit.'))
            try:
                response = input()
                if response.lower() == "quit":
                    result.print_result(cls.start_time)
                    cleanup.delete_temps()
                    print(_("Exiting..."))
                    exit(0)
                print(_('Resuming...'))
            except KeyboardInterrupt:
                result.print_result(cls.start_time)
                cleanup.delete_temps()
                print(_("Exiting..."))
                exit(0)

    @classmethod
    def run_test(cls, test, result):
        """Create a new test suite, add a test, and run it

        :param test: The test to add to the suite
        :param result: The result object to append to
        :type result: :class:`syntribos.result.IssueTestResult`
        :param bool dry_run: (OPTIONAL) Only print out test names
        """
        suite = unittest.TestSuite()
        suite.addTest(test("run_test_case"))
        suite.run(result)


def entry_point():
    """Start runner. Need this so we can point to it in ``setup.cfg``."""
    Runner.run()
    return 0


if __name__ == '__main__':
    entry_point()
