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
import logging
import xml.etree.ElementTree as ET


class Namespaces(object):
    XMLNS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    XMLNS = "http://docs.openstack.org/identity/api/v2.0"
    XMLNS_KSKEY = "http://docs.rackspace.com/identity/api/ext/RAX-KSKEY/v1.0"
    XMLNS_RAX_AUTH = "http://docs.rackspace.com/identity/api/ext/RAX-AUTH/v1.0"


class BaseIdentityModel(object):
    _namespaces = Namespaces

    def __init__(self, kwargs):
        super(BaseIdentityModel, self).__init__()
        self._log = logging.getLogger(__name__)
        for k, v in kwargs.items():
            if k != "self" and not k.startswith("_"):
                setattr(self, k, v)

    def serialize(self, format_type):
        try:
            serialize_method = '_obj_to_{0}'.format(format_type)
            return getattr(self, serialize_method)()
        except Exception as serialization_exception:
            self._log.error(
                'Error occured during serialization of a data model into'
                'the "%s: \n%s" format',
                format_type, serialization_exception)
            self._log.exception(serialization_exception)

    @classmethod
    def deserialize(cls, serialized_str, format_type):
        if serialized_str and len(serialized_str) > 0:
            try:
                deserialize_method = '_{0}_to_obj'.format(format_type)
                return getattr(cls, deserialize_method)(serialized_str)
            except Exception as deserialization_exception:
                cls._log.exception(deserialization_exception)
                cls._log.debug(
                    "Deserialization Error: Attempted to deserialize type"
                    " using type: {0}".format(format_type.decode(
                        encoding='UTF-8', errors='ignore')))
                cls._log.debug(
                    "Deserialization Error: Unable to deserialize the "
                    "following:\n{0}".format(serialized_str.decode(
                        encoding='UTF-8', errors='ignore')))

    @classmethod
    def _remove_xml_namespaces(cls, element):
        """Prunes namespaces from XML element

        :param element: element to be trimmed
        :returns: element with namespaces trimmed
        :rtype: :class:`xml.etree.ElementTree.Element`
        """
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

    # These next two functions must be defined by the child classes before
    # serializing
    def _obj_to_dict(self):
        raise NotImplementedError

    def _obj_to_xml_ele(self):
        raise NotImplementedError

    @staticmethod
    def _find(element, tag):
        """Finds element with tag

        :param element: :class:`xml.etree.ElementTree.Element`, the element
            through which to start searching
        :param tag: the tag to search for
        :returns: The element with tag `tag` if found, or a new element with
            tag None if not found
        :rtype: :class:`xml.etree.ElementTree.Element`
        """
        if element is None:
            return ET.Element(None)
        new_element = element.find(tag)
        if new_element is None:
            return ET.Element(None)
        return new_element

    @staticmethod
    def _build_list_model(data, field_name, model):
        """Builds list of python objects from XML or json data

        If data type is json, will find all json objects with `field_name` as
        key, and convert them into python objects of type `model`.
        If XML, will find all :class:`xml.etree.ElementTree.Element` with
        `field_name` as tag, and convert them into python objects of type
        `model`

        :param data: Either json or XML object
        :param str field_name: json key or XML tag
        :param model: Class of objects to be returned
        :returns: list of `model` objects
        :rtype: `list`
        """
        if data is None:
            return []
        if isinstance(data, dict):
            if data.get(field_name) is None:
                return []
            return [model._dict_to_obj(tmp) for tmp in data.get(field_name)]
        return [model._xml_ele_to_obj(tmp) for tmp in data.findall(field_name)]

    @staticmethod
    def _build_list(items, element=None):
        """Builds json object or xml element from model

        Calls either :func:`item._obj_to_dict` or
        :func:`item.obj_to_xml_ele` on all objects in `items`, and either
        returns the dict objects as a list or appends `items` to `element`

        :param items: list of objects for conversion
        :param element: The element to be appended, or None if json
        :returns: list of dicts if `element` is None or  `element` otherwise.
        """
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
        """Creates element with text data

        :returns: new element with name `name` and text `text`
        :rtype: :class:`xml.etree.ElementTree.Element`
        """
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
        """Remove empty values

        Returns a new dictionary based on 'dictionary', minus any keys with
        values that evaluate to False.

        :param dict data: Dictionary to be pruned
        :returns: dictionary without empty values
        :rtype: `dict`
        """
        if isinstance(data, dict):
            return dict(
                (k, v) for k, v in data.items() if v not in (
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
        """Converts object to json or XML

        :param model: Object to convert
        :param boolean json: True if converting to json, false if XML
        """
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
