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
import re

from six.moves.urllib.parse import urlparse

import syntribos.signal


def https_check(test):
    """Checks if the returned response consists of non-secure endpoint URIs

    :returns: syntribos.signal.SynSignal
    """
    check_name = "HTTPS_CHECK"
    if not test.init_signals.ran_check(check_name):
        response_text = test.init_resp.text
    else:
        response_text = test.test_resp.text
    target = test.init_req.url
    domain = urlparse(target).hostname
    regex = r"\bhttp://{0}".format(domain)

    if re.search(regex, response_text):
        text = "Non https endpoint URIs present in the response text"
        slug = "HTTP_LINKS_PRESENT"
        return syntribos.signal.SynSignal(text=text, slug=slug,
                                          strength=1.0, check_name=check_name)
