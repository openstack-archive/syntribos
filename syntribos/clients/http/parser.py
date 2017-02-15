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
from functools import reduce
import importlib
import json
import re
import string
import sys
import types
import uuid
import xml.etree.ElementTree as ElementTree

from oslo_config import cfg
import six
from six.moves import html_parser
from six.moves.urllib import parse as urlparse

from syntribos._i18n import _, _LE, _LW   # noqa

CONF = cfg.CONF
_iterators = {}
_string_var_objs = {}


class RequestCreator(object):
    ACTION_FIELD = "ACTION_FIELD:"
    EXTERNAL = r"CALL_EXTERNAL\|([^:]+?):([^:]+?):([^|]+?)\|"
    METAVAR = r"(\|[^\|]*\|)"
    FUNC_WITH_ARGS = r"([^:]+):([^:]+):(\[.+\])"
    FUNC_NO_ARGS = r"([^:]+):([^:]+)"

    @classmethod
    def create_request(cls, string, endpoint, meta_vars=None):
        """Parse the HTTP request template into its components

        :param str string: HTTP request template
        :param str endpoint: URL of the target to be tested
        :param dict meta_vars: Default None, dict parsed from meta.json
        :rtype: :class:`syntribos.clients.http.parser.RequestObject`
        :returns: RequestObject with method, url, params, etc. for use by
                  runner
        """
        if meta_vars:
            cls.meta_vars = meta_vars
        string = cls.call_external_functions(string)
        action_field = str(uuid.uuid4()).replace("-", "")
        string = string.replace(cls.ACTION_FIELD, action_field)
        lines = string.splitlines()
        for index, line in enumerate(lines):
            if line == "":
                break
        if lines[index] != "":
            index = index + 1
        method, url, params, version = cls._parse_url_line(lines[0], endpoint)
        headers = cls._parse_headers(lines[1:index])
        data = cls._parse_data(lines[index + 1:])
        return RequestObject(
            method=method, url=url, headers=headers, params=params, data=data,
            action_field=action_field)

    @classmethod
    def _create_var_obj(cls, var):
        """Given the name of a variable, creates VariableObject

        :param str var: name of the variable in meta.json
        :rtype: :class:`syntribos.clients.http.parser.VariableObject`
        :returns: VariableObject holding the attributes defined in the JSON
                  object read in from meta.json
        """
        if var not in cls.meta_vars:
            msg = _("Expected to find %s in meta.json, but didn't. "
                    "Check your templates") % var
            raise TemplateParseException(msg)
        var_dict = cls.meta_vars[var]
        if "type" in var_dict:
            var_dict["var_type"] = var_dict.pop("type")
        var_obj = VariableObject(var, **var_dict)
        return var_obj

    @classmethod
    def replace_one_variable(cls, var_obj):
        """Evaluate a VariableObject according to its type

        A meta variable's type is optional. If a type is given, the parser will
        interpret the variable in one of 3 ways according to its type, and
        returns that value.

        * Type config: The parser will attempt to read the config value
          specified by the "val" attribute and returns that value.
        * Type function: The parser will call the function named in the "val"
          attribute with arguments given in the "args" attribute, and returns
          the value from calling the function. This value is cached, and
          will be returned on subsequent calls.
        * Type generator: works the same way as the function type, but its
          results are not cached and the function will be called every time.

        Otherwise, the parser will interpret the variable as a static variable,
        and will return whatever is in the "val" attribute.

        :param var_obj: A :class:`syntribos.clients.http.parser.VariableObject`
        :returns: The evaluated value according to its meta variable type
        """
        if var_obj.var_type == 'config':
            try:
                return reduce(getattr, var_obj.val.split("."), CONF)
            except AttributeError:
                msg = _("Meta json file contains reference to the config "
                        "option %s, which does not appear to"
                        "exist.") % var_obj.val
                raise TemplateParseException(msg)

        elif var_obj.var_type == 'function':
            if var_obj.function_return_value:
                return var_obj.function_return_value
            if not var_obj.val:
                msg = _("The type of variable %s is function, but there is no "
                        "reference to the function.") % var_obj.name
                raise TemplateParseException(msg)
            else:
                var_obj.function_return_value = cls.call_one_external_function(
                    var_obj.val, var_obj.args)
                return var_obj.function_return_value

        elif var_obj.var_type == 'generator':
            if not var_obj.val:
                msg = _("The type of variable %s is generator, but there is no"
                        " reference to the function.") % var_obj.name
                raise TemplateParseException(msg)

            return cls.call_one_external_function(var_obj.val, var_obj.args)
        else:
            return str(var_obj.val)

    @classmethod
    def _replace_dict_variables(cls, dic):
        """Recursively evaluates all meta variables in a given dict."""
        for (key, value) in dic.items():
            # Keys dont get fuzzed, so can handle them here
            match = re.search(cls.METAVAR, key)
            if match:
                replaced_key = match.group(0).strip("|")
                key_obj = cls._create_var_obj(replaced_key)
                replaced_key = cls.replace_one_variable(key_obj)
                new_key = re.sub(cls.METAVAR, replaced_key, key)
                del dic[key]
                dic[new_key] = value
            # Vals are fuzzed so they need to be passed to datagen as an object
            if isinstance(value, six.string_types):
                match = re.search(cls.METAVAR, value)
                if match:
                    var_str = match.group(0).strip("|")
                    if var_str != value.strip("|%s" % string.whitespace):
                        msg = _("Meta-variable references cannot come in the "
                                "middle of the value %s") % value
                        raise TemplateParseException(msg)
                    val_obj = cls._create_var_obj(var_str)
                    if key in dic:
                        dic[key] = val_obj
                    elif new_key in dic:
                        dic[new_key] = val_obj
            elif isinstance(value, dict):
                cls._replace_dict_variables(value)
        return dic

    @classmethod
    def _replace_str_variables(cls, string):
        """Replaces all meta variable references in the string

        For every meta variable reference found in the string, it generates
        a VariableObject. It then associates each VariableObject with a uuid,
        as a key value pair, which is storedin the global dict variable
        `_str_var_obs`. It then replaces all meta variable references in the
        string with the uuid key to the VariableObject

        :param str string: String to be evaluated
        :returns: string with all metavariable references replaced
        """
        while True:
            match = re.search(cls.METAVAR, string)
            if not match:
                break
            obj_ref_uuid = str(uuid.uuid4()).replace("-", "")
            var_name = match.group(1).strip("|")
            var_obj = cls._create_var_obj(var_name)
            _string_var_objs[obj_ref_uuid] = var_obj
            string = re.sub(cls.METAVAR, obj_ref_uuid, string, count=1)
        return string

    @classmethod
    def _parse_url_line(cls, line, endpoint):
        """Split first line of an HTTP request into its components

        :param str line: the first line of the HTTP request
        :param str endpoint: the full URL of the endpoint to test
        :rtype: tuple
        :returns: HTTP method, URL, request parameters, HTTP version
        """
        valid_methods = ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE",
                         "TRACE", "CONNECT", "PATCH"]
        params = {}
        method, url, version = line.split()
        url = url.split("?", 1)
        if len(url) == 2:
            for param in url[1].split("&"):
                param = param.split("=", 1)
                if len(param) > 1:
                    params[param[0]] = param[1]
                else:
                    params[param[0]] = ""
        url = url[0]
        url = urlparse.urljoin(endpoint, url)
        if method not in valid_methods:
            raise ValueError(_("Invalid HTTP method: %s") % method)
        return (method, cls._replace_str_variables(url),
                cls._replace_dict_variables(params), version)

    @classmethod
    def _parse_headers(cls, lines):
        """Find and return headers in HTTP request

        :param str lines:  All but the first line of the HTTP request (list)
        :rtype: dict
        :returns: headers as key:value pairs
        """
        headers = {}
        for line in lines:
            key, value = line.split(":", 1)
            headers[key] = value.strip()
        return cls._replace_dict_variables(headers)

    @classmethod
    def _parse_data(cls, lines):
        """Parse the body of the HTTP request (e.g. POST variables)

        :param list lines: lines of the HTTP body

        :returns: object representation of body data (JSON or XML)
        """
        postdat_regex = r"([\w%]+=[\w%]+&?)+"
        data = "\n".join(lines).strip()
        if not data:
            return ""
        try:
            data = json.loads(data)
            # TODO(cneill): Make this less hacky
            if isinstance(data, list):
                data = json.dumps(data)
            if isinstance(data, dict):
                return cls._replace_dict_variables(data)
            else:
                return cls._replace_str_variables(data)
        except TemplateParseException:
            raise
        except (TypeError, ValueError):
            try:
                data = ElementTree.fromstring(data)
            except Exception:
                if not re.match(postdat_regex, data):
                    raise TypeError(_("Unknown data format"))
        except Exception:
            raise
        return data

    @classmethod
    def call_external_functions(cls, string):
        """Parse external function calls in the body of request templates

        :param str string: full HTTP request template as a string
        :rtype: str
        :returns: the request, with EXTERNAL calls filled in with their values
                  or UUIDs
        """
        if not isinstance(string, six.string_types):
            return string
        while True:
            match = re.search(cls.EXTERNAL, string)
            if not match:
                break
            dot_path = match.group(1)
            func_name = match.group(2)
            arg_list = match.group(3)
            mod = importlib.import_module(dot_path)
            func = getattr(mod, func_name)
            args = json.loads(arg_list)
            val = func(*args)
            if isinstance(val, types.GeneratorType):
                local_uuid = str(uuid.uuid4()).replace("-", "")
                string = re.sub(cls.EXTERNAL, local_uuid, string, count=1)
                _iterators[local_uuid] = val
            else:
                string = re.sub(cls.EXTERNAL, str(val), string, count=1)
        return string

    @classmethod
    def call_one_external_function(cls, string, args):
        """Calls one function read in from templates and returns the result."""
        if not isinstance(string, six.string_types):
            return string
        match = re.search(cls.FUNC_NO_ARGS, string)
        func_string_has_args = False
        if not match:
            match = re.search(cls.FUNC_WITH_ARGS, string)
            func_string_has_args = True

        if match:
            try:
                dot_path = match.group(1)
                func_name = match.group(2)
                mod = importlib.import_module(dot_path)
                func = getattr(mod, func_name)

                if func_string_has_args and not args:
                    arg_list = match.group(3)
                    args = json.loads(arg_list)

                val = func(*args)
            except Exception:
                msg = _("The reference to the function %s failed to parse "
                        "correctly, please check the documentation to ensure "
                        "your function import string adheres to the proper "
                        "format") % string
                raise TemplateParseException(msg)

        else:
            try:
                func_lst = string.split(":")
                if len(func_lst) == 2:
                    args = func_lst[1]
                func_str = func_lst[0]
                dot_path = ".".join(func_str.split(".")[:-1])
                func_name = func_str.split(".")[-1]
                mod = importlib.import_module(dot_path)
                func = getattr(mod, func_name)
                val = func(*args)
            except Exception:
                msg = _("The reference to the function %s failed to parse "
                        "correctly, please check the documentation to ensure "
                        "your function import string adheres to the proper "
                        "format") % string
                raise TemplateParseException(msg)

        if isinstance(val, types.GeneratorType):
            return str(six.next(val))
        else:
            return str(val)


class VariableObject(object):
    VAR_TYPES = ["function", "generator", "config"]
    FUZZ_TYPES = ["int", "ascii", "url"]

    def __init__(self, name, var_type="", args=[], val="", fuzz=True,
                 fuzz_types=[], min_length=0, max_length=sys.maxsize,
                 url_encode=False, **kwargs):
        if var_type and var_type.lower() not in self.VAR_TYPES:
            msg = _("The meta variable %(name)s has a type of %(var)s which "
                    "syntribos does not"
                    "recognize") % {'name': name, 'var': var_type}
            raise TemplateParseException(msg)

        self.name = name
        self.var_type = var_type.lower()
        self.val = val
        self.args = args
        self.fuzz_types = fuzz_types
        self.fuzz = fuzz
        self.min_length = min_length
        self.max_length = max_length
        self.url_encode = url_encode
        self.function_return_value = None

    def __repr__(self):
        return str(vars(self))


class TemplateParseException(Exception):
    pass


class RequestHelperMixin(object):
    """Class that helps with fuzzing requests."""

    def __init__(self):
        self.data = ""
        self.headers = ""
        self.params = ""
        self.data = ""
        self.url = ""
        self.url = ""

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
        elif isinstance(data, VariableObject):
            return RequestCreator.replace_one_variable(data)
        elif isinstance(data, six.string_types):
            data = data.replace(action_field, "")
            return cls._replace_iter(data)
        else:
            return data

    @classmethod
    def _run_iters_dict(cls, dic, action_field=""):
        """Run fuzz iterators for a dict type."""
        for key, val in dic.items():
            dic[key] = val = cls._replace_iter(val)
            if isinstance(key, six.string_types):
                new_key = cls._replace_iter(key).replace(action_field, "")
                if new_key != key:
                    del dic[key]
                    dic[new_key] = val
            if isinstance(val, VariableObject):
                if key in dic:
                    dic[key] = RequestCreator.replace_one_variable(val)
                elif new_key in dic:
                    dic[new_key] = RequestCreator.replace_one_variable(val)
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
            if isinstance(v, VariableObject):
                val[i] = v = RequestCreator.replace_one_variable(v)
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
        for k, v in list(_iterators.items()):
            if k in string:
                string = string.replace(k, six.next(v))
        for k, v in _string_var_objs.items():
            if k in string:
                str_val = str(RequestCreator.replace_one_variable(v))
                string = string.replace(k, str_val)
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
