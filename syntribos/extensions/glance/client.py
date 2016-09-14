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
from glanceclient.v2.client import Client
from oslo_config import cfg

from syntribos.extensions.identity import client as id_client
from syntribos.utils.memoize import memoize

CONF = cfg.CONF


def _get_client():
    token = id_client.get_scoped_token_v3("user")
    return Client(endpoint=CONF.syntribos.endpoint, token=token)


def create_image(conn):
    image = conn.images.create(name="sample_image")
    return image.id


def list_image_ids(conn):
    return [image.id for image in conn.images.list()]


@memoize
def get_image_id():
    glance_client = _get_client()
    image_ids = list_image_ids(glance_client)
    if not image_ids:
        image_ids.append(create_image(glance_client))
    return image_ids[-1]
