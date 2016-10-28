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

from syntribos.extensions.nova import client
from syntribos.utils.config_fixture import ConfFixture


class Content():
    id = 1234


class _Fakeserver():
    """Fake nova client object."""

    def create(*args, **kwargs):
        return Content()

    def list(data):
        return []


class _FakeHypervisor():
    def list(data):
        return [Content()]


class _FakeAggregates():
    def create(*args, **kwargs):
        return Content()

    def list(data):
        return []


class _FakeStorage():
    """Fake storage client."""
    servers = _Fakeserver()  # noqa
    hypervisors = _FakeHypervisor()  # noqa
    aggregates = _FakeAggregates()  # noqa


def fake_get_client():
    return _FakeStorage()


class TestNovaClientCreateResources(testtools.TestCase):
    """Tests all getter methods for nova extension client."""

    @mock.patch(
        "syntribos.extensions.nova.client._get_client",
        side_effect=fake_get_client)
    def test_get_hypervisor_id(self, get_client_fn):
        self.useFixture(ConfFixture())
        self.assertEqual(1234, client.get_hypervisor_id())

    @mock.patch(
        "syntribos.extensions.nova.client._get_client",
        side_effect=fake_get_client)
    def test_get_aggregate_id(self, get_client_fn):
        self.useFixture(ConfFixture())
        self.assertEqual(1234, client.get_aggregate_id())
