# Copyright 2015 Rackspace
#
# Original from OpenCafe (https://github.com/openstack/opencafe)
#
# Changes copyright 2016 Intel
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
from time import time

import requests
from requests.packages import urllib3
import six

import syntribos.checks.http as http_checks
import syntribos.signal


urllib3.disable_warnings()


def _log_transaction(log, level=logging.DEBUG):
    """Decorator used for logging requests/response in clients.

    Takes a python Logger object and an optional logging level.
    """

    def _safe_decode(text, incoming='utf-8', errors='replace'):
        """Decodes incoming text/bytes using `incoming` if not already unicode.

        :param incoming: Text's current encoding
        :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html

        :returns: text or a unicode `incoming` encoded
        representation of it.
        """

        if isinstance(text, six.text_type):
            return text

        return text.decode(incoming, errors)

    def _decorator(func):
        """Accepts a function and returns wrapped version of that function."""
        def _wrapper(*args, **kwargs):
            """Logging wrapper for any method that returns a requests response.

            Logs requestslib response objects, and the args and kwargs
            sent to the request() method, to the provided log at the provided
            log level.
            """

            logline = '{0} {1}'.format(args, kwargs)

            try:
                log.debug(_safe_decode(logline))
            except Exception as exception:
                # Ignore all exceptions that happen in logging, then log them
                log.info(
                    'Exception occured while logging signature of calling'
                    'method in http client')
                log.exception(exception)

            # Make the request and time its execution
            response = None
            elapsed = None
            signals = syntribos.signal.SignalHolder()

            try:
                start = time()
                response = func(*args, **kwargs)
            except requests.exceptions.RequestException as exc:
                signals.register(http_checks.check_fail(exc))
            except Exception as exc:
                log.critical('Call to Requests failed due to exception')
                log.exception(exception)
                signals.register(syntribos.signal.from_generic_exception(exc))
                raise exc

            elapsed = time() - start

            if response is None:
                log.log(level, "COULD NOT RETRIEVE RESPONSE FOR REQUEST")
                return (response, signals)

            # requests lib 1.0.0 renamed body to data in the request object
            request_body = ''
            if 'body' in dir(response.request):
                request_body = response.request.body
            elif 'data' in dir(response.request):
                request_body = response.request.data
            else:
                log.info(
                    "Unable to log request body, neither a 'data' nor a "
                    "'body' object could be found")

            # requests lib 1.0.4 removed params from response.request
            request_params = ''
            request_url = response.request.url
            if 'params' in dir(response.request):
                request_params = response.request.params
            elif '?' in request_url:
                request_url, request_params = request_url.split('?')

            logline = ''.join([
                '\n{0}\nREQUEST SENT\n{0}\n'.format('-' * 12),
                'request method..: {0}\n'.format(response.request.method),
                'request url.....: {0}\n'.format(request_url),
                'request params..: {0}\n'.format(request_params),
                'request headers.: {0}\n'.format(response.request.headers),
                'request body....: {0}\n'.format(request_body)])
            try:
                log.log(level, _safe_decode(logline))
            except Exception as exception:
                # Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nREQUEST INFO\n{0}\n'.format('-' * 12))
                log.exception(exception)

            logline = ''.join([
                '\n{0}\nRESPONSE RECEIVED\n{0}\n'.format('-' * 17),
                'response status..: {0}\n'.format(response),
                'response time....: {0}\n'.format(elapsed),
                'response headers.: {0}\n'.format(response.headers),
                'response body....: {0}\n'.format(response.content),
                '-' * 79])
            try:
                log.log(level, _safe_decode(logline))
            except Exception as exception:
                # Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nRESPONSE INFO\n{0}\n'.format('-' * 13))
                log.exception(exception)
            return (response, signals)
        return _wrapper
    return _decorator


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

    _log = logging.getLogger(__name__)

    def __init__(self):
        self.default_headers = {}

    @_log_transaction(log=_log)
    def request(
            self, method, url, headers=None, params=None, data=None,
            requestslib_kwargs=None):

        # set requestslib_kwargs to an empty dict if None
        requestslib_kwargs = requestslib_kwargs if (
            requestslib_kwargs is not None) else {}

        # Set defaults
        params = params if params is not None else {}
        verify = False

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
