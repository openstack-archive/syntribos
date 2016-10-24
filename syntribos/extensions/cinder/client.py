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
import random
import string

from cinderclient.v2.client import Client
from keystoneauth1 import identity
from keystoneauth1 import session
from oslo_config import cfg

from syntribos.utils.memoize import memoize

CONF = cfg.CONF


def _get_client():
    """Returns a v2 cinder client object."""
    auth_url = CONF.user.endpoint
    if auth_url.endswith("/v3/"):
        auth_url = auth_url[-1]
    elif auth_url.endswith("/v3"):
        pass
    else:
        auth_url = "{}/v3".format(auth_url)
    auth = identity.v3.Password(auth_url=auth_url,
                                project_name=CONF.user.project_name,
                                project_domain_name=CONF.user.domain_name,
                                user_domain_name=CONF.user.domain_name,
                                username=CONF.user.username,
                                password=CONF.user.password)
    return Client("2", session=session.Session(auth=auth))


def create_volume(conn):
    volume = conn.volumes.create(name="sample_vol", size=1)
    return volume.id


def list_volume_ids(conn):
    return [volume.id for volume in conn.volumes.list()]


def create_volume_type(conn):
    vname = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
    vtype = conn.volume_types.create(vname, "A new type of volume",
                                     is_public=True)
    return vtype.id


def list_volume_type_ids(conn):
    return [volume.id for volume in conn.volume_types.list()]


def create_snapshot(conn):
    volume_id = get_volume_id()
    snap_name = "".join(
        random.choice(string.ascii_lowercase) for _ in range(10))
    snapshot = conn.volume_snapshots.create(
        volume_id, name=snap_name, description="Test snapshot")
    return snapshot.id


def list_snapshot_ids(conn):
    return [snapshot.id for snapshot in conn.volume_snapshots.list()]


@memoize
def get_volume_id(create=False):
    cinder_client = _get_client()
    volume_ids = list_volume_ids(cinder_client)
    if create or not volume_ids:
        volume_ids.append(create_volume(cinder_client))
    return volume_ids[-1]


@memoize
def get_volume_type_id(create=False):
    cinder_client = _get_client()
    vtype_ids = list_volume_type_ids(cinder_client)
    if create or not vtype_ids:
        vtype_ids.append(create_volume_type(cinder_client))
    return vtype_ids[-1]


@memoize
def get_snapshot_id(create=False):
    cinder_client = _get_client()
    snapshot_ids = list_snapshot_ids(cinder_client)
    if create or not snapshot_ids:
        snapshot_ids.append(create_snapshot(cinder_client))
    return snapshot_ids[-1]
