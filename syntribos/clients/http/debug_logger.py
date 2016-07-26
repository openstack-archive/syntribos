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
import base64
from copy import deepcopy
import logging
from time import time
import zlib

from oslo_config import cfg
import requests
from requests.structures import CaseInsensitiveDict
import six

import syntribos.checks.http as http_checks
import syntribos.signal

CONF = cfg.CONF


def compress(content, threshold=512):
    """Uses zlib to do basic compression of content.

    Mostly used for compressing long fuzz strings in request body and
    response content. The threshold to start data compression is set at 512,
    if the content length is more than 512, it would be compressed using a
    default level of 6.

    :params: content, threshold
    :ptype: String, int
    :returns: Compressed String
    :rtype: String
    """
    is_dict = isinstance(content, CaseInsensitiveDict) or isinstance(
        content, dict)
    is_string = isinstance(content, six.string_types)
    compression_enabled = CONF.logging.http_request_compression

    if is_dict:
        for key in content:
                content[key] = compress(content[key])
    if is_string and compression_enabled:
        if len(content) > threshold:
            less_data = content[:50]
            compressed_data = base64.b64encode(zlib.compress(content))
            return ("******Content compressed by Syntribos.******\n"
                    "First fifty characters of the content:\n"
                    "       {data}\n       "
                    "Base64 encoded compressed content:\n"
                    "       {compressed}\n      "
                    "******End of compressed content.******\n").format(
                        data=less_data, compressed=compressed_data)
    return content


def log_http_transaction(log, level=logging.DEBUG):
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
            kwargs_copy = deepcopy(kwargs)
            logline = '{0} {1}'.format(args, compress(kwargs_copy))

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
            no_resp_time = None
            signals = syntribos.signal.SignalHolder()

            try:
                start = time()
                response = func(*args, **kwargs)
            except requests.exceptions.RequestException as exc:
                signals.register(http_checks.check_fail(exc))
                log.log(level, "A call to request() failed.")
                log.exception(exc)
                log.log(level, "=" * 80)
            except Exception as exc:
                log.critical('Call to Requests failed due to exception')
                log.exception(exc)
                signals.register(syntribos.signal.from_generic_exception(exc))
                raise exc

            if len(signals) > 0 and response is None:
                no_resp_time = time() - start
                log.log(level,
                        'Request failed, elapsed time....: {0:.5f} sec.\n'.
                        format(no_resp_time))
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

            req_body_len = 0
            req_header_len = 0
            if response.request.headers:
                req_header_len = len(response.request.headers)
            if response.request.body:
                req_body_len = len(response.request.body)

            logline = ''.join([
                '\n{0}\nREQUEST SENT\n{0}\n'.format('-' * 12),
                'request method.......: {0}\n'.format(response.request.method),
                'request url..........: {0}\n'.format(compress(request_url)),
                'request params.......: {0}\n'.format(compress
                                                      (request_params)),
                'request headers size.: {0}\n'.format(req_header_len),
                'request headers......: {0}\n'.format(compress(
                    response.request.headers)),
                'request body size....: {0}\n'.format(req_body_len),
                'request body.........: {0}\n'.format(compress
                                                      (request_body))])

            try:
                log.log(level, _safe_decode(logline))
            except Exception as exception:
                # Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nREQUEST INFO\n{0}\n'.format('-' * 12))
                log.exception(exception)

            logline = ''.join([
                '\n{0}\nRESPONSE RECEIVED\n{0}\n'.format('-' * 17),
                'response status..: {0}\n'.format(response),
                'response headers.: {0}\n'.format(response.headers),
                'response time....: {0}\n'.format
                (response.elapsed.total_seconds()),
                'response size....: {0}\n'.format(len(response.content)),
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
