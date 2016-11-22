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
import json
from xml.etree import ElementTree as ET

import syntribos.extensions.identity.models.base


class AuthResponse(
        syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self,
                 token=None,
                 service_catalog=None,
                 user=None,
                 metadata=None):
        super(AuthResponse, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(token=Token._dict_to_obj(data.get('token')),
                   metadata=Metadata._dict_to_obj(data.get('metadata')),
                   user=User._dict_to_obj(data.get('user')),
                   service_catalog=cls._build_list_model(
                       data, "serviceCatalog", Service))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get("access"))

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return cls(
            service_catalog=cls._build_list_model(
                cls._find(data, "serviceCatalog"), "service", Service),
            token_model=Token._xml_ele_to_obj(cls._find(data, "token")),
            user_model=User._xml_ele_to_obj(cls._find(data, "user")))

    def get_service(self, name):
        for service in self.service_catalog:
            if service.name == name:
                return service
        return None


class Metadata(syntribos.extensions.identity.models.base.BaseIdentityModel):
    @classmethod
    def _dict_to_obj(cls, data):
        return data

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return data.attrib


class Tenant(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self, enabled=None, description=None, name=None, id_=None):
        super(Tenant, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, data):
        description = data.findtext('description')
        return cls(name=data.attrib.get("name"),
                   id_=data.attrib.get("id"),
                   enabled=True
                   if data.attrib.get('enabled') == "true" else False,
                   description=description)

    @classmethod
    def _dict_to_obj(cls, data_dict):
        return cls(description=data_dict.get('description'),
                   enabled=data_dict.get('enabled'),
                   id_=data_dict.get('id'),
                   name=data_dict.get('name'))


class Token(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self, id_=None, issued_at=None, expires=None, tenant=None):
        super(Token, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return None
        return cls(id_=data.get('id'),
                   expires=data.get('expires'),
                   issued_at=data.get('issued_at'),
                   tenant=Tenant._dict_to_obj(data.get('tenant', {})))

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return cls(id_=data.attrib.get('id'),
                   expires=data.attrib.get('expires'),
                   issued_at=data.attrib.get('issued_at'),
                   tenant=Tenant._xml_ele_to_obj(data.find('tenant')))


class User(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self, id_=None, name=None, username=None, roles=None):
        super(User, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(id_=data.get('id'),
                   name=data.get('name'),
                   username=data.get('username'),
                   roles=cls._build_list_model(data, "roles", Role))

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return cls(id_=data.attrib.get('id'),
                   name=data.attrib.get('name'),
                   username=data.attrib.get('username'),
                   roles=cls._build_list_model(
                       cls._find(data, "roles"), "role", Role))


class Service(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self, endpoints=None, name=None, type_=None):
        super(Service, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            endpoints=cls._build_list_model(data, "endpoints", Endpoint),
            name=data.get("name"),
            type_=data.get("type"))

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return cls(endpoints=cls._build_list_model(data, "endpoint", Endpoint),
                   name=data.attrib.get("name"),
                   type_=data.attrib.get("type"))


class Endpoint(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self,
                 region=None,
                 id_=None,
                 public_url=None,
                 admin_url=None,
                 internal_url=None,
                 private_url=None,
                 version_id=None,
                 version_info=None,
                 version_list=None):
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


class Role(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self,
                 id_=None,
                 name=None,
                 description=None,
                 tenant_id=None,
                 service_id=None):
        super(Role, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element is None:
            return None
        return cls(id_=element.attrib.get("id"),
                   name=element.attrib.get("name"),
                   description=element.attrib.get("description"))

    @classmethod
    def _dict_to_obj(cls, data):
        if data is None:
            return None
        return cls(id_=data.get("id"),
                   name=data.get("name"),
                   description=data.get("description"))


class Auth(syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self, password_creds=None, tenant_id=None, tenant_name=None):
        super(Auth, self).__init__(locals())

    def _obj_to_dict(self):
        dic = {}
        dic["passwordCredentials"] = self._get_sub_model(self.password_creds)
        dic["tenantId"] = self.tenant_id
        dic["tenantName"] = self.tenant_name
        return {"auth": self._remove_empty_values(dic)}

    def _obj_to_xml_ele(self):
        ele = ET.Element("auth")
        ele.append(self._get_sub_model(self.password_creds, False))
        ele.attrib["tenantId"] = self.tenant_id
        return self._remove_empty_values(ele)


class PasswordCredentials(
        syntribos.extensions.identity.models.base.BaseIdentityModel):
    def __init__(self, username=None, password=None):
        super(PasswordCredentials, self).__init__(locals())

    def _obj_to_dict(self):
        dic = {"username": self.username, "password": self.password}
        return self._remove_empty_values(dic)

    def _obj_to_xml_ele(self):
        ele = ET.Element("passwordCredentials")
        ele.attrib["username"] = self.username
        ele.attrib["password"] = self.password
        return self._remove_empty_values(ele)
