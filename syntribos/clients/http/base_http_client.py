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
import logging

import requests
from requests.packages import urllib3

from syntribos.clients.http.debug_logger import log_http_transaction

urllib3.disable_warnings()


class HTTPClient(object):

    """Allows clients to inherit requests.request.

    @summary: Redefines request() so that keyword args are passed.
              The parameters are passed through a named dictionary
              instead of kwargs. Client methods can then take parameters
              that may overload request parameters, which allows client
              method calls to override parts of the request with parameters
              sent directly to requests, overriding the client method logic
              either in part or whole on the fly.

    """

    LOG = logging.getLogger(__name__)

    def __init__(self):
        self.default_headers = {}

    @log_http_transaction(log=LOG)
    def request(self, method, url, headers=None, params=None, data=None,
                sanitize=False, requestslib_kwargs=None):

        # set requestslib_kwargs to an empty dict if None
        requestslib_kwargs = requestslib_kwargs if (
            requestslib_kwargs is not None) else {}

        # Set defaults
        params = params if params is not None else {}
        verify = False
        sanitize = sanitize

        # If headers are provided by both, headers "wins" over default_headers
        headers = dict(self.default_headers, **(headers or {}))

        # Override url if present in requestslib_kwargs
        if 'url' in list(requestslib_kwargs.keys()):
            url = requestslib_kwargs.get('url', None) or url
            del requestslib_kwargs['url']

        # Override method if present in requestslib_kwargs
        if 'method' in list(requestslib_kwargs.keys()):
            method = requestslib_kwargs.get('method', None) or method
            del requestslib_kwargs['method']

        # The requests lib already removes None key/value pairs, but we force
        # it here in case that behavior ever changes
        for key in list(requestslib_kwargs.keys()):
            if requestslib_kwargs[key] is None:
                del requestslib_kwargs[key]

        # Create the final parameters for the call to the base request()
        # Wherever a parameter is provided both by the calling method AND
        # the requests_lib kwargs dictionary, requestslib_kwargs "wins"
        requestslib_kwargs = dict(
            {'headers': headers, 'params': params, 'verify': verify,
             'data': data}, **requestslib_kwargs)

        # Make the request
        return requests.request(method, url, **requestslib_kwargs)
