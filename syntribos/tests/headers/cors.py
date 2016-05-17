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
import os

from syntribos.clients.http import client
from syntribos.clients.http import parser
from syntribos.issue import Issue
from syntribos.tests import base


class CorsHeader(base.BaseTestCase):

    """Test to check if CORS header variables are set to wild characters."""

    test_name = "CORS_HEADER"
    test_type = "headers"
    client = client()
    failures = []

    @classmethod
    def get_test_cases(cls, filename, file_content):

        request_obj = parser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT")
        )
        request_obj.headers['Origin'] = 'http://example.com'
        cls.resp = cls.client.send_request(request_obj)
        yield cls

    def test_case(self):

        if 'Access-Control-Allow-Origin' in self.resp.headers:
            if self.resp.headers['Access-Control-Allow-Origin'] == "*":
                self.register_issue(
                    Issue(test="CORS_HEADER",
                          severity="Medium",
                          confidence="High",
                          text=("CORS header `Access-Control-Allow-Origin` set"
                                " to a wild character, this header should"
                                " always be set to a white listed set of URIs"
                                )
                          )
                )

        if 'Access-Control-Allow-Methods' in self.resp.headers:
            if self.resp.headers['Access-Control-Allow-Methods'] == "*":
                self.register_issue(
                    Issue(test="CORS_HEADER",
                          severity="Low",
                          confidence="High",
                          text=("CORS header `Access-Control-Allow-Methods`"
                                " set to a wild character,it is a good"
                                " practice to give a white list of allowed"
                                " methods."
                                )
                          )
                )

        if 'Access-Control-Allow-Headers' in self.resp.headers:
            if self.resp.headers['Access-Control-Allow-Headers'] == "*":
                self.register_issue(
                    Issue(test="CORS_HEADER",
                          severity="Low",
                          confidence="High",
                          text=("CORS header `Access-Control-Allow-Headers`"
                                " set to a wild character,it is a good"
                                " practice to give a white list of allowed"
                                " headers"
                                )
                          )
                )
