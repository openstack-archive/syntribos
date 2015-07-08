import json
from xml.etree import ElementTree as ET
from cafe.engine.models.base import (
    AutoMarshallingModel, AutoMarshallingListModel)


class V2_0Constants(object):
    XML_NS = 'http://docs.openstack.org/identity/api/v2.0'
    XML_NS_OPENSTACK_COMMON = 'http://docs.openstack.org/common/api/v1.0'
    XML_NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
    XML_NS_OS_KSADM = \
        'http://docs.openstack.org/identity/api/ext/OS-KSADM/v1.0'
    XML_NS_OS_KSEC2 = \
        'http://docs.openstack.org/identity/api/ext/OS-KSEC2/v1.0'
    XML_NS_RAX_KSQA = \
        'http://docs.rackspace.com/identity/api/ext/RAX-KSQA/v1.0'
    XML_NS_RAX_KSKEY = \
        'http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0'
    XML_NS_RAX_AUTH = \
        'http://docs.rackspace.com/identity/api/ext/RAX-AUTH/v1.0'
    XML_NS_RAX_KSGRP = \
        'http://docs.rackspace.com/identity/api/ext/RAX-KSGRP/v1.0'
    XML_NS_ATOM = 'http://www.w3.org/2005/Atom'


class BaseIdentityModel(AutoMarshallingModel):
    _namespaces = V2_0Constants

    def __init__(self, kwargs):
        super(BaseIdentityModel, self).__init__()
        for var in kwargs:
            if var != "self" and not var.startswith("_"):
                setattr(self, var, kwargs.get(var))

    @classmethod
    def _remove_xml_namespaces(cls, element):
        for key, value in cls._namespaces.__dict__.items():
            if key.startswith("__"):
                continue
            element = cls._remove_namespace(element, value)
        return element

    @classmethod
    def _remove_namespace(cls, element, XML_NS):
        return cls._remove_xml_etree_namespace(element, XML_NS)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        return cls._xml_ele_to_obj(
            cls._remove_xml_namespaces(element))

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        return ET.tostring(element)

    @staticmethod
    def _find(element, tag):
        if element is None:
            return ET.Element(None)
        new_element = element.find(tag)
        if new_element is None:
            return ET.Element(None)
        return new_element


class BaseIdentityListModel(AutoMarshallingListModel, BaseIdentityModel):
    pass


class EmptyModel(object):
    def _obj_to_dict(self):
        return None

    def _obj_to_xml_ele(self):
        return ET.Element(None)


class AuthResponse(BaseIdentityModel):
    def __init__(
            self, token=None, service_catalog=None, user=None):
        super(AuthResponse, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            token=AuthResponseToken._dict_to_obj(data.get("token")),
            user=User._dict_to_obj(data.get("user")),
            service_catalog=ServiceCatalog._dict_to_obj(
                data.get("serviceCatalog")))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._dict_to_obj(data.get("access"))

    @classmethod
    def _xml_ele_to_obj(cls, element):
        service_catalog = ServiceCatalog._xml_ele_to_obj(
            cls._find(element, "serviceCatalog"))
        return cls(
            token=AuthResponseToken._xml_ele_to_obj(
                cls._find(element, "token")),
            user=User._xml_ele_to_obj(cls._find(element, "user")),
            service_catalog=service_catalog)

    def get_service(self, name):
        for service in self.service_catalog:
            if service.name == name:
                return service
        return None


class Tenant(BaseIdentityModel):
    def __init__(self, name=None, id_=None):
        super(Tenant, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element is None:
            return cls()
        return cls(
            name=element.attrib.get("name"), id_=element.attrib.get("id"))

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return cls()
        return cls(
            name=data.get("name"), id_=data.get("id"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data = json.loads(serialized_str)
        return cls._dict_to_obj(data.get("tenant"))


class AuthResponseToken(BaseIdentityModel):
    def __init__(
            self, id_=None, expires=None, tenant=None, authenticated_by=None):
        super(AuthResponseToken, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(id_=data.get("id"),
                   expires=data.get("expires"),
                   tenant=Tenant._dict_to_obj(data.get("tenant")),
                   authenticated_by=data.get("RAX-AUTH:authenticatedBy"))

    @classmethod
    def _xml_ele_to_obj(cls, element):
        authenticated_by = cls._find(element, "authenticatedBy")
        authenticated_by = authenticated_by.findtext("credential")
        return cls(
            id_=element.attrib.get("id"),
            expires=element.attrib.get("expires"),
            tenant=Tenant._xml_ele_to_obj(cls._find(element, "tenant")),
            authenticated_by=authenticated_by)


class ServiceCatalog(BaseIdentityListModel):

    @classmethod
    def _dict_to_obj(cls, data):
        return ServiceCatalog(
            [Service._dict_to_obj(service) for service in data])

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return ServiceCatalog(
            [Service._xml_ele_to_obj(service) for service in element])


class User(BaseIdentityModel):
    def __init__(
            self, id_=None, name=None, roles=None,
            rax_auth_default_region=None, rax_auth_federated=None):
        super(User, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return cls()
        region = data.get("RAX-AUTH:defaultRegion")
        if isinstance(region, list):
            region = region[0]
        return cls(
            id_=data.get("id"),
            name=data.get("name"),
            roles=Roles._dict_to_obj(data.get("roles")),
            rax_auth_default_region=region,
            rax_auth_federated=data.get("RAX-AUTH:federated"))

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return cls(
            id_=element.attrib.get("id"),
            name=element.attrib.get("name"),
            roles=Roles._xml_ele_to_obj(cls._find(element, "roles")),
            rax_auth_default_region=element.attrib.get("defaultRegion"),
            rax_auth_federated=element.attrib.get("federated"))


class Service(BaseIdentityModel):
    def __init__(self, endpoints=None, name=None, type_=None):
        super(Service, self).__init__(locals())

    def get_endpoint(self, region):
        """
        Returns the endpoint that matches the provided region,
        or None if such an endpoint is not found
        """
        for endpoint in self.endpoints:
            if getattr(endpoint, "region"):
                if str(endpoint.region).lower() == str(region).lower():
                    return endpoint
        return None

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            endpoints=Endpoints._dict_to_obj(data.get("endpoints")),
            name=data.get("name"), type_=data.get("type"))

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return cls(
            endpoints=Endpoints._xml_ele_to_obj(
                element.findall("endpoint")),
            name=element.attrib.get("name"),
            type_=element.attrib.get("type"))


class Endpoints(BaseIdentityListModel):
    @classmethod
    def _xml_ele_to_obj(cls, elements):
        if not elements:
            return cls()
        return cls([Endpoint._xml_ele_to_obj(endp) for endp in elements])

    @classmethod
    def _dict_to_obj(cls, data):
        if not data:
            return cls()
        return cls([Endpoint._dict_to_obj(endpoint) for endpoint in data])

    @classmethod
    def _json_to_obj(cls, string):
        data = json.loads(string)
        return cls._dict_to_obj(data.get("endpoints"))


class Endpoint(BaseIdentityModel):
    def __init__(self, id_=None, tenant_id=None, region=None, type_=None,
                 public_url=None, internal_url=None, admin_url=None,
                 version_id=None, version_info=None, version_list=None,
                 name=None):
        super(Endpoint, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        version = element.find("version")
        version_attrib = version.attrib if version is not None else {}
        return cls(
            id_=element.attrib.get("id"),
            tenant_id=element.attrib.get("tenantId"),
            region=element.attrib.get("region"),
            type_=element.attrib.get("type"),
            name=element.attrib.get("name"),
            public_url=element.attrib.get("publicURL"),
            internal_url=element.attrib.get("internalURL"),
            admin_url=element.attrib.get("adminURL"),
            version_id=version_attrib.get("id"),
            version_info=version_attrib.get("info"),
            version_list=version_attrib.get("list"))

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            id_=data.get("id"),
            tenant_id=data.get("tenantId"),
            region=data.get("region"),
            type_=data.get("type"),
            name=data.get("name"),
            public_url=data.get("publicURL"),
            internal_url=data.get("internalURL"),
            admin_url=data.get("adminURL"),
            version_id=data.get("versionId"),
            version_info=data.get("versionInfo"),
            version_list=data.get("versionList"))


class Roles(BaseIdentityListModel):

    @classmethod
    def _xml_ele_to_obj(cls, elements):
        return Roles(
            [Role._xml_ele_to_obj(element) for element in elements])

    @classmethod
    def _dict_to_obj(cls, data):
        return Roles([Role._dict_to_obj(obj) for obj in data])


class Role(BaseIdentityModel):
    def __init__(
            self, id_=None, name=None, description=None,
            rax_auth_propagate=None, tenant_id=None, service_id=None):
        super(Role, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element is None:
            return None
        return cls(
            id_=element.attrib.get("id"), name=element.attrib.get("name"),
            description=element.attrib.get("description"),
            rax_auth_propagate=element.attrib.get("propagate"),
            service_id=element.attrib.get("serviceId"),
            tenant_id=element.attrib.get("tenantId"))

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return None
        return cls(
            id_=data.get("id"), name=data.get("name"),
            description=data.get("description"),
            rax_auth_propagate=data.get("rax-auth:propagate"),
            service_id=data.get("serviceId"),
            tenant_id=data.get("tenantId"))


class Auth(BaseIdentityModel):
    xmlns = V2_0Constants.XML_NS

    def __init__(
            self, password_creds=None, rsa_creds=None, token_creds=None,
            api_key_creds=None, domain=None, tenant_name=None, tenant_id=None):
        password_creds = password_creds or EmptyModel()
        token_creds = token_creds or EmptyModel()
        api_key_creds = api_key_creds or EmptyModel()
        super(Auth, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {
            "tenantName": self.tenant_name,
            "tenantId": self.tenant_id,
            "passwordCredentials": self.password_creds._obj_to_dict(),
            "RAX-KSKEY:apiKeyCredentials": self.api_key_creds._obj_to_dict(),
            "token": self.token_creds._obj_to_dict()}
        return {'auth': self._remove_empty_values(attrs)}

    def _obj_to_xml_ele(self):
        element = ET.Element('auth')
        element = self._set_xml_etree_element(
            element, {"tenantName": self.tenant_name, "xmlns": self.xmlns,
                      "tenantId": self.tenant_id})
        element.append(self.password_creds._obj_to_xml_ele())
        element.append(self.rsa_creds._obj_to_xml_ele())
        element.append(self.token_creds._obj_to_xml_ele())
        element.append(self.api_key_creds._obj_to_xml_ele())
        element.append(self.domain._obj_to_xml_ele())
        return element


class PasswordCredentials(BaseIdentityModel):

    def __init__(self, username=None, password=None):
        super(PasswordCredentials, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {"username": self.username, "password": self.password}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element('passwordCredentials')
        attrs = {"username": self.username, "password": self.password}
        return self._set_xml_etree_element(element, attrs)


class Token(BaseIdentityModel):
    def __init__(self, id_=None):
        super(Token, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {"id": self.id_}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element('token')
        attrs = {"id": self.id_}
        return self._set_xml_etree_element(element, attrs)


class APIKeyCredentials(BaseIdentityModel):
    def __init__(self, username=None, api_key=None):
        xmlns = V2_0Constants.XML_NS_RAX_KSKEY
        super(APIKeyCredentials, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {"username": self.username, "apiKey": self.api_key}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element('apiKeyCredentials')
        attrs = {
            "username": self.username, "apiKey": self.api_key,
            "xmlns": self.xmlns}
        return self._set_xml_etree_element(element, attrs)


class RSACredentials(BaseIdentityModel):
    xmlns = V2_0Constants.XML_NS_RAX_AUTH

    def __init__(self, username=None, rsa_key=None):
        super(RSACredentials, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {"username": self.username, "tokenKey": self.rsa_key}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element('RAX-AUTH:rsaCredentials')
        attrs = {
            "username": self.username, "tokenKey": self.rsa_key,
            "xmlns:RAX-AUTH": self.xmlns}
        return self._set_xml_etree_element(element, attrs)


class Domain(BaseIdentityModel):
    xmlns = V2_0Constants.XML_NS_RAX_AUTH

    def __init__(self, name=None):
        super(Domain, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {"name": self.name}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element("RAX-AUTH:domain")
        attrs = {"name": self.name, "xmlns:RAX-AUTH": self.xmlns}
        return self._set_xml_etree_element(element, attrs)
