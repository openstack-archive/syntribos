from copy import deepcopy
from importlib import import_module
from uuid import uuid4
from xml.etree import ElementTree
import json
import re
import types
import urlparse

from cafe.engine.http.client import HTTPClient

_iterators = {}


class SynHTTPClient(HTTPClient):
    def send_request(self, r):
        return self.request(
            method=r.method, url=r.url, headers=r.headers, params=r.params,
            data=r.data)


class RequestHelperMixin(object):
    @classmethod
    def _run_iters(cls, data, action_field):
        if isinstance(data, dict):
            return cls._run_iters_dict(data, action_field)
        elif isinstance(data, ElementTree.Element):
            return cls._run_iters_xml(data, action_field)
        else:
            return data

    @classmethod
    def _run_iters_dict(cls, dic, action_field=""):
        for key, val in dic.iteritems():
            dic[key] = val = cls._replace_iter(val)
            if isinstance(key, basestring):
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
        for i, v in enumerate(val):
            if isinstance(v, basestring):
                val[i] = v = cls._replace_iter(v).replace(action_field, "")
            elif isinstance(v, dict):
                val[i] = cls._run_iters_dict(v, action_field)
            elif isinstance(v, list):
                cls._run_iters_list(v, action_field)

    @classmethod
    def _run_iters_xml(cls, ele, action_field=""):
        if isinstance(ele.text, basestring):
            ele.text = cls._replace_iter(ele.text).replace(action_field, "")
        cls._run_iters_dict(ele.attrib, action_field)
        for i, v in enumerate(list(ele)):
            ele[i] = cls._run_iters_xml(v, action_field)
        return ele

    @staticmethod
    def _string_data(data):
        if isinstance(data, dict):
            return json.dumps(data)
        elif isinstance(data, ElementTree.Element):
            return ElementTree.tostring(data)
        else:
            return data

    @staticmethod
    def _replace_iter(string):
        if not isinstance(string, basestring):
            return string
        for k, v in _iterators.items():
            if k in string:
                string = string.replace(k, v.next())
        return string


class RequestObject(RequestHelperMixin):
    def __init__(
        self, method, url, action_field=None, headers=None, params=None,
            data=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.data = data
        self.action_field = action_field

    def prepare_request(self):
        """ it should be noted this function does not make a request copy
            destroying iterators in request.  A copy should be made if making
            multiple requests"""
        self.data = self._run_iters(self.data, self.action_field)
        self.headers = self._run_iters(self.headers, self.action_field)
        self.params = self._run_iters(self.params, self.action_field)
        self.data = self._string_data(self.data)

    def get_prepared_copy(self):
        copy = deepcopy(self)
        copy.prepare_request()
        return copy

    def get_copy(self):
        return deepcopy(self)


class RequestCreator(object):
    ACTION_FIELD = "ACTION_FIELD:"
    EXTERNAL = r"CALL_EXTERNAL\|([^|]+?):([^|]+?):([^|]+?)\|"

    @classmethod
    def create_request(cls, string, endpoint):
        string = cls.call_external_functions(string)
        action_field = str(uuid4()).replace("-", "")
        string = string.replace(cls.ACTION_FIELD, action_field)
        lines = string.splitlines()
        for index, line in enumerate(lines):
            if line == "":
                break
        method, url, params, version = cls._parse_url_line(lines[0], endpoint)
        headers = cls._parse_headers(lines[1:index])
        data = cls._parse_data(lines[index+1:])
        return RequestObject(
            method=method, url=url, headers=headers, params=params, data=data,
            action_field=action_field)

    @classmethod
    def _parse_url_line(cls, line, endpoint):
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
        return method, url, params, version

    @classmethod
    def _parse_headers(cls, lines):
        headers = {}
        for line in lines:
            key, value = line.split(":", 1)
            headers[key] = value.strip()
        return headers

    @classmethod
    def _parse_data(cls, lines):
        data = "\n".join(lines).strip()
        if not data:
            return ""
        try:
            data = json.loads(data)
        except:
            try:
                data = ElementTree.fromstring(data)
            except:
                raise Exception("Unknown Data format")
        return data

    @classmethod
    def call_external_functions(cls, string):
        if not isinstance(string, basestring):
            return string

        while True:
            match = re.search(cls.EXTERNAL, string)
            if not match:
                break
            dot_path = match.group(1)
            func_name = match.group(2)
            arg_list = match.group(3)
            mod = import_module(dot_path)
            func = getattr(mod, func_name)
            args = json.loads(arg_list)
            val = func(*args)
            if isinstance(val, types.GeneratorType):
                uuid = str(uuid4()).replace("-", "")
                string = re.sub(cls.EXTERNAL, uuid, string, count=1)
                _iterators[uuid] = val
            else:
                string = re.sub(cls.EXTERNAL, str(val), string, count=1)
        return string
