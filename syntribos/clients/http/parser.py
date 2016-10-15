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
import importlib
import json
import re
import types
import uuid
import xml.etree.ElementTree as ElementTree

import six
from six.moves.urllib import parse as urlparse

from syntribos.clients.http.models import _iterators
from syntribos.clients.http.models import RequestObject


class RequestCreator(object):
    ACTION_FIELD = "ACTION_FIELD:"
    EXTERNAL = r"CALL_EXTERNAL\|([^:]+?):([^:]+?):([^|]+?)\|"
    request_model_type = RequestObject

    @classmethod
    def create_request(cls, string, endpoint):
        """Parse the HTTP request template into its components

        :param str string: HTTP request template
        :param str endpoint: URL of the target to be tested

        :rtype: :class:`syntribos.clients.http.models.RequestObject`
        :returns: RequestObject with method, url, params, etc. for use by
                  runner
        """
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
        return cls.request_model_type(
            method=method, url=url, headers=headers, params=params, data=data,
            action_field=action_field)

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
        valid_versions = ["HTTP/1.1", "HTTP/1.0", "HTTP/0.9"]

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
            raise ValueError("Invalid HTTP method: {0}".format(method))

        if version not in valid_versions:
            raise ValueError("Invalid HTTP version: {0}".format(version))

        return method, url, params, version

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
        return headers

    @classmethod
    def _parse_data(cls, lines):
        """Parse the body of the HTTP request (e.g. POST variables)

        :param list lines: lines of the HTTP body

        :returns: object representation of body data (JSON or XML)
        """
        postdat_regex = "([\w%]+=[\w%]+&?)+"
        data = "\n".join(lines).strip()
        if not data:
            return ""
        try:
            data = json.loads(data)
            # TODO(cneill): Make this less hacky
            if isinstance(data, list):
                data = json.dumps(data)
        except Exception:
            try:
                data = ElementTree.fromstring(data)
            except Exception:
                if not re.match(postdat_regex, data):
                    raise TypeError("Unknown data format")
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
