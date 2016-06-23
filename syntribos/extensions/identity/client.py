# Copyright 2015 Rackspace
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
import logging

from requests import RequestException as RequestException

from syntribos.clients.http.base_http_client import HTTPClient
import syntribos.extensions.identity.config
import syntribos.extensions.identity.models.v2 as v2
import syntribos.extensions.identity.models.v3 as v3

logging.basicConfig(level=logging.CRITICAL)
LOG = logging.getLogger(__name__)


def authenticate_v2(
    url, username=None, password=None, tenant_name=None,
    tenant_id=None, domain=None, serialize_format="json",
        deserialize_format="json"):

    headers = {}
    kwargs = {}
    password_creds = None

    url = '{0}/v2.0/tokens'.format(url)
    headers["Content-Type"] = "application/{0}".format(serialize_format)
    headers["Accept"] = "application/{0}".format(deserialize_format)

    kwargs["tenant_name"] = tenant_name
    kwargs["tenant_id"] = tenant_id

    if password is not None:
        password_creds = v2.PasswordCredentials(
            username=username, password=password
        )

    request_entity = v2.Auth(
        tenant_name=tenant_name, tenant_id=tenant_id,
        password_creds=password_creds
    )

    data = request_entity.serialize(serialize_format)
    try:
        r, signals = HTTPClient().request(
            "POST", url, headers=headers,
            data=data).json()
    except RequestException as e:
        LOG.debug(e)
    else:
        if not r:
            raise Exception("Failed to authenticate")

        if r['access'] is None:
            raise Exception("Failed to parse Auth response Body")
        return r['access']


def authenticate_v2_config(user_config, userauth_config):
    return authenticate_v2(
        url=user_config.endpoint or userauth_config.endpoint,
        username=user_config.username,
        password=user_config.password,
        tenant_name=user_config.tenant_name,
        tenant_id=user_config.tenant_id,
        serialize_format=userauth_config.serialize_format,
        deserialize_format=userauth_config.deserialize_format)


def get_token_v2(user_section_name=None, endpoint_section_name=None):
    access_data = authenticate_v2_config(
        syntribos.extensions.identity.config.UserConfig(
            section_name=user_section_name),
        syntribos.extensions.identity.config.EndpointConfig(
            section_name=endpoint_section_name
        ))
    return access_data['token']['id']


def authenticate_v3(
    url, username=None, password=None, user_id=None, domain_id=None,
        domain_name=None, token=None, serialize_format="json",
        deserialize_format="json"):

    headers = {}
    kwargs = {}

    url = '{0}/v3/auth/tokens'.format(url)
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"

    if user_id is not None:
        domain = None
        username = None
    else:
        domain = v3.Domain(name=domain_name, id_=domain_id)
    password = v3.Password(user=v3.User(
        name=username, password=password, id_=user_id, domain=domain
    ))

    if token is not None:
        kwargs = {"token": v3.Token(id_=token), "methods": ["token"]}
    else:
        kwargs = {"password": password, "methods": ["password"]}
    request_entity = v3.Auth(identity=v3.Identity(**kwargs))
    data = request_entity.serialize(serialize_format)
    try:
        r, signals = HTTPClient().request(
            "POST", url, headers=headers,
            data=data)
    except RequestException as e:
        LOG.critical(e)
    else:
        if not r:
            raise Exception("Failed to authenticate")
        return r


def authenticate_v3_config(user_config, endpoint_config):
    return authenticate_v3(
        url=user_config.endpoint or endpoint_config.endpoint,
        username=user_config.username,
        password=user_config.password,
        user_id=user_config.user_id,
        domain_id=user_config.domain_id,
        domain_name=user_config.domain_name,
        token=user_config.token)


def get_token_v3(user_section_name=None, endpoint_section_name=None):
    r = authenticate_v3_config(
        syntribos.extensions.identity.config.UserConfig(
            section_name=user_section_name),
        syntribos.extensions.identity.config.EndpointConfig(
            section_name=endpoint_section_name))
    return r.headers["X-Subject-Token"]
