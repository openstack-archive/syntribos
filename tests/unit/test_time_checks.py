# Copyright 2017 Intel
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
import testtools

import syntribos.checks.time as time_checks
import syntribos.signal


class _FakeSignal(object):

    def ran_check(self, check_name):
        return True


class _FakeElapsedObject(object):

    def __init__(self, seconds):
        self.seconds = seconds

    def total_seconds(self):
        return self.seconds


class _FakeRequestObject(object):

    def __init__(self, seconds=10):
        self.request = "request"
        self.elapsed = _FakeElapsedObject(seconds)


class _FakeTestObject(object):

    def __init__(self, seconds=10, diff=False):
        self.init_req = _FakeRequestObject(seconds)  # noqa
        self.init_resp = _FakeRequestObject(seconds)  # noqa
        if diff:
            seconds += 1000
        self.test_req = _FakeRequestObject(seconds)  # noqa
        self.test_resp = _FakeRequestObject(seconds)  # noqa
        self.init_signals = _FakeSignal()


class TimeCheckUnittest(testtools.TestCase):

    test_0 = _FakeTestObject()
    test_1 = _FakeTestObject(1, diff=True)

    def test_percentage_difference(self):
        signal_0 = time_checks.percentage_difference(self.test_0)
        signal_1 = time_checks.percentage_difference(self.test_1)
        self.assertIsNone(signal_0)
        self.assertTrue(isinstance(signal_1, syntribos.signal.SynSignal))

    def test_absolute_time(self):
        signal_0 = time_checks.absolute_time(self.test_0)
        self.assertTrue(isinstance(signal_0, syntribos.signal.SynSignal))
