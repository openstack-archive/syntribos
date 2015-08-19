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
            self, token=None, service_catalog=None, user=None, metadata=None):
            super(AuthResponse, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            token=AuthResponseToken._dict_to_obj(data.get('token')),
            metadata=Metadata._dict_to_obj(data.get('metadata')),
            user=User._dict_to_obj(data.get('user')),
            service_catalog=ServiceCatalog._dict_to_obj(
                data.get('serviceCatalog')))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get("access"))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            token=AuthResponseToken._xml_ele_to_obj(ele.find('token')),
            metadata=Metadata._xml_ele_to_obj(ele.find('metadata')),
            user=User._xml_ele_to_obj(ele.find('user')),
            service_catalog=ServiceCatalog._xml_ele_to_obj(
                ele.find('serviceCatalog')))

    def get_service(self, name):
        for service in self.service_catalog:
            if service.name == name:
                return service
        return None


class Metadata(BaseIdentityModel):

    @classmethod
    def _dict_to_obj(cls, data):
        return data

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return ele.attrib


class Tenant(BaseIdentityModel):
    def __init__(self, enabled=None, description=None, name=None, id_=None):
        super(Tenant, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element.tag.lower() != "tenant":
            raise Exception("wrong element")
        enabled = True if element.attrib.get('enabled') == "true" else False
        description = element.find('description')
        description = "" if description is None else description.text
        return cls(enabled=enabled,
                   description=description,
                   name=element.attrib.get('name'),
                   id_=element.attrib.get('id'))

    @classmethod
    def _dict_to_obj(cls, data_dict):
        return cls(description=data_dict.get('description'),
                   enabled=data_dict.get('enabled'),
                   id_=data_dict.get('id'),
                   name=data_dict.get('name'))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get('tenant'))


class AuthResponseToken(BaseIdentityModel):
    def __init__(self, id_=None, issued_at=None, expires=None, tenant=None):
        super(AuthResponseToken, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(id_=data.get('id'),
                   expires=data.get('expires'),
                   issued_at=data.get('issued_at'),
                   tenant=Tenant._dict_to_obj(data.get('tenant')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(id_=ele.attrib.get('id'),
                   expires=ele.attrib.get('expires'),
                   issued_at=ele.attrib.get('issued_at'),
                   tenant=Tenant._xml_ele_to_obj(ele.find('tenant')))


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
            self, id_=None, name=None, username=None, roles=None,
            roles_links=None):
        super(User, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            id_=data.get('id'),
            name=data.get('name'),
            username=data.get('username'),
            roles=Roles._dict_to_obj(data.get('roles')),
            roles_links=RolesLinks._dict_to_obj(data.get('roles_links')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            id_=ele.attrib.get('id'),
            name=ele.attrib.get('name'),
            username=ele.attrib.get('username'),
            roles=Roles._xml_ele_to_obj(ele.findall('role')),
            roles_links=RolesLinks._xml_ele_to_obj(ele.find('roles_links')))


class Service(BaseIdentityModel):
    def __init__(
            self, endpoints=None, endpoints_links=None, name=None, type_=None):
        super(Service, self).__init__(locals())

    def get_endpoint(self, region):
        """
        Returns the endpoint that matches the provided region,
        or None if such an endpoint is not found
        """
        for endpoint in self.endpoints:
            if getattr(endpoint, 'region'):
                if str(endpoint.region).lower() == str(region).lower():
                    return endpoint
        return None

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            endpoints=Endpoints._dict_to_obj(data.get('endpoints')),
            endpoints_links=EndpointsLinks._dict_to_obj(
                data.get('endpoints_links')),
            name=data.get('name'), type_=data.get('type'))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            endpoints=Endpoints._xml_ele_to_obj(ele.findall("endpoint")),
            endpoints_links=EndpointsLinks._xml_ele_to_obj(
                ele.find('endpoints_links')),
            name=ele.attrib.get('name'),
            type_=ele.attrib.get('type'))


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


class EndpointsLinks(BaseIdentityListModel):
    # always returns an empty list since no documentation on endpoint links
    @classmethod
    def _dict_to_obj(cls, data):
        return EndpointsLinks()

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return EndpointsLinks()


class Endpoint(BaseIdentityModel):
    def __init__(
            self, region=None, id_=None, public_url=None, admin_url=None,
            internal_url=None, private_url=None, version_id=None,
            version_info=None, version_list=None):
        super(Endpoint, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(region=data.get('region'),
                   id_=data.get('Id'),
                   public_url=data.get('publicURL'),
                   private_url=data.get('privateURL'),
                   admin_url=data.get('adminURL'),
                   internal_url=data.get('internalURL'),
                   version_id=data.get('versionId'),
                   version_info=data.get('versionInfo'),
                   version_list=data.get('versionList'))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(region=ele.attrib.get('region'),
                   id_=ele.attrib.get('Id'),
                   public_url=ele.attrib.get('publicURL'),
                   private_url=ele.attrib.get('privateURL'),
                   admin_url=ele.attrib.get('adminURL'),
                   internal_url=ele.attrib.get('internalURL'),
                   version_id=ele.attrib.get('versionId'),
                   version_info=ele.attrib.get('versionInfo'),
                   version_list=ele.attrib.get('versionList'))


class Roles(BaseIdentityListModel):

    @classmethod
    def _xml_ele_to_obj(cls, elements):
        return Roles(
            [Role._xml_ele_to_obj(element) for element in elements])

    @classmethod
    def _dict_to_obj(cls, data):
        return Roles([Role._dict_to_obj(obj) for obj in data])


class RolesLinks(BaseIdentityListModel):
    # always returns an empty list since no documentation on role links
    @classmethod
    def _dict_to_obj(cls, data):
        return RolesLinks()

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return RolesLinks()


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
            id_=element.attrib.get("id"),
            name=element.attrib.get("name"),
            description=element.attrib.get("description"))

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return None
        return cls(
            id_=data.get("id"),
            name=data.get("name"),
            description=data.get("description"))


class Auth(BaseIdentityModel):

    def __init__(
            self, username=None, password=None, tenant_name=None,
            tenant_id=None, token=None):
        super(Auth, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {
            "tenantName": self.tenant_name,
            "tenantId": self.tenant_id,
            "passwordCredentials": self.password_credentials._obj_to_dict()}
        return {'auth': self._remove_empty_values(attrs)}

    def _obj_to_xml_ele(self):
        element = ET.Element('auth')
        element = self._set_xml_etree_element(
            element, {"tenantName": self.tenant_name,
                      "tenantId": self.tenant_id})
        element.append(self.password_credentials._obj_to_xml_ele())
        return element


class PasswordCredentials(BaseIdentityModel):

    def __init__(self, username=None, password=None):
        super(PasswordCredentials, self).__init__(locals())

    def _obj_to_dict(self):
        attrs = {
            "username": self.username,
            "password": self.password}
        return self._remove_empty_values(attrs)

    def _obj_to_xml_ele(self):
        element = ET.Element('passwordCredentials')
        attrs = {
            "username": self.username,
            "password": self.password}
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
