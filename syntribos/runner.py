from __future__ import print_function

from unittest.runner import _WritelnDecorator
import os
import pkgutil
import requests
import sys
import time
import unittest

from cafe.common.reporting.cclogging import init_root_log_handler
from cafe.configurator.managers import TestEnvManager
from cafe.drivers.base import print_exception
from cafe.drivers.unittest.suite import OpenCafeUnittestTestSuite as TestSuite

from syntribos import tests
from syntribos.tests.base import test_table
from syntribos.config import MainConfig
from syntribos.arguments import SyntribosCLI


class Runner(object):
    @classmethod
    def load_modules(cls, package):
        if not os.environ.get("CAFE_CONFIG_FILE_PATH"):
            os.environ["CAFE_CONFIG_FILE_PATH"] = "./"
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + '.',
                onerror=lambda x: None):
            __import__(modname, fromlist=[])

    @classmethod
    def get_tests(cls, test_types=None):
        cls.load_modules(tests)
        test_types = test_types or [""]
        for k, v in sorted(test_table.items()):
            if any([True for t in test_types if t in k]):
                yield k, v

    @classmethod
    def print_tests(cls):
        for name, test in cls.get_tests():
            print(name)

    @staticmethod
    def print_symbol():
        """ Syntribos radiation symbol """
        border = '-' * 40
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

        print(border)
        print(symbol)
        print(border)

    @staticmethod
    def print_log():
        test_log = os.environ.get("CAFE_TEST_LOG_PATH")
        if test_log:
            print("=" * 70)
            print("LOG PATH..........: {0}".format(test_log))
            print("=" * 70)

    @classmethod
    def run(cls):
        requests.packages.urllib3.disable_warnings()
        try:
            cls.print_symbol()
            usage = """
                syntribos <config> <input_file> --test-types=TEST_TYPES
                syntribos <config> <input_file> -t TEST_TYPE TEST_TYPE ...
                syntribos <config> <input_file>
                """
            args, unknown = SyntribosCLI(usage=usage).parse_known_args()
            test_env_manager = TestEnvManager(
                "", args.config, test_repo_package_name="os")
            test_env_manager.finalize()
            cls.set_env()
            init_root_log_handler()

            cls.print_log()
            result = unittest.TextTestResult(
                _WritelnDecorator(sys.stdout), True, 2 if args.verbose else 1)
            start_time = time.time()
            for file_path, req_str in args.input:
                for test_name, test_class in cls.get_tests(args.test_types):
                    for test in test_class.get_test_cases(file_path, req_str):
                        cls.run_test(test, result, args.dry_run)
            cls.print_result(result, start_time)
        except KeyboardInterrupt:
            print_exception("Runner", "run", "Keyboard Interrupt, exiting...")
            exit(0)

    @classmethod
    def run_test(cls, test, result, dry_run=False):
        suite = TestSuite()
        suite.addTest(test("test_case"))
        if dry_run:
            for test in suite:
                print(test)
        else:
            suite(result)

    @classmethod
    def set_env(cls):
        config = MainConfig()
        os.environ["SYNTRIBOS_ENDPOINT"] = config.endpoint

    @classmethod
    def print_result(cls, result, start_time):
        """Prints results summerized"""
        result.printErrors()
        run_time = time.time() - start_time
        tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)

        print("{0}".format("-" * 70))
        print("Ran {0} test{1} in {2:.3f}s".format(
            tests, "s" * bool(tests - 1), run_time))
        if failures or errors:
            print("\nFAILED ({0}{1}{2})".format(
                "failures={0}".format(failures) if failures else "",
                ", " if failures and errors else "",
                "errors={0}".format(errors) if errors else ""))
        cls.print_log()
        return tests, errors, failures


def entry_point():
    Runner.run()
    return 0

if __name__ == '__main__':
    entry_point()
