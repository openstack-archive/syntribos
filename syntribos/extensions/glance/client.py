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
from glanceclient.v2 import client
from keystoneauth1 import identity
from keystoneauth1 import session
from oslo_config import cfg

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
    auth = identity.Password(auth_url=auth_url,
                             project_name=project_name,
                             project_domain_name=project_domain_name,
                             user_domain_name=user_domain_name,
                             project_domain_id=project_domain_id,
                             user_domain_id=user_domain_id,
                             username=username,
                             password=password)
    return client.Client(endpoint=CONF.syntribos.endpoint,
                         session=session.Session(auth=auth))


glance_client = create_connection(
    auth_url=CONF.user.endpoint,
    project_name=CONF.user.project_name,
    project_domain_name=CONF.user.domain_name,
    user_domain_name=CONF.user.domain_name,
    project_domain_id=CONF.user.domain_id,
    user_domain_id=CONF.user.domain_id,
    username=CONF.user.username,
    password=CONF.user.password)


def create_image(conn):
    image = conn.images.create(name="sample_image")
    return image.id


def list_image_ids(conn):
    return [image.id for image in conn.images.list()]


@memoize
def get_image_id():
    image_ids = list_image_ids(glance_client)
    if not image_ids:
        image_ids.append(create_image(glance_client))
    return image_ids[-1]
