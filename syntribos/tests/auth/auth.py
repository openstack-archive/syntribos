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
from oslo_config import cfg

import syntribos
import syntribos.config
import syntribos.extensions.identity.client
from syntribos.tests import base

CONF = cfg.CONF


class AuthTestCase(base.BaseTestCase):
    """Test for possible token misuse in keystone."""
    test_name = "AUTH"
    test_type = "headers"

    @classmethod
    def setUpClass(cls):
        super(AuthTestCase, cls).setUpClass()
        version = CONF.user.version

        if not version or version == 'v2.0':
            alt_token = syntribos.extensions.identity.client.get_token_v2(
                'alt_user')
        else:
            alt_token = syntribos.extensions.identity.client.get_token_v3(
                'alt_user')

        cls.request.headers['x-auth-token'] = alt_token

        cls.test_resp, cls.test_signals = cls.client.request(
            method=cls.request.method, url=cls.request.url,
            headers=cls.request.headers, params=cls.request.params,
            data=cls.request.data)

    @classmethod
    def send_init_request(cls, filename, file_content, meta_vars):
        super(AuthTestCase, cls).send_init_request(filename,
                                                   file_content, meta_vars)
        cls.request = cls.init_req.get_prepared_copy()

    @classmethod
    def tearDownClass(cls):
        super(AuthTestCase, cls).tearDownClass()

    def test_case(self):
        if 'HTTP_STATUS_CODE_2XX' in self.test_signals:
            description = (
                "This request did not fail with 404 (User not found),"
                " therefore it indicates that authentication with"
                " another user's token was successful.")
            self.register_issue(
                defect_type="alt_user_token",
                severity=syntribos.HIGH,
                confidence=syntribos.HIGH,
                description=description
            )

    @classmethod
    def get_test_cases(cls, filename, file_content):
        """Generates the test cases

        For this particular test, only a single test
        is created (in addition to the base case, that is)
        """
        alt_user_group = cfg.OptGroup(name="alt_user",
                                      title="Alt Keystone User Config")
        CONF.register_group(alt_user_group)
        CONF.register_opts(syntribos.config.list_user_opts(),
                           group=alt_user_group)

        alt_user_id = CONF.alt_user.user_id
        alt_user_username = CONF.alt_user.username
        if not alt_user_id or not alt_user_username:
            return

        yield cls
