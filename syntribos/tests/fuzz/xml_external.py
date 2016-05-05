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
import os

from syntribos.issue import Issue
from syntribos.tests.fuzz import base_fuzz
import syntribos.tests.fuzz.datagen


class XMLExternalEntityBody(base_fuzz.BaseFuzzTestCase):
    test_name = "XML_EXTERNAL_ENTITY_BODY"
    test_type = "data"
    dtds_data_key = "xml-external.txt"
    config = syntribos.tests.fuzz.config.BaseFuzzConfig()
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

    @classmethod
    def get_test_cases(cls, filename, file_content):
        """Makes sure API call supports XML

        Overrides parent fuzz test generation, if API method does not support
        XML, do not generate tests.
        """
        # Send request for different content-types
        request_obj = syntribos.tests.fuzz.datagen.FuzzParser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT"))

        prepared_copy = request_obj.get_prepared_copy()
        prepared_copy.headers['content-type'] = "application/json"
        prepared_copy_xml = prepared_copy.get_prepared_copy()
        prepared_copy_xml.headers['content-type'] = "application/xml"

        init_response = cls.client.send_request(prepared_copy)
        init_response_xml = cls.client.send_request(prepared_copy_xml)

        cls.init_response = init_response

        content_type = init_response.headers['content-type']
        content_type_xml_request = init_response_xml.headers['content-type']
        if ('xml' not in content_type and
                'xml' not in content_type_xml_request):
            return

        if (init_response.status_code in (400, 415) or
                init_response_xml.status_code in (400, 415)):
            return

        # iterate through permutations of doctype declarations and fuzz fields
        dtds = cls._get_strings(cls.dtds_data_key)
        for d_num, dtd in enumerate(dtds):
            prefix_name = "{filename}_{test_name}_{fuzz_file}{d_index}_"
            prefix_name = prefix_name.format(
                filename=filename, test_name=cls.test_name,
                fuzz_file=cls.dtds_data_key, d_index=d_num)
            fr = request_obj.fuzz_request(
                ["&xxe;"], cls.test_type, prefix_name)
            for fuzz_name, request, fuzz_string, param_path in fr:
                request.data = "{0}\n{1}".format(dtd, request.data)
                yield cls.extend_class(fuzz_name, fuzz_string, param_path,
                                       {"request": request})

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

        time_diff = self.config.time_difference_percent / 100
        # Timing attacks for requesting invalid url in dtd
        if (self.resp.elapsed.total_seconds() >
                time_diff * self.init_response.elapsed.total_seconds()):
            self.register_issue(
                Issue(test="xml_timing",
                      severity="Medium",
                      confidence="Medium",
                      text=("The time it took to resolve a request with an "
                            "invalid URL in the DTD takes too long compared "
                            "to the baseline request. This could reflect a "
                            "vulnerability to an XML external entity attack."))
            )
