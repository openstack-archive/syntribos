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


def has_string(test):
    """Checks if the response consists of any failure strings

    :returns: syntribos.signal.SynSignal
    """

    slug = "FAILURE_KEYS_PRESENT"
    data = {
        "req": test.test_resp.request,
        "resp": test.test_resp,
        "failed_strings": []
    }

    failure_keys = test.failure_keys
    if failure_keys:
        data["failed_strings"] = [key for key in failure_keys
                                  if key in test.test_resp.text]

    if len(data["failed_strings"]) > 0:
        keys = "\n".join([str(s) for s in data["failed_strings"]])
        text = "Failed strings present " + keys
        return syntribos.signal.SynSignal(
            check_name="has_string",
            text=text,
            slug=slug,
            data=data,
            strength=1.0)
