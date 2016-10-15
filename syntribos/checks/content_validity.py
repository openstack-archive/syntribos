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
import json
import xml.etree.ElementTree as etree

import syntribos.signal


def valid_content(test):
    """Checks if the response.content is valid.

    Checks if the response.content is either xml or json
    and returns a signal based on if the content is valid
    or not.

    :returns: SynSignal
    """
    check_name = "VALID_CONTENT"
    strength = 1.0
    tags = []
    validity = "VALID"

    if not test.init_signals.ran_check(check_name):
        resp = test.init_resp
    else:
        resp = test.test_resp

    data = {"response_content": resp.content}

    if "Content-type" in resp.headers:
        content_type = resp.headers["Content-type"]
        data["content_type"] = content_type

    if "application/xml" in content_type or "text/html" in content_type:
        try:
            etree.fromstring(resp.text)
        except Exception as e:
            validity = "INVALID"
            tags = ['APPLICATION_FAIL']
            text = str(e)

        text = "\n\tContent is: {0} xml".format(validity.lower())
        slug = "{0}_XML".format(validity)

    elif "application/json" in content_type or "text/json" in content_type:
        try:
            json.loads(resp.text)
        except Exception as e:
            validity = "INVALID"
            tags = ['APPLICATION_FAIL']
            text = str(e)

        text = "\n\tContent is: {0} json".format(validity.lower())
        slug = "{0}_JSON".format(validity)

    else:
        return None
    return syntribos.signal.SynSignal(
        data=data,
        tags=tags,
        text=text,
        slug=slug,
        strength=strength,
        check_name=check_name)
