# Copyright 2016 Intel
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
import sys

import testtools

from syntribos.result import IssueTestResult


class FakeTest(object):
    def __init__(self, name):
        self.failures = [1, 2]
        self.errors = [3, 4]
        self.successes = [5, 6]
        self.name = name
        self.failureException = Exception

    def __str__(self):
        return self.name


class TestIssueTestResult(testtools.TestCase):
    """Class to test methods in IssueTestResult class."""

    issue_result = IssueTestResult(None, False, 0)

    def test_addFailure(self):
        test = FakeTest("failure")
        self.issue_result.addFailure(test, ())
        self.assertEqual(self.issue_result.stats["failures"], 2)

    def test_addError(self):
        test = FakeTest("error")
        self.issue_result.addError(test, sys.exc_info())
        self.assertEqual(self.issue_result.stats["errors"], 1)

    def test_addSuccess(self):
        test = FakeTest("success")
        self.issue_result.addSuccess(test)
        self.assertEqual(self.issue_result.stats["successes"], 1)
