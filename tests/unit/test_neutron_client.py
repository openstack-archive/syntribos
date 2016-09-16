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

from syntribos.extensions.neutron import client


class _FakeNetwork():
    """Fake neutron client object."""

    def create_network(self, data):
        return {"id": 1234}

    def create_subnet(self, data):
        return {"id": 1234}

    def create_port(self, data):
        return {"id": 1234}

    def create_security_group(self, data):
        return {"id": 1234}

    def create_router(self, data):
        return {"id": 1234}

    def list_networks(data):
        return {"networks": []}

    def list_subnets(data):
        return {"subnets": []}

    def list_ports(data):
        return {"ports": []}

    def list_security_groups(data):
        return {"security_groups": []}

    def list_routers(data):
        return {"routers": []}


def fake_get_client():
    return _FakeNetwork()


class TestNeutronClientCreateResources(testtools.TestCase):
    """Tests all getter methods for neutron extension client."""

    @mock.patch("syntribos.extensions.neutron.client._get_client",
                side_effect=fake_get_client)
    def test_get_network_id(self, get_client_fn):
        self.assertEqual(1234, client.get_network_id())

    @mock.patch("syntribos.extensions.neutron.client._get_client",
                side_effect=fake_get_client)
    def test_get_subnet_id(self, get_client_fn):
        self.assertEqual(1234, client.get_subnet_id())

    @mock.patch("syntribos.extensions.neutron.client._get_client",
                side_effect=fake_get_client)
    def test_get_port_id(self, get_client_fn):
        self.assertEqual(1234, client.get_port_id())

    @mock.patch("syntribos.extensions.neutron.client._get_client",
                side_effect=fake_get_client)
    def test_get_router_id(self, get_client_fn):
        self.assertEqual(1234, client.get_router_id())

    @mock.patch("syntribos.extensions.neutron.client._get_client",
                side_effect=fake_get_client)
    def test_get_sec_group_id(self, get_client_fn):
        self.assertEqual(1234, client.get_sec_group_id())
