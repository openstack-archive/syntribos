# Copyright 2016 Rackspace
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
from glanceclient.v2.client import Client as GC
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client
from oslo_config import cfg
import six.moves.urllib.parse as urlparse

from syntribos.extensions.identity import client as id_client
from syntribos.utils.memoize import memoize

CONF = cfg.CONF


def create_connection(auth_url=None,
                      project_name=None,
                      project_domain_name="default",
                      user_domain_name="default",
                      project_domain_id="default",
                      user_domain_id="default",
                      username=None,
                      password=None):
    """Method return a glance client."""

    if auth_url.endswith("/v3/"):
        auth_url = auth_url[-1]
    elif auth_url.endswith("/v3"):
        pass
    else:
        auth_url = "{}/v3".format(auth_url)
    auth = v3.Password(auth_url=auth_url,
                       project_name=project_name,
                       project_domain_name=project_domain_name,
                       user_domain_name=user_domain_name,
                       project_domain_id=project_domain_id,
                       user_domain_id=user_domain_id,
                       username=username,
                       password=password)
    return Client("2", auth_url=CONF.user.endpoint,
                  session=session.Session(auth=auth))


def _get_client():
    # Required to use keystone client in order for nova client to properly
    # discover service URL
    nova_client = create_connection(
        auth_url=CONF.user.endpoint,
        project_name=CONF.user.project_name,
        project_domain_name=CONF.user.domain_name,
        user_domain_name=CONF.user.domain_name,
        project_domain_id=CONF.user.domain_id,
        user_domain_id=CONF.user.domain_id,
        username=CONF.user.username,
        password=CONF.user.password)

    return nova_client


def list_hypervisor_ids(conn):
    return [hypervisor.id for hypervisor in conn.hypervisors.list()]


def list_server_ids(conn):
    return [server.id for server in conn.servers.list()]


def create_server(conn):
    token = id_client.get_scoped_token_v3("user")
    _url = urlparse.urlunparse(CONF.syntribos.endpoint)
    endpoint = urlparse.urlunparse(
        (_url.scheme,
         _url.hostname + ":9292",
         _url.path,
         _url.params,
         _url.query,
         _url.fragment))
    _gc = GC(endpoint=endpoint, token=token)
    image = _gc.images.get(get_image_id())
    flavor = conn.flavors.get(get_flavor_id())
    server = conn.servers.create(
        name="test", flavor=flavor, image=image)

    return server.id


def list_flavor_ids(conn):
    return [flavor.id for flavor in conn.flavors.list()]


def create_flavor(conn):
    flavor = conn.flavors.create(
        name="test", ram=1, vcpus=1, disk=1)
    return flavor.id


def list_aggregate_ids(conn):
    return [aggregate.id for aggregate in conn.aggregates.list()]


def create_aggregate(conn):
    aggregate = conn.aggregates.create(
        name="test", availability_zone="test_zone")
    return aggregate.id


@memoize
def get_hypervisor_id():
    nova_client = _get_client()
    hypervisor_ids = list_hypervisor_ids(nova_client)
    return hypervisor_ids[-1]


@memoize
def get_image_id():
    token = id_client.get_scoped_token_v3("user")
    _url = urlparse.urlparse(CONF.syntribos.endpoint)
    endpoint = urlparse.urlunparse(
        (_url.scheme,
         _url.hostname + ":9292",
         _url.path,
         _url.params,
         _url.query,
         _url.fragment))
    _gc = GC(endpoint=endpoint, token=token)
    image_ids = [image.id for image in _gc.images.list()]
    if not image_ids:
        image_ids.append(_gc.images.create(name="test"))

    return image_ids[-1]


@memoize
def get_server_id():
    nova_client = _get_client()
    server_ids = list_server_ids(nova_client)
    if not server_ids:
        server_ids.append(create_server(nova_client))
    return server_ids[-1]


@memoize
def get_flavor_id():
    nova_client = _get_client()
    flavor_ids = list_flavor_ids(nova_client)
    if not flavor_ids:
        flavor_ids.append(create_flavor(nova_client))
    return flavor_ids[-1]


@memoize
def get_aggregate_id():
    nova_client = _get_client()
    aggregate_ids = list_aggregate_ids(nova_client)
    if not aggregate_ids:
        aggregate_ids.append(create_aggregate(nova_client))
    return aggregate_ids[-1]
