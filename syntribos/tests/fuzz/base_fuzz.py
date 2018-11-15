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
# pylint: skip-file
import logging
import os

from oslo_config import cfg
from six.moves.urllib.parse import urlparse

import syntribos
from syntribos.checks import length_diff as length_diff
from syntribos.tests import base
import syntribos.tests.fuzz.datagen
from syntribos.utils.file_utils import ContentType
from syntribos.utils import remotes

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class BaseFuzzTestCase(base.BaseTestCase):
    failure_keys = None
    success_keys = None

    @classmethod
    def _get_strings(cls, file_name=None):
        payloads = CONF.syntribos.payloads
        if not payloads:
            payloads = remotes.get(CONF.remote.payloads_uri)
        content = ContentType('r')(payloads)
        for file_path, _ in content:
            if file_path.endswith(".txt"):
                file_dir = os.path.split(file_path)[0]
                payloads = os.path.join(payloads, file_dir)
                break
        try:
            if os.path.isfile(cls.data_key):
                path = cls.data_key
            else:
                path = os.path.join(payloads, file_name or cls.data_key)
            with open(path, "r") as fp:
                return fp.read().splitlines()
        except (IOError, AttributeError, TypeError) as e:
            LOG.error("Exception raised: {}".format(e))
            print("\nPayload file for test '{}' not readable, "
                  "exiting...".format(cls.test_name))
            exit(1)

    @classmethod
    def setUpClass(cls):
        """being used as a setup test not."""
        super(BaseFuzzTestCase, cls).setUpClass()
        cls.test_resp, cls.test_signals = cls.client.request(
            method=cls.request.method,
            url=cls.request.url,
            headers=cls.request.headers,
            params=cls.request.params,
            data=cls.request.data)

        if not hasattr(cls.request, 'body'):
            cls.request.body = cls.request.data
        cls.test_req = cls.request

        if cls.test_resp is None or "EXCEPTION_RAISED" in cls.test_signals:
            cls.dead = True

    @classmethod
    def tearDownClass(cls):
        super(BaseFuzzTestCase, cls).tearDownClass()

    def run_default_checks(self):
        """Tests for some default issues

        These issues are not specific to any test type, and can be raised as a
        result of many different types of attacks. Therefore, they're defined
        separately from the test_case method so that they are not overwritten
        by test cases that inherit from BaseFuzzTestCase.

        Any extension to this class should call
        self.run_default_checks() in order to test for the Issues
        defined here
        """
        if "HTTP_STATUS_CODE_5XX" in self.test_signals:
            self.register_issue(
                defect_type="500_errors",
                severity=syntribos.LOW,
                confidence=syntribos.HIGH,
                description=("This request returns an error with status code "
                             "{0}, which might indicate some server-side "
                             "fault that may lead to further vulnerabilities"
                             ).format(self.test_resp.status_code))
        self.diff_signals.register(length_diff(self))
        if "LENGTH_DIFF_OVER" in self.diff_signals:
            if self.init_resp.status_code == self.test_resp.status_code:
                description = ("The difference in length between the response "
                               "to the baseline request and the request "
                               "returned when sending an attack string "
                               "exceeds {0} percent, which could indicate a "
                               "vulnerability to injection attacks"
                               ).format(CONF.test.length_diff_percent)
                self.register_issue(
                    defect_type="length_diff",
                    severity=syntribos.LOW,
                    confidence=syntribos.LOW,
                    description=description)

    def test_case(self):
        """Performs the test

        The test runner will call test_case on every TestCase class, and will
        report any AssertionError raised by this method to the results.
        """
        self.run_default_checks()

    @classmethod
    def get_test_cases(cls, filename, file_content, meta_vars):
        """Generates new TestCases for each fuzz string

        For each string returned by cls._get_strings(), yield a TestCase class
        for the string as an extension to the current TestCase class. Every
        string used as a fuzz test payload entails the generation of a new
        subclass for each parameter fuzzed. See :func:`base.extend_class`.
        """
        cls.failures = []
        if hasattr(cls, 'data_key'):
            prefix_name = "{filename}_{test_name}_{fuzz_file}_".format(
                filename=filename,
                test_name=cls.test_name,
                fuzz_file=cls.data_key)
        else:
            prefix_name = "{filename}_{test_name}_".format(
                filename=filename, test_name=cls.test_name)

        fr = syntribos.tests.fuzz.datagen.fuzz_request(
            cls.init_req, cls._get_strings(), cls.parameter_location,
            prefix_name)
        for fuzz_name, request, fuzz_string, param_path in fr:
            yield cls.extend_class(fuzz_name, fuzz_string, param_path,
                                   {"request": request})

    @classmethod
    def extend_class(cls, new_name, fuzz_string, param_path, kwargs):
        """Creates an extension for the class

        Each TestCase class created is added to the `test_table`, which is then
        read in by the test runner as the master list of tests to be run.

        :param str new_name: Name of new class to be created
        :param str fuzz_string: Fuzz string to insert
        :param str param_path: String tracing location of the ImpactedParameter
        :param dict kwargs: Keyword arguments to pass to the new class
        :rtype: class
        :returns: A TestCase class extending :class:`BaseTestCase`
        """

        new_cls = super(BaseFuzzTestCase, cls).extend_class(new_name, kwargs)
        new_cls.fuzz_string = fuzz_string
        new_cls.param_path = param_path
        return new_cls

    def register_issue(self, defect_type, severity, confidence, description):
        """Adds an issue to the test's list of issues

        Creates a :class:`syntribos.issue.Issue` object, with given function
        parameters as instance variables, registers the Issue as a
        failure, and associates the test's metadata to it, including the
        :class:`syntribos.tests.fuzz.base_fuzz.ImpactedParameter` object that
        encapsulates the details of the fuzz test.

        :param defect_type: The type of vulnerability that Syntribos believes
        it has found. This may be something like 500 error or DoS, regardless
        of what the Test Type is.
        :param severity: "Low", "Medium", or "High", depending on the defect
        :param description: Description of the defect
        :param confidence: The confidence in the validity of the defect
        :returns: new issue object with metadata associated
        :rtype: :class:`syntribos.issue.Issue`
        """

        issue = syntribos.Issue(
            defect_type=defect_type,
            severity=severity,
            confidence=confidence,
            description=description)

        issue.request = self.test_req
        issue.response = self.test_resp
        issue.template_path = self.template_path

        issue.test_type = self.test_name
        url_components = urlparse(self.prepared_init_req.url)
        issue.target = url_components.netloc
        issue.path = url_components.path
        issue.init_signals = self.init_signals
        issue.test_signals = self.test_signals
        issue.diff_signals = self.diff_signals
        if 'content-type' in self.init_req.headers:
            issue.content_type = self.init_req.headers['content-type']
        else:
            issue.content_type = None

        issue.impacted_parameter = ImpactedParameter(
            method=issue.request.method,
            location=self.parameter_location,
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
        if len(value) >= 128:
            self.trunc_fuzz_string = "{0}...({1} chars)...{2}".format(
                value[:64], len(value), value[-64:])
        else:
            self.trunc_fuzz_string = value
        self.fuzz_string = value
        self.name = name

    def as_dict(self):
        return {
            "method": self.method,
            "location": self.location,
            "name": self.name,
            "value": self.trunc_fuzz_string
        }
