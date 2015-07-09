from copy import copy
from uuid import uuid4
from xml.etree import ElementTree
import json
import urlparse
from importlib import import_module

from syntribos.datagen import FuzzBehavior


class RequestObject(object):
    behavior = FuzzBehavior

    def __init__(
        self, method, url, static=None, headers=None, params=None,
            data=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or ""
        self.static = static

    def get_request(self, request):
        """ it should be noted this function does not make a request copy"""

        request.data = self.behavior.run_iters(request.data)
        request.headers = self.behavior.run_iters(request.headers)
        request.params = self.behavior.run_iters(request.params)
        request.data = self.behavior.string_data(request.data, self.static)
        return request

    def get_fuzz_requests(self, type_, strings, name):
        attrs = {"BODY": "data", "HEADERS": "headers", "PARAMS": "params"}
        attr = attrs.get(type_, "data")
        for name, data in self.behavior.fuzz_data(
                strings, getattr(self, attr), self.static, name):
            request_copy = copy(self)
            setattr(request_copy, attr, data)
            request_copy = self.get_request(request_copy, self.static)
            yield request_copy


class RequestCreator(object):
    EXTERNAL = "CALL_EXTERNAL:"
    STATIC = "STATIC"

    @classmethod
    def _parse(cls, string, endpoint):
        params = None
        lines = string.splitlines()
        method, url, http_version = lines[0].split()
        url = url.split("?", 1)
        if len(url) > 1:
            params = {}
            for param in url[1].split("&"):
                param = param.split("=", 1)
                if len(param) > 1:
                    params[param[0]] = param[1]
                else:
                    params[param[0]] = ""
        url = url[0]
        url = urlparse.urljoin(endpoint, url)
        for index, line in enumerate(lines):
            if line == "":
                break
        headers = {}
        for line in lines[1:index]:
            key, value = line.split(":", 1)
            headers[key] = value.strip()
        static = str(uuid4())
        data = "\n".join(lines[index+1:]).replace(cls.STATIC, static)
        try:
            data = json.loads(data)
        except:
            try:
                data = ElementTree.fromstring(data)
            except:
                raise Exception("Unknown Data format")
        return RequestObject(
            method=method, url=url, headers=headers, params=params, data=data,
            static=static)

    @classmethod
    def call_external_functions(cls, data):
        if isinstance(data, dict):
            cls._call_external(data)
        else:
            cls._call_external_xml(data)

    @classmethod
    def _call_external(cls, dic):
        for key, val in dic.iteritems():
            if isinstance(val, str):
                dic.update({key: cls._get_external_value(val)})
            elif isinstance(val, dict):
                cls._call_external(val)
            elif isinstance(val, list):
                for i, v in enumerate(val):
                    if cls._iterable(v):
                        val[i] = v.next()
                    elif isinstance(v, dict):
                        val[i] = cls._call_external(v)

    @classmethod
    def _call_external_xml(cls, ele):
        ele.text = cls._get_external_value(ele.text)
        cls._call_external(ele.attrib)
        for i, v in enumerate(list(ele)):
            ele[i] = cls._call_external_xml(v)
        return ele

    @classmethod
    def _get_external_value(cls, string):
        if not string.startswith(cls.CALL_EXTERNAL):
            return string
        _, dot_path, func_name, arg_list = string.split(":", 4)
        mod = import_module(dot_path)
        func = getattr(mod, func_name)
        try:
            args = json.loads(arg_list)
        except:
            args = []
        return func(*args)

    @classmethod
    def create_request(cls, string, endpoint):
        request = cls._parse(string, endpoint)
        cls.call_external_functions(request.data)
        cls.call_external_functions(request.headers)
        cls.call_external_functions(request.params)
        return request
