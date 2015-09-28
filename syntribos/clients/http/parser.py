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
from importlib import import_module
from uuid import uuid4
from xml.etree import ElementTree
import json
import re
import types
import urlparse

from syntribos.clients.http.models import RequestObject, _iterators


class RequestCreator(object):
    ACTION_FIELD = "ACTION_FIELD:"
    EXTERNAL = r"CALL_EXTERNAL\|([^:]+?):([^:]+?):([^|]+?)\|"
    request_model_type = RequestObject

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
        data = cls._parse_data(lines[index + 1:])
        return cls.request_model_type(
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
