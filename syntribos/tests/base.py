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
import os
import string as t_string

import cafe.drivers.unittest.fixtures
import six
from six.moves.urllib.parse import urlparse

import syntribos
from syntribos.clients.http import client
from syntribos.clients.http import parser
from syntribos.signal import SignalHolder


ALLOWED_CHARS = "().-_{0}{1}".format(t_string.ascii_letters, t_string.digits)

"""test_table is the master list of tests to be run by the runner"""
test_table = {}


def replace_invalid_characters(string, new_char="_"):
    """Replace invalid characters in test names

    This function corrects `string` so the following is true.

    Identifiers (also referred to as names) are described by the
    following lexical definitions:

    | ``identifier ::=  (letter|"_") (letter | digit | "_")*``
    | ``letter     ::=  lowercase | uppercase``
    | ``lowercase  ::=  "a"..."z"``
    | ``uppercase  ::=  "A"..."Z"``
    | ``digit      ::=  "0"..."9"``

    :param str string: Test name
    :param str new_char: The character to replace invalid characters with
    :returns: The test name, with invalid characters replaced with `new_char`
    :rtype: str
    """
    if not string:
        return string
    for char in set(string) - set(ALLOWED_CHARS):
        string = string.replace(char, new_char)
    if string[0] in t_string.digits:
        string = string.replace(string[0], new_char, 1)
    return string


class TestType(type):

    """This is the metaclass for each class extending :class:`BaseTestCase`."""

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

    """Base class for building new tests

    :attribute str test_name: A name like ``XML_EXTERNAL_ENTITY_BODY``,
        containing the test type and the portion of the request template being
        tested
    :attribute list failures: A collection of "failures" raised by tests
    :attribute bool dead: Flip this if one of the requests doesn't return a
        response object
    :attribute client: HTTP client to be used by the test
    :attribute init_req: Initial request (loaded from request template)
    :attribute init_resp: Response to the initial request
    :attribute test_req: Request sent by the test for analysis
    :attribute test_resp: Response to the test request
    :attribute init_signals: Holder for signals on `init_req`
    :attribute test_signals: Holder for signals on `test_req`
    :attribute diff_signals: Holder for signals between `init_req` and
        `test_req`
    """

    test_name = None
    failures = []
    dead = False
    client = client()

    init_req = None
    init_resp = None
    test_req = None
    test_resp = None

    init_signals = SignalHolder()
    test_signals = SignalHolder()
    diff_signals = SignalHolder()

    @classmethod
    def get_test_cases(cls, filename, file_content):
        """Returns tests for given TestCase class (overwritten by children)."""
        yield cls

    @classmethod
    def send_init_request(cls, filename, file_content, parser=parser):
        request_obj = parser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT"))
        prepared_copy = request_obj.get_prepared_copy()
        cls.init_resp, cls.init_signals = cls.client.send_request(
            prepared_copy)
        cls.init_req = request_obj
        if cls.init_resp is None:
            cls.dead = True

    @classmethod
    def extend_class(cls, new_name, kwargs):
        """Creates an extension for the class

        Each TestCase class created is added to the `test_table`, which is then
        read in by the test runner as the master list of tests to be run.

        :param str new_name: Name of new class to be created
        :param dict kwargs: Keyword arguments to pass to the new class
        :rtype: class
        :returns: A TestCase class extending :class:`BaseTestCase`
        """

        new_name = replace_invalid_characters(new_name)
        if not isinstance(kwargs, dict):
            raise Exception("kwargs must be a dictionary")
        new_cls = type(new_name, (cls, ), kwargs)
        new_cls.__module__ = cls.__module__
        return new_cls

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        if not cls.failures:
            if "EXCEPTION_RAISED" in cls.test_signals:
                sig = cls.test_signals.get_matching_signals(
                    tags="EXCEPTION_RAISED")[0]
                raise sig.data["exception"]

    def run_test(self):
        """This kicks off the test(s) for a given TestCase class

        After running the tests, an `AssertionError` is raised if any tests
        were added to self.failures.

        :raises: :exc:`AssertionError`
        """
        if not self.dead:
            self.test_case()
            if self.failures:
                raise AssertionError

    def test_case(self):
        """This method is overwritten by individual TestCase classes

        It represents the actual test that is called in :func:`run_test`,
        and handles populating `self.failures`
        """
        pass

    def register_issue(self, defect_type, severity, confidence, description):
        """Adds an issue to the test's list of issues

        Creates a :class:`syntribos.issue.Issue` object, with given function
        parameters as instances variables, and registers the issue as a
        failure and associates the test's metadata to it.

        :param defect_type: The type of vulnerability that Syntribos believes
        it has found. This may be something like 500 error or DoS, regardless
        tof whathe Test Type is.
        :param severity: "Low", "Medium", or "High", depending on the defect
        :param description: Description of the defect
        :param confidence: The confidence of the defect
        :returns: new issue object with metadata associated
        :rtype: Issue
        """

        issue = syntribos.Issue(defect_type=defect_type,
                                severity=severity,
                                confidence=confidence,
                                description=description)

        # Still associating request and response objects with issue in event of
        # debug log
        issue.request = self.test_req
        issue.response = self.test_resp

        issue.test_type = self.test_name
        url_components = urlparse(self.init_resp.url)
        issue.target = url_components.netloc
        issue.path = url_components.path

        self.failures.append(issue)

        return issue
