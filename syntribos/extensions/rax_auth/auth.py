from cafe.engine.behaviors import BaseBehavior
from cafe.engine.http.client import AutoMarshallingHTTPClient

from syntribos.extensions.rax_auth.models import auth_models
from syntribos.extensions.rax_auth.auth_config import (
    UserAuthConfig, UserConfig)


class TokensBehavior(BaseBehavior):
    @classmethod
    def get_access_data_config(cls, user_config, userauth_config):
        return cls.get_access_data(
            url=user_config.endpoint or userauth_config.endpoint,
            username=user_config.username,
            password=user_config.password,
            tenant_name=user_config.tenant_name,
            tenant_id=user_config.tenant_id,
            token=user_config.token,
            api_key=user_config.api_key,
            serialize_format=userauth_config.serialize_format,
            deserialize_format=userauth_config.deserialize_format)

    @classmethod
    def get_access_data(cls, *args, **kwargs):
        return cls.authenticate(*args, **kwargs).entity

    @classmethod
    def authenticate(
            cls, url, username=None, password=None, tenant_name=None,
            tenant_id=None, token=None, api_key=None, rsa_key=None,
            domain=None, serialize_format="json", deserialize_format="json"):
        url = '{0}/tokens'.format(url)
        client = AutoMarshallingHTTPClient(
            serialize_format, deserialize_format)

        client.default_headers["Content-Type"] = "application/{0}".format(
            serialize_format)
        client.default_headers["Accept"] = "application/{0}".format(
            deserialize_format)

        kwargs = {}
        kwargs["tenant_name"] = tenant_name
        kwargs["tenant_id"] = tenant_id

        if password is not None:
            kwargs["password_creds"] = auth_models.PasswordCredentials(
                username=username, password=password)

        if token is not None:
            kwargs["token_creds"] = auth_models.Token(id_=token)

        if api_key is not None:
            kwargs["api_key_creds"] = auth_models.APIKeyCredentials(
                username=username, api_key=api_key)

        request_entity = auth_models.Auth(**kwargs)

        r = client.request(
            "POST", url, request_entity=request_entity,
            response_entity_type=auth_models.AuthResponse)
        if not r.ok:
            raise Exception("Failed to authenticate")

        r.entity = auth_models.AuthResponse.deserialize(
            r.content, deserialize_format)
        if r.entity is None:
            raise Exception("Failed to parse Auth response Body")
        return r


def get_access(section_name):
    return TokensBehavior.get_access_data_config(
        UserConfig(section_name=section_name), UserAuthConfig())
