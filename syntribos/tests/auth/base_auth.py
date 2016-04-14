# Copyright 2016 Rackspace
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
from syntribos.issue import Issue
import syntribos.tests.auth.datagen
from syntribos.tests import base

data_dir = os.environ.get("CAFE_DATA_DIR_PATH")


class BaseAuthTestCase(base.BaseTestCase):
    client = client()
    failure_keys = None
    success_keys = None

    @classmethod
    def data_driven_failure_cases(cls):
        failure_assertions = []
        if cls.failure_keys is None:
            return []
        for line in cls.failure_keys:
            failure_assertions.append((cls.assertNotIn,
                                      line, cls.resp.content))
        return failure_assertions

    @classmethod
    def data_driven_pass_cases(cls):
        if cls.success_keys is None:
            return True
        for s in cls.success_keys:
            if s in cls.resp.content:
                return True
        return False

    @classmethod
    def setUpClass(cls):
        super(BaseAuthTestCase, cls).setUpClass()
        cls.issues = []
        cls.failures = []
        cls.resp = cls.client.request(
            method=cls.request.method, url=cls.request.url,
            headers=cls.request.headers, params=cls.request.params,
            data=cls.request.data)

    @classmethod
    def tearDownClass(cls):
        super(BaseAuthTestCase, cls).tearDownClass()
        for issue in cls.issues:
            if issue.failure:
                cls.failures.append(issue.as_dict())

    def test_case(self):
        text = ("This request did not fail with 404 (User not found)"
                " therefore it indicates that authentication with"
                " another user's token was successful.")
        self.register_issue(
            Issue(test="try_alt_user_token",
                  severity="High",
                  text=text,
                  assertions=[(self.assertTrue, self.resp.status_code == 404)])
        )
        self.test_issues()

    @classmethod
    def get_test_cases(cls, filename, file_content):
        """Generates the test cases

        For this particular test, only a single test
        is created (in addition to the base case, that is)
        """

        alt_user_config = syntribos.extensions.identity.config.UserConfig(
            section_name='alt_user')
        alt_user_id = alt_user_config.user_id
        if alt_user_id is None:
            return

        request_obj = syntribos.tests.auth.datagen.AuthParser.create_request(
            file_content, os.environ.get("SYNTRIBOS_ENDPOINT"))

        prepared_copy = request_obj.get_prepared_copy()
        cls.init_response = cls.client.send_request(prepared_copy)

        prefix_name = "{filename}_{test_name}_{fuzz_file}_".format(
            filename=filename, test_name=cls.test_name, fuzz_file='auth')

        main_config = syntribos.config.MainConfig()
        version = main_config.version

        if version is None or version == 'v2':
            alt_token = syntribos.extensions.identity.client.get_token_v2(
                'alt_user', 'auth')
        else:
            alt_token = syntribos.extensions.identity.client.get_token_v3(
                'alt_user', 'auth')
        alt_user_token_request = request_obj.get_prepared_copy()
        for h in alt_user_token_request.headers:
            if 'x-auth-token' == h.lower():
                alt_user_token_request.headers[h] = alt_token

        test_name = prefix_name + 'another_users_token'

        def test_gen(test_name, request):
            yield (test_name, request)

        for name, req in test_gen(test_name, alt_user_token_request):
            c = cls.extend_class(test_name,
                                 {"request": alt_user_token_request})
            yield c
