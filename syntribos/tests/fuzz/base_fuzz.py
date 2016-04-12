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

import os

from six.moves.urllib.parse import urlparse

from syntribos.clients.http import client
from syntribos.issue import Issue
from syntribos.tests import base
import syntribos.tests.fuzz.config
import syntribos.tests.fuzz.datagen

data_dir = os.environ.get("CAFE_DATA_DIR_PATH")


class BaseFuzzTestCase(base.BaseTestCase):
    config = syntribos.tests.fuzz.config.BaseFuzzConfig()
    client = client()
    failure_keys = None
    success_keys = None

    @classmethod
    def validate_length(cls):
        """Validates length of response

        Compares the length of a fuzzed response with a response to the
        baseline request. If the response is longer than expected, returns
        false

        :returns: boolean - whether the response is longer than expected
        """
        if getattr(cls, "init_response", False) is False:
            raise NotImplemented
        init_req_len = len(cls.init_response.request.body or "")
        init_resp_len = len(cls.init_response.content or "")
        req_len = len(cls.resp.request.body or "")
        resp_len = len(cls.resp.content or "")
        request_diff = req_len - init_req_len
        response_diff = resp_len - init_resp_len
        percent_diff = abs(float(response_diff) / (init_resp_len + 1)) * 100
        msg = (
            "Validate Length:\n"
            "\tInitial request length: {0}\n"
            "\tInitial response length: {1}\n"
            "\tRequest length: {2}\n"
            "\tResponse length: {3}\n"
            "\tRequest difference: {4}\n"
            "\tResponse difference: {5}\n"
            "\tPercent difference: {6}\n"
            "\tConfig percent: {7}\n").format(
            init_req_len, init_resp_len, req_len, resp_len, request_diff,
            response_diff, percent_diff, cls.config.percent)
        cls.fixture_log.debug(msg)
        if request_diff == response_diff:
            return True
        elif resp_len == init_resp_len:
            return True
        elif cls.config.percent:
            if percent_diff <= cls.config.percent:
                return True
        return False

    @classmethod
    def _get_strings(cls, file_name=None):
        path = os.path.join(data_dir, file_name or cls.data_key)
        with open(path, "rb") as fp:
            return fp.read().splitlines()

    @classmethod
    def data_driven_failure_cases(cls):
        """Checks if response contains known bad strings

        :returns: a list of strings that show up in the response that are also
        defined in cls.failure_strings.
        failed_strings = []
        """
        failed_strings = []
        if cls.failure_keys is None:
            return []
        for line in cls.failure_keys:
            if line in cls.resp.content:
                failed_strings.append(line)
        return failed_strings

    @classmethod
    def data_driven_pass_cases(cls):
        """Checks if response contains expected strings

        :returns: a list of assertions that fail if the response doesn't
        contain a string defined in cls.success_keys as a string expected in
        the response.
        """
        if cls.success_keys is None:
            return True
        for s in cls.success_keys:
            if s in cls.resp.content:
                return True
        return False

    @classmethod
    def setUpClass(cls):
        """being used as a setup test not."""
        super(BaseFuzzTestCase, cls).setUpClass()
        cls.failures = []
        cls.resp = cls.client.request(
            method=cls.request.method, url=cls.request.url,
            headers=cls.request.headers, params=cls.request.params,
            data=cls.request.data)

    @classmethod
    def tearDownClass(cls):
        super(BaseFuzzTestCase, cls).tearDownClass()

    def test_default_issues(self):
        """Tests for some default issues

        These issues are not specific to any test type, and can be raised as a
        result of many different types of attacks. Therefore, they're defined
        separately from the test_case method so that they are not overwritten
        by test cases that inherit from BaseFuzzTestCase.

        Any extension to this class should call
        self.test_default_issues() in order to test for the Issues
        defined here
        """
        if self.resp.status_code >= 500:
            self.register_issue(
                Issue(test="500_errors",
                      severity="Low",
                      confidence="High",
                      text=("This request returns an error with status code "
                            "{0}, which might indicate some server-side fault"
                            "that could lead to further vulnerabilities"
                            ).format(self.resp.status_code)
                      )
            )

        if not self.validate_length():
            self.register_issue(
                Issue(test="length_diff",
                      severity="Low",
                      confidence="Low",
                      text=("The difference in length between the response to"
                            "the baseline request and the request returned"
                            "when sending an attack string exceeds {0}"
                            "percent, which could indicate a vulnerability to"
                            "injection attacks")
                      .format(self.config.percent)
                      )
            )

    def test_case(self):
        """Performs the test

        The test runner will call test_case on every TestCase class, and will
        report any AssertionError raised by this method to the results.
        """
        self.test_default_issues()

    @classmethod
    def get_test_cases(cls, filename, file_content):
        """Generates new TestCases for each fuzz string

        First, sends a baseline (non-fuzzed) request, storing it in
        cls.init_response.

        For each string returned by cls._get_strings(), yield a TestCase class
        for the string as an extension to the current TestCase class. Every
        string used as a fuzz test payload entails the generation of a new
        subclass for each parameter fuzzed. See :func:`base.extend_class`.
        """
        # maybe move this block to base.py
        request_obj = syntribos.tests.fuzz.datagen.FuzzParser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT"))
        prepared_copy = request_obj.get_prepared_copy()
        cls.init_response = cls.client.send_request(prepared_copy)
        # end block

        prefix_name = "{filename}_{test_name}_{fuzz_file}_".format(
            filename=filename, test_name=cls.test_name, fuzz_file=cls.data_key)
        fr = request_obj.fuzz_request(
            cls._get_strings(), cls.test_type, prefix_name)
        for fuzz_name, request, fuzz_string, param_path in fr:
            yield cls.extend_class(fuzz_name, fuzz_string, param_path,
                                   {"request": request})

    def register_issue(self, issue):
        """Adds an issue to the test's list of issues

        Registers a :class:`syntribos.issue.Issue` object as a failure and
        associates the test's metadata to it, including the
        :class:`syntribos.tests.fuzz.base_fuzz.ImpactedParameter` object that
        encapsulates the details of the fuzz test.

        :param Issue issue: issue object to update
        :returns: new issue object with metadata associated
        :rtype: Issue
        """

        # Still associating request and response objects with issue in event of
        # debug log
        req = self.resp.request
        issue.request = req
        issue.response = self.resp

        issue.test_type = self.test_name
        url_components = urlparse(self.resp.request.url)
        issue.target = url_components.netloc
        issue.path = url_components.path

        issue.impacted_parameter = ImpactedParameter(method=req.method,
                                                     location=self.test_type,
                                                     name=self.param_path,
                                                     value=self.fuzz_string)

        self.failures.append(issue)

        return issue


class ImpactedParameter(object):
    """Object that encapsulates the details about what caused the defect

    :ivar method: The HTTP method used in the test
    :ivar location: The location of the impacted parameter
    :ivar name: The parameter (e.g. HTTP header, GET var) that was modified by
        a given test case
    :ivar value: The "fuzz" string that was supplied in a given test case
    :ivar request_body_format: The type of a body (POST/PATCH/etc.) variable.
    """

    def __init__(self, method, location, name, value):
        self.method = method
        self.location = location
        self.fuzz_string = value
        self.name = name

    def as_dict(self):
        trunc_string = self.fuzz_string
        if len(self.fuzz_string) >= 512:
            trunc_string = "{0}...({1} chars)...{2}".format(
                self.fuzz_string[:256], len(self.fuzz_string),
                self.fuzz_string[-256:])
        return {
            "method": self.method,
            "location": self.location,
            "name": self.name,
            "value": trunc_string
        }
