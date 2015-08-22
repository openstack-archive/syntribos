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
import six
from xml.etree import ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel


class Namespaces(object):
    XMLNS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    XMLNS = "http://docs.openstack.org/identity/api/v2.0"
    XMLNS_KSKEY = "http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0"
    XMLNS_RAX_AUTH = "http://docs.rackspace.com/identity/api/ext/RAX-AUTH/v1.0"


class BaseIdentityModel(AutoMarshallingModel):
    _namespaces = Namespaces

    def __init__(self, kwargs):
        super(BaseIdentityModel, self).__init__()
        for k, v in kwargs.items():
            if k != "self" and not k.startswith("_"):
                setattr(self, k, v)

    @classmethod
    def _remove_xml_namespaces(cls, element):
        for key, value in vars(cls._namespaces).items():
            if key.startswith("__"):
                continue
            element = cls._remove_xml_etree_namespace(element, value)
        return element

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str, strict=False)
        return cls._dict_to_obj(data_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str, encoding="iso-8859-2"):
        parser = ET.XMLParser(encoding=encoding)
        element = ET.fromstring(serialized_str, parser=parser)
        return cls._xml_ele_to_obj(cls._remove_xml_namespaces(element))

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        element.attrib["xmlns"] = self._namespaces.XMLNS
        return ET.tostring(element)

    @staticmethod
    def _find(element, tag):
        if element is None:
            return ET.Element(None)
        new_element = element.find(tag)
        if new_element is None:
            return ET.Element(None)
        return new_element

    @staticmethod
    def _build_list_model(data, field_name, model):
        if data is None:
            return []
        if isinstance(data, dict):
            if data.get(field_name) is None:
                return []
            return [model._dict_to_obj(tmp) for tmp in data.get(field_name)]
        return [model._xml_ele_to_obj(tmp) for tmp in data.findall(field_name)]

    @staticmethod
    def _build_list(items, element=None):
        if element is None:
            if items is None:
                return []
            return [item._obj_to_dict() for item in items]
        else:
            if items is None:
                return element
            for item in items:
                element.append(item._obj_to_xml_ele())
            return element

    @staticmethod
    def _create_text_element(name, text):
        element = ET.Element(name)
        if text is True or text is False:
            element.text = str(text).lower()
        elif text is None:
            return ET.Element(None)
        else:
            element.text = str(text)
        return element

    def __ne__(self, obj):
        return not self.__eq__(obj)

    @classmethod
    def _remove_empty_values(cls, data):
        """Returns a new dictionary based on 'dictionary', minus any keys with
        values that evaluate to False
        """
        if isinstance(data, dict):
            return dict(
                (k, v) for k, v in six.iteritems(data) if v not in (
                    [], {}, None))
        elif isinstance(data, ET.Element):
            if data.attrib:
                data.attrib = cls._remove_empty_values(data.attrib)
            data._children = [
                c for c in data._children if c.tag is not None and (
                    c.attrib or c.text is not None or c._children)]
            return data

    @staticmethod
    def _get_sub_model(model, json=True):
        if json:
            if model is not None:
                return model._obj_to_dict()
            else:
                return None
        else:
            if model is not None:
                return model._obj_to_xml_ele()
            else:
                return ET.Element(None)
