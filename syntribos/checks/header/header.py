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


def cors(test):
    """Checks if the response header has any CORS headers.

    If any cross origin resource sharing headers (CORS) are found,
    checks if any is set to wild characters, if so returns a Signal.

    :param test object
    :returns: Signal if cors vulnerability is found, other wise None
    :rtype: :class:`syntribos.signal.SynSignal, None`
    """
    check_name = "HEADER_CORS"
    strength = 1.0
    slug = "HEADER_CORS{0}_WILDCARD"
    cors_type = ""
    places = ['Origin', 'Methods', 'Headers']
    cors_headers = ["Access-Control-Allow-{0}".format(p) for p in places]
    headers = test.test_resp.headers

    for cors_header in cors_headers:
        if headers.get(cors_header) == '*':
            cors_type += "_" + cors_header.upper().split('-')[-1]
            text = ("A wildcard CORS header policy with these details "
                    "was detected: {head}: {value}.\n".format(
                        head=cors_header, value=headers[cors_header]))
    if cors_type == "":
        return None

    slug = slug.format(cors_type)
    return syntribos.signal.SynSignal(text=text, slug=slug, strength=strength,
                                      check_name=check_name)
