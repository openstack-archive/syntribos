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
import syntribos.signal


def stacktrace(test):
    """Checks if a stacktrace is returned by the response.

    If a stacktrace is returned, attempts to identity if it was an
    application failure or a server failure and return appropriate
    tags.

    returns a signal with the stacktrace slug.

    :returns: SynSignal
    """
    error_string = 'Traceback (most recent call last):'
    strength = 1.0
    tags = ["APPLICATION_FAIL"]
    slug = "STACKTRACE_PRESENT"
    check_name = "STACKTRACE"
    if not test.init_signals.ran_check(check_name):
        resp = test.init_resp
    else:
        resp = test.test_resp
    if error_string in resp.text:
        text = ("Stacktrace detected: {0}\n".format(
            resp.text[resp.text.index(error_string):]))
        return syntribos.signal.SynSignal(text=text, tags=tags,
                                          slug=slug, strength=strength,
                                          check_name=check_name)
