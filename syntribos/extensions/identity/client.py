"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from cafe.engine.http.client import AutoMarshallingHTTPClient

from syntribos.extensions.identity.models import v2, v3
from syntribos.extensions.identity.config import (
    EndpointConfig, UserConfig)


def authenticate_v2(
    url, username=None, password=None, tenant_name=None,
    tenant_id=None, token=None, domain=None, serialize_format="json",
        deserialize_format="json"):
    url = '{0}/v2.0/tokens'.format(url)
    client = AutoMarshallingHTTPClient(serialize_format, deserialize_format)
    client.default_headers["Content-Type"] = "application/{0}".format(
        serialize_format)
    client.default_headers["Accept"] = "application/{0}".format(
        deserialize_format)

    kwargs = {}
    kwargs["tenant_name"] = tenant_name
    kwargs["tenant_id"] = tenant_id

    if password is not None:
        password_creds = v2.PasswordCredentials(
            username=username, password=password)

    request_entity = v2.Auth(
        tenant_name=tenant_name, tenant_id=tenant_id,
        password_creds=password_creds)

    r = client.request(
        "POST", url, request_entity=request_entity,
        response_entity_type=v2.AuthResponse)

    if not r.ok:
        raise Exception("Failed to authenticate")

    if r.entity is None:
        raise Exception("Failed to parse Auth response Body")
    return r


def authenticate_v2_config(user_config, userauth_config):
    return authenticate_v2(
        url=user_config.endpoint or userauth_config.endpoint,
        username=user_config.username,
        password=user_config.password,
        tenant_name=user_config.tenant_name,
        tenant_id=user_config.tenant_id,
        token=user_config.token,
        serialize_format=userauth_config.serialize_format,
        deserialize_format=userauth_config.deserialize_format)


def get_token_v2(user_section_name=None, endpoint_section_name=None):
    access_data = authenticate_v2_config(
        UserConfig(section_name=user_section_name),
        EndpointConfig(section_name=endpoint_section_name)).entity
    return access_data.token.id_


def authenticate_v3(
    url, username=None, password=None, user_id=None, domain_id=None,
        domain_name=None, token=None):

    url = '{0}/v3/auth/tokens'.format(url)
    client = AutoMarshallingHTTPClient("json", "json")
    client.default_headers["Content-Type"] = "application/json"
    client.default_headers["Accept"] = "application/json"

    if user_id is not None:
        domain = None
        username = None
    else:
        domain = v3.Domain(name=domain_name, id_=domain_id)
    password = v3.Password(user=v3.User(
        name=username, password=password, id_=user_id, domain=domain))

    if token is not None:
        kwargs = {"token": v3.Token(id_=token), "methods": ["token"]}
    else:
        kwargs = {"password": password, "methods": ["password"]}
    request_entity = v3.Auth(identity=v3.Identity(**kwargs))

    r = client.request(
        "POST", url, request_entity=request_entity)

    if not r.ok:
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
        UserConfig(section_name=user_section_name),
        EndpointConfig(section_name=endpoint_section_name))
    return r.headers.get("X-Subject-Token")
