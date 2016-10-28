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

from syntribos.extensions.cinder import client


class Content():
    id = 1234


class _FakeVolume():
    """Fake cinder client object."""

    def create(*args, **kwargs):
        return Content()

    def list(data):
        return []


class _FakeVolumeType():
    def create(*args, **kwargs):
        return Content()

    def list(data):
        return []


class _FakeSnapshot():
    def create(*args, **kwargs):
        return Content()

    def list(data):
        return []


class _FakeStorage():
    """Fake storage client."""
    volumes = _FakeVolume()  # noqa
    volume_types = _FakeVolumeType()  # noqa
    volume_snapshots = _FakeSnapshot()  # noqa


def fake_get_client():
    return _FakeStorage()


class TestCinderClientCreateResources(testtools.TestCase):
    """Tests all getter methods for cinder extension client."""

    @mock.patch(
        "syntribos.extensions.cinder.client._get_client",
        side_effect=fake_get_client)
    def test_get_volume_id(self, get_client_fn):
        self.assertEqual(1234, client.get_volume_id())

    @mock.patch(
        "syntribos.extensions.cinder.client._get_client",
        side_effect=fake_get_client)
    def test_get_volume_type_id(self, get_client_fn):
        self.assertEqual(1234, client.get_volume_type_id())

    @mock.patch(
        "syntribos.extensions.cinder.client._get_client",
        side_effect=fake_get_client)
    def test_get_snapshot_id(self, get_client_fn):
        self.assertEqual(1234, client.get_snapshot_id())
