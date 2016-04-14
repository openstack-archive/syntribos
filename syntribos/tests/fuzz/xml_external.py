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
from syntribos.issue import Issue
from syntribos.tests.fuzz import base_fuzz


class XMLExternalEntityBody(base_fuzz.BaseFuzzTestCase):
    test_name = "XML_EXTERNAL_ENTITY_BODY"
    test_type = "data"
    data_key = "xml-external.txt"
    failure_keys = [
        'root:',
        'root@',
        'daemon:',
        'sys:',
        '[boot loader]',
        '[operating systems]',
        'multi(0)',
        'disk(0)',
        'partition']

    def test_case(self):
        self.test_default_issues()
        failed_strings = self.data_driven_failure_cases()
        if failed_strings:
            self.register_issue(
                Issue(test="xml_strings",
                      severity="Medium",
                      confidence="Low",
                      text=("The string(s): \'{0}\', known to be commonly "
                            "returned after a successful XML external entity "
                            "attack, have been found in the response. This "
                            "could indicate a vulnerability to XML external "
                            "entity attacks.").format(failed_strings)
                      )
            )


class XMLExternalEntityParams(XMLExternalEntityBody):
    test_name = "XML_EXTERNAL_ENTITY_PARAMS"
    test_type = "params"


class XMLExternalEntityHeaders(XMLExternalEntityBody):
    test_name = "XML_EXTERNAL_ENTITY_HEADERS"
    test_type = "headers"


class XMLExternalEntityURL(XMLExternalEntityBody):
    test_name = "XML_EXTERNAL_ENTITY_URL"
    test_type = "url"
    url_var = "FUZZ"
