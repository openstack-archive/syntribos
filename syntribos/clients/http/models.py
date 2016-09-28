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
import json
import re
import xml.etree.ElementTree as ElementTree

import six
from six.moves import html_parser

_iterators = {}


class RequestHelperMixin(object):
    """Class that helps with fuzzing requests."""

    @classmethod
    def _run_iters(cls, data, action_field):
        """Recursively fuzz variables in `data` and its children

        :param data: The request data to be modified
        :param action_field: The name of the field to be replaced
        :returns: object or string with action_field fuzzed
        :rtype: `dict` OR `str` OR :class:`ElementTree.Element`
        """
        if isinstance(data, dict):
            return cls._run_iters_dict(data, action_field)
        elif isinstance(data, ElementTree.Element):
            return cls._run_iters_xml(data, action_field)
        elif isinstance(data, six.string_types):
            data = data.replace(action_field, "")
            return cls._replace_iter(data)
        else:
            return data

    @classmethod
    def _run_iters_dict(cls, dic, action_field=""):
        """Run fuzz iterators for a dict type."""
        for key, val in six.iteritems(dic):
            dic[key] = val = cls._replace_iter(val)
            if isinstance(key, six.string_types):
                new_key = cls._replace_iter(key).replace(action_field, "")
                if new_key != key:
                    del dic[key]
                    dic[new_key] = val
            if isinstance(val, dict):
                cls._run_iters_dict(val, action_field)
            elif isinstance(val, list):
                cls._run_iters_list(val, action_field)
        return dic

    @classmethod
    def _run_iters_list(cls, val, action_field=""):
        """Run fuzz iterators for a list type."""
        for i, v in enumerate(val):
            if isinstance(v, six.string_types):
                val[i] = v = cls._replace_iter(v).replace(action_field, "")
            elif isinstance(v, dict):
                val[i] = cls._run_iters_dict(v, action_field)
            elif isinstance(v, list):
                cls._run_iters_list(v, action_field)

    @classmethod
    def _run_iters_xml(cls, ele, action_field=""):
        """Run fuzz iterators for an XML element type."""
        if isinstance(ele.text, six.string_types):
            ele.text = cls._replace_iter(ele.text).replace(action_field, "")
        cls._run_iters_dict(ele.attrib, action_field)
        for i, v in enumerate(list(ele)):
            ele[i] = cls._run_iters_xml(v, action_field)
        return ele

    @staticmethod
    def _string_data(data):
        """Replace various objects types with string representations."""
        if isinstance(data, dict):
            return json.dumps(data)
        elif isinstance(data, ElementTree.Element):
            str_data = ElementTree.tostring(data)
            # No way to stop tostring from HTML escaping even if we wanted
            h = html_parser.HTMLParser()
            return h.unescape(str_data.decode())
        else:
            return data

    @staticmethod
    def _replace_iter(string):
        """Fuzz a string."""
        if not isinstance(string, six.string_types):
            return string
        for k, v in list(six.iteritems(_iterators)):
            if k in string:
                string = string.replace(k, six.next(v))
        return string

    @staticmethod
    def _remove_braces(string):
        """Remove braces from strings (in request templates)."""
        return re.sub(r"{([^}]*)}", "\\1", string)

    @staticmethod
    def _remove_attr_names(string):
        """removes identifiers from string substitution

        If we are fuzzing example.com/{userid:123}, this method removes the
        identifier name so that the client only sees example.com/{123} when
        it sends the request
        """
        return re.sub(r"{[\w]+:", "{", string)

    def prepare_request(self):
        """Prepare a request for sending off

        It should be noted this function does not make a request copy,
        destroying iterators in request.  A copy should be made if making
        multiple requests.
        """
        self.data = self._run_iters(self.data, self.action_field)
        self.headers = self._run_iters(self.headers, self.action_field)
        self.params = self._run_iters(self.params, self.action_field)
        self.data = self._string_data(self.data)
        self.url = self._run_iters(self.url, self.action_field)
        self.url = self._remove_braces(self._remove_attr_names(self.url))

    def get_prepared_copy(self):
        """Create a copy of `self`, and prepare it for use by a fuzzer

        :returns: Copy of request object that has been prepared for sending
        :rtype: :class:`RequestHelperMixin`
        """
        local_copy = copy.deepcopy(self)
        local_copy.prepare_request()
        return local_copy

    def get_copy(self):
        return copy.deepcopy(self)


class RequestObject(RequestHelperMixin):
    """An object that holds information about an HTTP request.

    :ivar str method: Request method
    :ivar str url: URL to request
    :ivar dict action_field: Action Fields
    :ivar dict headers: Dictionary of headers in name:value format
    :ivar dict params: Dictionary of params in name:value format
    :ivar data: Data to send as part of request body
    :ivar bool sanitize: Boolean variable used to filter secrets
    """

    def __init__(self,
                 method,
                 url,
                 action_field=None,
                 headers=None,
                 params=None,
                 data=None,
                 sanitize=False):
        self.method = method
        self.url = url
        self.action_field = action_field
        self.headers = headers
        self.params = params
        self.data = data
        self.sanitize = sanitize
