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
import re
from xml.etree import ElementTree

from syntribos.clients.http.models import RequestHelperMixin
from syntribos.clients.http.models import RequestObject
from syntribos.clients.http import parser


class FuzzMixin(object):

    """Mixin for fuzz tests

    This class provides the :meth:`~.FuzzMixin._fuzz_data` function which
    yields a test name and all iterations of a given piece of data (currently
    supports `dict`, :class:`xml.etree.ElementTree.Element`, and `basestring`
    formats) with each string provided.
    """
    @classmethod
    def _fuzz_data(cls, strings, data, skip_var, name_prefix):
        """Iterates through model fields and places fuzz string in each field

        For each attribute in the model object, call the _build_combinations
        method corresponding to the type of the data parameter, which replaces
        the value with the fuzz string.

        :param strings:
        :param data:
        :param skip_var:
        :param name_prefix:
        """
        param_path = ""
        for str_num, stri in enumerate(strings, 1):
            if isinstance(data, dict):
                model_iter = cls._build_combinations(stri, data, skip_var)
            elif isinstance(data, ElementTree.Element):
                model_iter = cls._build_xml_combinations(stri, data, skip_var)
            elif isinstance(data, basestring):
                model_iter = cls._build_str_combinations(stri, data)
            else:
                raise TypeError("Format not recognized!")
            for model_num, (model, param_path) in enumerate(model_iter, 1):
                name = "{0}str{1}_model{2}".format(
                    name_prefix, str_num, model_num)
                yield (name, model, stri, param_path)

    @classmethod
    def _build_str_combinations(cls, fuzz_string, data):
        """Places `fuzz_string` in fuzz location for string data.

        :param str fuzz_string: Value to place in fuzz location
        :param str data: Lines from the request template
        """
        for match in re.finditer(r"{([\w]*):?([^}]*)}", data):
            # Match either "{identifier:value}" or "{value}"
            start, stop = match.span()
            model = "{0}{1}{2}".format(
                    cls.remove_braces(data[:start]),
                    fuzz_string, cls.remove_braces(data[stop:]))
            if match.group(1):
                # The string is of the format "{identifier:value}", so we just
                # want the identifier as the param_path
                yield model, match.group(1)
            else:
                yield model, cls.remove_braces(match.group(0))

    @classmethod
    def _build_combinations(cls, stri, dic, skip_var):
        """Places fuzz string in fuzz location for object data.

        :param stri:
        :param dic:
        :param skip_var:
        """
        for key, val in dic.iteritems():
            if skip_var in key:
                continue
            elif isinstance(val, dict):
                for ret, param_path in cls._build_combinations(
                        stri, val, skip_var):
                    yield (cls._merge_dictionaries(dic, {key: ret}),
                           "{0}/{1}".format(key, param_path))
            elif isinstance(val, list):
                for i, v in enumerate(val):
                    list_ = [_ for _ in val]
                    if isinstance(v, dict):
                        for ret, param_path in cls._build_combinations(
                                stri, v, skip_var):
                            list_[i] = ret.copy()
                            yield (cls._merge_dictionaries(dic, {key: ret}),
                                   "{0}[{1}]/{2}".format(key, i, param_path))
                    else:
                        list_[i] = stri
                        yield (cls._merge_dictionaries(dic, {key: list_}),
                               "{0}[{1}]".format(key, i))
            else:
                yield cls._merge_dictionaries(dic, {key: stri}), key

    @staticmethod
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

    @classmethod
    def _build_xml_combinations(cls, stri, ele, skip_var):
        """Places fuzz string in fuzz location for XML data."""
        if skip_var not in ele.tag:
            if not ele.text or (skip_var not in ele.text):
                yield cls._update_element(ele, stri), ele.tag
            for attr, param_path in cls._build_combinations(
                    stri, ele.attrib, skip_var):
                yield (cls._update_attribs(ele, attr),
                       "{0}/{1}".format(ele.tag, param_path))
            for i, element in enumerate(list(ele)):
                for ret, param_path in cls._build_xml_combinations(
                        stri, element, skip_var):
                    list_ = list(ele)
                    list_[i] = ret.copy()
                    yield (cls._update_inner_element(ele, list_),
                           "{0}/{1}".format(ele.tag, param_path))

    @staticmethod
    def _update_element(ele, text):
        """Copies an XML element, updates its text attribute with `text`

        :param ele: XML element to be copied, modified
        :type ele: :class:`xml.ElementTree.Element`
        :param str text: Text to populate `ele`'s text attribute with
        :returns: XML element with "text" attribute set to `text`
        :rtype: :class:`xml.ElementTree.Element`
        """
        ret = ele.copy()
        ret.text = text
        return ret

    @staticmethod
    def _update_attribs(ele, attribs):
        """Copies an XML element, populates attributes from `attribs`

        :param ele: XML element to be copied, modified
        :type ele: :class:`xml.ElementTree.Element`
        :param dict attribs: Source of new attribute values for `ele`
        :returns: XML element with all attributes overwritten by `attribs`
        :rtype: :class:`xml.ElementTree.Element`
        """
        ret = ele.copy()
        ret.attrib = attribs
        return ret

    @staticmethod
    def _update_inner_element(ele, list_):
        """Copies an XML element, populates sub-elements from `list_`

        Returns a copy of the element with the subelements given via list_
        :param ele: XML element to be copied, modified
        :type ele: :class:`xml.ElementTree.Element`
        :param list list_: List of subelements to append to `ele`
        :returns: XML element with new subelements from `list_`
        :rtype: :class:`xml.ElementTree.Element`
        """
        ret = ele.copy()
        for i, v in enumerate(list_):
            ret[i] = v
        return ret

    @staticmethod
    def remove_braces(string):
        """Remove braces from strings (in request templates)."""
        return string.replace("}", "").replace("{", "")

    @staticmethod
    def remove_attr_names(string):
        """removes identifiers from string substitution

        If we are fuzzing example.com/{userid:123}, this method removes the
        identifier name so that the client only sees example.com/{123} when
        it sends the request
        """
        return re.sub(r"{[\w]+:", "{", string)


class FuzzRequest(RequestObject, FuzzMixin, RequestHelperMixin):

    def fuzz_request(self, strings, fuzz_type, name_prefix):
        """Creates the fuzzed request object

        Gets the name and the fuzzed request model from _fuzz_data, and
        creates a request object from the parameters of the model.

        :param strings:
        :param fuzz_type:
        :param name_prefix:
        :returns: Generator of tuples:
            (name, request, fuzzstring, ImpactedParameter name)
        :rtype: `tuple`
        """
        for name, data, stri, param_path in self._fuzz_data(
            strings, getattr(self, fuzz_type), self.action_field,
                name_prefix):
            request_copy = self.get_copy()
            setattr(request_copy, fuzz_type, data)
            request_copy.prepare_request(fuzz_type)
            yield name, request_copy, stri, param_path

    def prepare_request(self, fuzz_type=None):
        super(FuzzRequest, self).prepare_request()
        if fuzz_type != "url":
            self.url = self.remove_attr_names(self.url)
            self.url = self.remove_braces(self.url)


class FuzzParser(parser):
    request_model_type = FuzzRequest
