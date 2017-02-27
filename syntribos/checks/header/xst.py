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
import syntribos.signal


def validate_content(test):
    """Checks if the API is responding to TRACE requests

    Checks if the response body contains the request header
    "TRACE_THIS".

    :returns: SynSignal
    """
    check_name = "VALID_CONTENT"
    strength = 1.0
    tags = []

    if not test.init_signals.ran_check(check_name):
        resp = test.init_resp
    else:
        resp = test.test_resp

    data = {"response_content": resp.text}
    # vulnerable to XST if response body has the request header
    xst_header = "TRACE_THIS: XST_Vuln"
    if "Content-type" in resp.headers:
        content_type = resp.headers["Content-type"]
        data["content_type"] = content_type

    if data["response_content"]:
        if data["response_content"].find(xst_header) != -1:
            text = "Request header in response: {}".format(xst_header)
            slug = "HEADER_XST"

            return syntribos.signal.SynSignal(
                data=data,
                tags=tags,
                text=text,
                slug=slug,
                strength=strength,
                check_name=check_name)
