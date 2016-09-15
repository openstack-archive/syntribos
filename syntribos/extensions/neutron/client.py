# Copyright 2016 Intel
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
from neutronclient.v2_0.client import Client
from oslo_config import cfg

from syntribos.extensions.identity import client as id_client
from syntribos.utils.memoize import memoize

CONF = cfg.CONF


def _get_client():
    token = id_client.get_scoped_token_v3("user")
    return Client(endpoint=CONF.syntribos.endpoint, token=token)


def create_network(conn):
    data = {"name": "sample_network",
            "admin_state_up": True}
    return conn.create_network({"network": data})


def list_network_ids(conn):
    return [network["id"] for network in conn.list_networks()["networks"]]


def create_subnet(conn, network_id):
    data = {"name": "sample_subnet",
            "network_id": network_id,
            "ip_version": 4,
            "cidr": "11.0.3.0/24"}
    return conn.create_subnet({"subnet": data})


def list_subnet_ids(conn):
    subnet_ids = [subnet["id"] for subnet in conn.list_subnets()["subnets"]]
    return subnet_ids


def create_port(conn, network_id):
    data = {"network_id": network_id,
            "name": "sample_port",
            "admin_state_up": True}
    return conn.create_port({"port": data})


def list_port_ids(conn):
    port_ids = [port["id"] for port in conn.list_ports()["ports"]]
    return port_ids


def create_security_group(conn):
    data = {"name": "new_servers",
            "description": "security group for servers"}
    return conn.create_security_group({"security_group": data})


def list_security_group_ids(conn):
    sec_gp_ids = [sg["id"] for sg in conn.list_security_groups(
    )["security_groups"]]
    return sec_gp_ids


def create_router(conn, network_id, subnet_id):
    # The network_id should be of an external network
    data = {
        "name": "router1",
        "external_gateway_info": {
            "network_id": network_id,
            "enable_snat": True,
            "external_fixed_ips": [
                {
                    "ip_address": "172.24.4.6",
                    "subnet_id": subnet_id
                }
            ]
        },
        "admin_state_up": True
    }
    return conn.create_router({"router": data})


def list_router_ids(conn):
    router_ids = [router["id"] for router in conn.list_routers()["routers"]]
    return router_ids


@memoize
def get_port_id():
    neutron_client = _get_client()
    port_ids = list_port_ids(neutron_client)
    if not port_ids:
        network_id = get_network_id()
        port_ids.append(create_port(neutron_client, network_id)["id"])
    return port_ids[-1]


@memoize
def get_network_id():
    neutron_client = _get_client()
    network_ids = list_network_ids(neutron_client)
    if len(network_ids) < 3:
        network_ids.append(create_network(neutron_client)["id"])
    return network_ids[-1]


@memoize
def get_subnet_id():
    neutron_client = _get_client()
    subnet_ids = list_subnet_ids(neutron_client)
    if not subnet_ids:
        network_id = get_network_id()
        subnet_ids.append(create_subnet(neutron_client, network_id)["id"])
    return subnet_ids[-1]


@memoize
def get_sec_group_id():
    neutron_client = _get_client()
    sg_ids = list_security_group_ids(neutron_client)
    if not sg_ids:
        sg_ids.append(create_security_group(neutron_client)["id"])
    return sg_ids[-1]


@memoize
def get_router_id():
    neutron_client = _get_client()
    router_ids = list_router_ids(neutron_client)
    if not router_ids:
        network_id = get_network_id()
        subnet_id = get_subnet_id()
        router_ids.append(
            create_router(neutron_client, network_id, subnet_id)["id"])
    return router_ids[-1]
