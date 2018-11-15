# Copyright 2016 Rackspace
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

import requests.exceptions as rex
from six.moves import http_client as httplib

import syntribos.signal


def check_fail(exception):
    """Checks for a requestslib exception, returns a signal if found.

    If this Exception is an instance of
    :class:`requests.exceptions.RequestException`, determine what kind of
    exception was raised. If not, return the results of from_generic_exception.

    :param Exception exception: An Exception object
    :returns: Signal with exception details
    :rtype: :class:`syntribos.signal.SynSignal`
    """
    check_name = "HTTP_CHECK_FAIL"

    def uncamel(string):
        string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).upper()

    if not isinstance(exception, rex.RequestException):
        return syntribos.signal.from_generic_exception(exception)

    data = {
        "response": exception.response,
        "request": exception.request,
        "exception": exception,
        "exception_name": uncamel(exception.__class__.__name__)
    }
    text = "An exception was encountered when sending the request. {desc}"
    slug = "HTTP_FAIL_{exc}".format(exc=data["exception_name"])
    tags = set(["EXCEPTION_RAISED"])

    invalid_request_exceptions = (rex.URLRequired, rex.MissingSchema,
                                  rex.InvalidSchema, rex.InvalidURL)

    if exception.__doc__:
        text = text.format(desc=exception.__doc__)
    else:
        text = text.format(
            desc="An unknown exception was raised. Please report this.")

    # CONNECTION FAILURES
    if isinstance(exception, (rex.ProxyError, rex.SSLError,
                              rex.ChunkedEncodingError, rex.ConnectionError)):
        tags.update(["CONNECTION_FAIL"])
    # TIMEOUTS
    elif isinstance(exception, (rex.ConnectTimeout, rex.ReadTimeout)):
        tags.update(["CONNECTION_TIMEOUT", "SERVER_FAIL"])
    # INVALID REQUESTS
    elif isinstance(exception, invalid_request_exceptions):
        tags.update(["INVALID_REQUEST", "CLIENT_FAIL"])

    return syntribos.signal.SynSignal(
        text=text,
        slug=slug,
        strength=1.0,
        tags=list(tags),
        data=data,
        check_name=check_name)


def check_status_code(response):
    """Returns a signal with info about a response's HTTP status code

    :param response: A `Response` object
    :type response: :class:`requests.Response`
    :returns: Signal with status code details
    :rtype: :class:`syntribos.signal.SynSignal`
    """
    check_name = "HTTP_STATUS_CODE"
    codes = httplib.responses

    data = {
        "response": response,
        "status_code": response.status_code,
        "reason": response.reason,
    }
    if codes.get(response.status_code, None):
        data["details"] = codes[response.status_code]
    else:
        data["details"] = "Unknown"

    text = ("A {code} HTTP status code was returned by the server, with reason"
            " '{reason}'. This status code usually means '{details}'.").format(
                code=data["status_code"],
                reason=data["reason"],
                details=data["details"])

    slug = "HTTP_STATUS_CODE_{range}"
    tags = []

    if data["status_code"] in range(200, 300):
        slug = slug.format(range="2XX")

    elif data["status_code"] in range(300, 400):
        slug = slug.format(range="3XX")

        # CCNEILL: 304 == use local cache; not really a redirect
        if data["status_code"] != 304:
            tags.append("SERVER_REDIRECT")

    elif data["status_code"] in range(400, 500):
        slug = slug.format(range="4XX")
        tags.append("CLIENT_FAIL")

    elif data["status_code"] in range(500, 600):
        slug = slug.format(range="5XX")
        tags.append("SERVER_FAIL")

    slug = (slug + "_{code}").format(code=data["status_code"])

    return syntribos.signal.SynSignal(
        text=text,
        slug=slug,
        strength=1,
        tags=tags,
        data=data,
        check_name=check_name)


def check_content_type(response):
    """Returns a signal with info about a response's content type

    :param response:
    :type response: :class:`requests.Response`
    :returns: Signal with content type info
    :rtype: :class:`syntribos.signal.SynSignal`
    """

    check_name = "HTTP_CONTENT_TYPE"
    # LOOKUP MAPS
    known_subtypes = ["xml", "json", "javascript", "html", "plain"]
    known_suffixes = ["xml", "json"]  # RFC6838

    raw_type = response.headers.get("Content-Type", "unknown/unknown").lower()
    fuzzy_type = None

    # valid headers should be in form type/subtype
    if "/" not in raw_type:
        raise Exception("Not a valid content type. What happened?")

    # chop off encodings, etc (ex: application/json[; charset=utf-8])
    if ";" in raw_type:
        raw_type = raw_type.split(";")[0]

    _, subtype = raw_type.split("/")

    # if subtype is known, return that (ex: application/[json])
    if subtype in known_subtypes:
        fuzzy_type = subtype.upper()

    # check for known 'suffixes' (ex: application/atom+[xml])
    elif "+" in subtype:
        _, suffix = subtype.split("+")
        if suffix in known_suffixes:
            fuzzy_type = suffix.upper()

    # fuzzy search for other types (ex: text/[xml]-external-parsed-entity)
    else:
        for s in known_subtypes:
            if s in subtype:
                fuzzy_type = s.upper()
                break

    text = ("The content type returned by the server was {raw}. We determined"
            " this is of the general type {fuzzy_type}.").format(
                raw=raw_type, fuzzy_type=fuzzy_type)

    slug = "HTTP_CONTENT_TYPE_{fuzzy_type}".format(fuzzy_type=fuzzy_type)

    data = {"raw_type": raw_type, "fuzzy_type": fuzzy_type}

    return syntribos.signal.SynSignal(
        text=text, slug=slug, strength=1.0, data=data, check_name=check_name)
