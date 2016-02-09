"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import six

import string as t_string

import cafe.drivers.unittest.fixtures

from syntribos.issue import Issue

ALLOWED_CHARS = "().-_{0}{1}".format(t_string.ascii_letters, t_string.digits)

'''test_table is the master list of tests to be run by the runner'''
test_table = {}


def replace_invalid_characters(string, new_char="_"):
    """Replace invalid characters

    This functions corrects string so the following is true
    Identifiers (also referred to as names) are described by the
    following lexical definitions:
    identifier ::=  (letter|"_") (letter | digit | "_")*
    letter     ::=  lowercase | uppercase
    lowercase  ::=  "a"..."z"
    uppercase  ::=  "A"..."Z"
    digit      ::=  "0"..."9"
    """
    if not string:
        return string
    for char in set(string) - set(ALLOWED_CHARS):
        string = string.replace(char, new_char)
    if string[0] in t_string.digits:
        string = string.replace(string[0], new_char, 1)
    return string


class TestType(type):
    def __new__(cls, cls_name, cls_parents, cls_attr):
        new_class = super(TestType, cls).__new__(
            cls, cls_name, cls_parents, cls_attr)
        test_name = getattr(new_class, "test_name", None)
        if test_name is not None:
            if test_name not in test_table:
                test_table[test_name] = new_class
        return new_class


@six.add_metaclass(TestType)
class BaseTestCase(cafe.drivers.unittest.fixtures.BaseTestFixture):
    """Base Class

    Base for building new tests
    """
    test_name = None

    @classmethod
    def get_test_cases(cls, filename, file_content):
        yield cls

    @classmethod
    def extend_class(cls, new_name, kwargs):
        '''Creates an extension for the class

        Each TestCase class created is added to the test_table, which is then
        read in by the test runner as the master list of tests to be run.
        '''
        new_name = replace_invalid_characters(new_name)
        if not isinstance(kwargs, dict):
            raise Exception("kwargs must be a dictionary")
        new_cls = type(new_name, (cls, ), kwargs)
        new_cls.__module__ = cls.__module__
        return new_cls

    def test_case(self):
        pass

    def register_issue(self, issue=None):
        """Adds an issue to the test's list of issues

        Creates a new issue object, and associates the test's request
        and response to it. In addition, adds the issue to the test's
        list of issues
        """

        if not issue:
            issue = Issue()
        issue.request = self.resp.request
        issue.response = self.resp

        self.issues.append(issue)

        return issue

    def test_issues(self):
        '''run assertions for each test registered in test_case.'''
        for issue in self.issues:
            issue.run_tests()
