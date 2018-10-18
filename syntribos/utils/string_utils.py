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
import pprint
import zlib

from oslo_config import cfg
from oslo_utils import strutils
from requests.structures import CaseInsensitiveDict
import six

CONF = cfg.CONF


def is_dict(content=None):
    return isinstance(content, CaseInsensitiveDict) or isinstance(content,
                                                                  dict)


def is_string(content=None):
    return isinstance(content, six.string_types)


def sanitize_secrets(content, mask="****"):
    """Extends oslo_utils strutils to make mask passwords more robust."""

    def mask_dict_password(dictionary, secret="***"):
        """Overriding strutils.mask_dict_password.

        Overriding mask_dict_password to accept CaseInsenstiveDict as well.
        """
        out = deepcopy(dictionary)

        for k, v in dictionary.items():
            if is_dict(v):
                out[k] = mask_dict_password(v, secret=secret)
                continue
            for sani_key in strutils._SANITIZE_KEYS:
                if sani_key in k:
                    out[k] = secret
                    break
            else:
                if isinstance(v, six.string_types):
                    out[k] = strutils.mask_password(v, secret=secret)
        return out

    strutils.mask_dict_password = mask_dict_password
    if is_dict(content):
        return strutils.mask_dict_password(content, mask)
    if is_string(content):
        return strutils.mask_password(content, mask)


def compress(content, threshold=512):
    """Uses zlib to do basic compression of content.

    Mostly used for compressing long fuzz strings in request body and
    response content. The threshold to start data compression is set at 512,
    if the content length is more than 512, it would be compressed using a
    default level of 6.

    :params: content, threshold
    :ptype: str, int
    :returns: Compressed String
    :rtype: str
    """
    compression_enabled = CONF.logging.http_request_compression

    if is_dict(content):
        for key in content:
            content[key] = compress(content[key])
    if is_string(content) and compression_enabled:
        if len(content) > threshold:
            less_data = content[:50]
            compressed_data = base64.b64encode(
                zlib.compress(bytes(content.encode("utf-8"))))
            if not six.PY2:
                compressed_data = str(compressed_data.decode("utf-8"))
            return pprint.pformat(
                "\n***Content compressed by Syntribos.***"
                "\nFirst fifty characters of content:\n"
                "***{data}***"
                "\nBase64 encoded compressed content:\n"
                "{compressed}"
                "\n***End of compressed content.***\n".format(
                    data=less_data, compressed=compressed_data))
    return content
