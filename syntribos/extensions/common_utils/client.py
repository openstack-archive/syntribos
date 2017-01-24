# Copyright 2016 Intel
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
import datetime
import hashlib
import hmac
import logging
import time

import six

LOG = logging.getLogger(__name__)


def hash_it(data, hash_type="sha256"):
    """Returns hashed value of data."""
    if hash_type == "sha1":
        hash_obj = hashlib.sha1()
    elif hash_type == "md5":
        hash_obj = hashlib.md5()
    else:
        hash_obj = hashlib.sha256()
    try:
        hash_obj.update(data.encode())
        return hash_obj.hexdigest()
    except (TypeError, AttributeError) as e:
        LOG.error("Couldn't hash the data, exception raised: %s", e)
        return hash(data)


def hmac_it(data, key, hash_type="sha256"):
    """Returns HMAC based on the hash algorithm, data and key."""
    if hash_type == "md5":
        hash_obj = hashlib.md5
    elif hash_type == "sha1":
        hash_obj = hashlib.sha1
    else:
        hash_obj = hashlib.sha256
    try:
        h_digest = hmac.new(key.encode(), data.encode(), hash_obj)
        return h_digest.hexdigest()
    except (TypeError, AttributeError) as e:
        LOG.error("Couldn't hash the data, exception raised: %s", e)


def epoch_time(offset=0):
    """Returns time since epoch."""
    try:
        return time.time() - offset
    except TypeError as e:
        LOG.error("Couldn't reduce offset, %s, from epoch time, ex %s.",
                  offset, e)
        return time.time()


def utc_datetime():
    """Returns utc date time."""
    epoch = epoch_time()
    ts = datetime.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")
    return ts


def base64_encode(data):
    """Returns base 64 encoded value of data."""
    try:
        data = base64.b64encode(data.encode())
    except TypeError as e:
        LOG.error("Couldn't encode data to base64: %s", e)
    return data


def url_encode(url):
    """Returns encoded URL."""
    try:
        return six.moves.urllib.parse.quote_plus(url)
    except TypeError as e:
        LOG.error("Couldn't encode the URL: %s", e)
        return url
