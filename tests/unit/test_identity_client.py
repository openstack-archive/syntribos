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
import mock
import testtools

from syntribos.clients.http.client import SynHTTPClient
from syntribos.extensions.identity import client
from syntribos.utils.config_fixture import ConfFixture


class TestIdentityClient(testtools.TestCase):
    """Tests get_token v2 and v3 methods of the identity client."""

    class _FakeRequest():
        """Fake request class used to mock request method of SynHTTPClient."""
        class _FakeResponse():
            def __init__(self):
                self.content = {"access": {"token": {"id": 1234}}}
                self.headers = {"X-Subject-Token": 12345}

            def json(self):
                return self.content

            def text(self):
                return self.content

        def fake_request(self, method="POST", url="http://localhost",
                         headers="headers", data="data", sanitize=True):
            return(self._FakeResponse(), "FAKE_SIGNAL")

    @mock.patch.object(SynHTTPClient, 'request',
                       _FakeRequest().fake_request)
    def test_get_token_v2(self):
        self.useFixture(ConfFixture())
        token = client.get_token_v2()
        self.assertEqual(1234, token)

    @mock.patch.object(SynHTTPClient, 'request',
                       _FakeRequest().fake_request)
    def test_get_token_v3(self):
        self.useFixture(ConfFixture())
        token = client.get_token_v3()
        self.assertEqual(12345, token)
