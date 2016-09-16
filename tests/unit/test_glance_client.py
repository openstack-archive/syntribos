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

from syntribos.extensions.glance import client


class _Image_meta_data():
    def __init__(self):
        self.id = 1234


class _Images():

    def create(self, name):
        return _Image_meta_data()

    def list(data):
        return []


class _FakeGlance():
    """Fake glance client object."""
    images = _Images()


def fake_get_client():
    return _FakeGlance()


class TestGlanceClientCreateResources(testtools.TestCase):
    """Tests all getter methods for glance extension client."""

    @mock.patch("syntribos.extensions.glance.client._get_client",
                side_effect=fake_get_client)
    def test_get_image_id(self, get_client_fn):
        self.assertEqual(1234, client.get_image_id())
