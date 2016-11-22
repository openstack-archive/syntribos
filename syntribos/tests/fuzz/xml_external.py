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
from oslo_config import cfg

import syntribos
from syntribos.checks import has_string as has_string
from syntribos.checks import time_diff as time_diff
from syntribos.clients.http import parser
from syntribos.tests.fuzz import base_fuzz
import syntribos.tests.fuzz.datagen

CONF = cfg.CONF


class XMLExternalEntityBody(base_fuzz.BaseFuzzTestCase):
    """Test for XML-external-entity injection vulnerabilities in HTTP body."""

    test_name = "XML_EXTERNAL_ENTITY_BODY"
    test_type = "data"
    dtds_data_key = "xml-external.txt"
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
        request_obj = parser.create_request(
            file_content, CONF.syntribos.endpoint)

        prepared_copy = request_obj.get_prepared_copy()
        prepared_copy.headers['content-type'] = "application/json"
        prepared_copy_xml = prepared_copy.get_prepared_copy()
        prepared_copy_xml.headers['content-type'] = "application/xml"

        init_response, init_signals = cls.client.send_request(prepared_copy)
        _, xml_signals = cls.client.send_request(
            prepared_copy_xml)

        cls.init_resp = init_response
        cls.init_signals = init_signals

        if ("HTTP_CONTENT_TYPE_XML" not in init_signals and
                "HTTP_CONTENT_TYPE_XML" not in xml_signals):
            return

        # iterate through permutations of doctype declarations and fuzz fields
        dtds = cls._get_strings(cls.dtds_data_key)
        for d_num, dtd in enumerate(dtds):
            prefix_name = "{filename}_{test_name}_{fuzz_file}{d_index}_"
            prefix_name = prefix_name.format(
                filename=filename, test_name=cls.test_name,
                fuzz_file=cls.dtds_data_key, d_index=d_num)
            fr = syntribos.tests.fuzz.datagen.fuzz_request(
                request_obj, ["&xxe;"], cls.test_type, prefix_name)
            for fuzz_name, request, fuzz_string, param_path in fr:
                request.data = "{0}\n{1}".format(dtd, request.data)
                yield cls.extend_class(fuzz_name, fuzz_string, param_path,
                                       {"request": request})

    def test_case(self):
        self.run_default_checks()
        self.test_signals.register(has_string(self))
        if "FAILURE_KEYS_PRESENT" in self.test_signals:
            failed_strings = self.test_signals.find(
                slugs="FAILURE_KEYS_PRESENT")[0].data["failed_strings"]
            self.register_issue(
                defect_type="xml_strings",
                severity=syntribos.MEDIUM,
                confidence=syntribos.LOW,
                description=("The string(s): '{0}', known to be commonly "
                             "returned after a successful XML external entity "
                             "attack, have been found in the response. This "
                             "could indicate a vulnerability to XML external "
                             "entity attacks.").format(failed_strings))

        self.diff_signals.register(time_diff(self))
        if "TIME_DIFF_OVER" in self.diff_signals:
            self.register_issue(
                defect_type="xml_timing",
                severity=syntribos.MEDIUM,
                confidence=syntribos.MEDIUM,
                description=("The time it took to resolve a request with an "
                             "invalid URL in the DTD takes too long compared "
                             "to the baseline request. This could reflect a "
                             "vulnerability to an XML external entity attack.")
            )
