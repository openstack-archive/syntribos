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
import copy
import re
from xml.etree import ElementTree

import six

from syntribos.clients.http.parser import _string_var_objs
from syntribos.clients.http.parser import RequestCreator
from syntribos.clients.http import VariableObject


def fuzz_request(req, strings, fuzz_type, name_prefix):
    """Creates the fuzzed RequestObject

    Gets the name and the fuzzed request model from _fuzz_data, and
    creates a RequestObject from the parameters of the model.

    :param req: The RequestObject to be fuzzed
    :type req: :class:`syntribos.clients.http.parser.RequestObject`
    :param list strings: List of strings to fuzz with
    :param str fuzz_type: What attribute of the RequestObject to fuzz
    :param name_prefix: (Used for ImpactedParameter)
    :returns: Generator of tuples:
        (name, request, fuzzstring, ImpactedParameter name)
    :rtype: `tuple`
    """
    for name, data, stri, param_path in _fuzz_data(
            strings, getattr(req, fuzz_type), req.action_field, name_prefix):
        request_copy = req.get_copy()
        setattr(request_copy, fuzz_type, data)
        request_copy.prepare_request()
        yield name, request_copy, stri, param_path


def _fuzz_data(strings, data, skip_var, name_prefix):
    """Iterates through model fields and places fuzz string in each field

    For each attribute in the model object, call the _build_X_combinations
    method corresponding to the type of the data parameter, which replaces
    the value with the fuzz string.

    :param list strings: List of strings to fuzz with
    :param data: Can be a dict, XML Element, or string
    :param str skip_var: String representing ACTION_FIELDs
    :param str name_prefix: (Used for ImpactedParameter)
    :returns: Generator of tuples:
        (name, model, string, ImpactedParameter name)
    """
    param_path = ""
    for str_num, stri in enumerate(strings, 1):
        if isinstance(data, dict):
            model_iter = _build_dict_combinations(stri, data, skip_var)
        elif isinstance(data, ElementTree.Element):
            model_iter = _build_xml_combinations(stri, data, skip_var)
        elif isinstance(data, six.string_types):
            model_iter = _build_str_combinations(stri, data)
        else:
            raise TypeError("Format not recognized!")
        for model_num, (model, param_path) in enumerate(model_iter, 1):
            name = "{0}str{1}_model{2}".format(name_prefix, str_num, model_num)
            yield (name, model, stri, param_path)


def _build_str_combinations(fuzz_string, data):
    """Places `fuzz_string` in fuzz location for string data.

    :param str fuzz_string: Value to place in fuzz location
    :param str data: Lines from the request template
    """
    # Match either "{identifier:value}" or "{value}"
    var_regex = r"{([\w]*):?([^}]*)}"
    for match in re.finditer(var_regex, data):
        start, stop = match.span()
        model = "{0}{1}{2}".format(data[:start], fuzz_string, data[stop:])

        if match.group(1):
            # The string is of the format "{identifier:value}", so we just
            # want the identifier as the param_path
            param = match.group(1)
        else:
            param = match.group(0)

        if param in _string_var_objs:
            var_obj = _string_var_objs[param]
            if not _check_var_obj_limits(var_obj, fuzz_string):
                continue
            param = RequestCreator.replace_one_variable(var_obj)
        yield model, param


def _build_dict_combinations(fuzz_string, dic, skip_var):
    """Places fuzz string in fuzz location for object data.

    :param str fuzz_string: Value to place in fuzz location
    :param dic: A dictionary to fuzz
    :param skip_var: ACTION_FIELD UUID value to skip
    """
    for key, val in dic.items():
        if skip_var in key:
            continue
        elif isinstance(val, VariableObject):
            if not _check_var_obj_limits(val, fuzz_string):
                continue
            else:
                yield _merge_dictionaries(dic, {key: fuzz_string}), key
        elif isinstance(val, dict):
            for ret, param_path in _build_dict_combinations(fuzz_string, val,
                                                            skip_var):
                yield (_merge_dictionaries(dic, {
                    key: ret
                }), "{0}/{1}".format(key, param_path))
        elif isinstance(val, list):
            for i, v in enumerate(val):
                list_ = [_ for _ in val]
                if isinstance(v, dict):
                    for ret, param_path in _build_dict_combinations(
                            fuzz_string, v, skip_var):
                        list_[i] = copy.copy(ret)
                        yield (_merge_dictionaries(dic, {
                            key: ret
                        }), "{0}[{1}]/{2}".format(key, i, param_path))
                elif isinstance(v, VariableObject):
                    if not _check_var_obj_limits(v, fuzz_string):
                        continue
                else:
                    list_[i] = fuzz_string
                    yield (_merge_dictionaries(dic, {
                        key: list_
                    }), "{0}[{1}]".format(key, i))
        else:
            yield _merge_dictionaries(dic, {key: fuzz_string}), key


def _merge_dictionaries(x, y):
    """Merge `dicts` together

    Create a copy of `x`, and update that with elements of `y`, to prevent
    squashing of passed in dicts.

    :param dict x: Dictionary 1
    :param dict y: Dictionary 2
    :returns: Merged dictionary
    :rtype: `dict`
    """

    z = x.copy()
    z.update(y)
    return z


def _build_xml_combinations(stri, ele, skip_var):
    """Places fuzz string in fuzz location for XML data."""
    if skip_var not in ele.tag:
        if ele.text and skip_var not in ele.text:
            yield _update_xml_ele_text(ele, stri), ele.tag
        for attr, param_path in _build_dict_combinations(stri, ele.attrib,
                                                         skip_var):
            yield (_update_xml_ele_attribs(ele, attr),
                   "{0}/{1}".format(ele.tag, param_path))
        for i, element in enumerate(list(ele)):
            for ret, param_path in _build_xml_combinations(stri, element,
                                                           skip_var):
                list_ = list(ele)
                list_[i] = copy.copy(ret)
                yield (_update_inner_xml_ele(ele, list_),
                       "{0}/{1}".format(ele.tag, param_path))


def _update_xml_ele_text(ele, text):
    """Copies an XML element, updates its text attribute with `text`

    :param ele: XML element to be copied, modified
    :type ele: :class:`xml.ElementTree.Element`
    :param str text: Text to populate `ele`'s text attribute with
    :returns: XML element with "text" attribute set to `text`
    :rtype: :class:`xml.ElementTree.Element`
    """
    ret = copy.copy(ele)
    ret.text = text
    return ret


def _update_xml_ele_attribs(ele, attribs):
    """Copies an XML element, populates attributes from `attribs`

    :param ele: XML element to be copied, modified
    :type ele: :class:`xml.ElementTree.Element`
    :param dict attribs: Source of new attribute values for `ele`
    :returns: XML element with all attributes overwritten by `attribs`
    :rtype: :class:`xml.ElementTree.Element`
    """
    ret = copy.copy(ele)
    ret.attrib = attribs
    return ret


def _update_inner_xml_ele(ele, list_):
    """Copies an XML element, populates sub-elements from `list_`

    Returns a copy of the element with the subelements given via list_
    :param ele: XML element to be copied, modified
    :type ele: :class:`xml.ElementTree.Element`
    :param list list_: List of subelements to append to `ele`
    :returns: XML element with new subelements from `list_`
    :rtype: :class:`xml.ElementTree.Element`
    """
    ret = copy.copy(ele)
    for i, v in enumerate(list_):
        ret[i] = v
    return ret


def _check_var_obj_limits(var_obj, fuzz_string):
    if not var_obj.fuzz:
        return False
    if var_obj.fuzz_types:
        ret = False
        if "int" in var_obj.fuzz_types:
            try:
                int(fuzz_string)
                ret = True
            except ValueError:
                pass
        if "ascii" in var_obj.fuzz_types:
            try:
                fuzz_string.encode('ascii')
                ret = True
            except UnicodeEncodeError:
                pass
        if "url" in var_obj.fuzz_types:
            url_re = r"^[A-Za-z0-9\-\._~:\/\?#[\]@!\$&'()*\+,;=%]+$"
            if re.match(url_re, fuzz_string):
                ret = True
        if "str" in var_obj.fuzz_types:
            try:
                str(fuzz_string)
                ret = True
            except ValueError:
                pass
        if not ret:
            return ret

    if len(fuzz_string) > var_obj.max_length:
        return False
    if len(fuzz_string) < var_obj.min_length:
        return False
    return True
